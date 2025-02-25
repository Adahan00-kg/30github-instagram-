import json
import uuid
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.utils import timezone
from django.core.files.base import ContentFile
import base64
from .models import Chat, Message, ChatNotification
from register_user.models import UserProfile


class ChatConsumer(AsyncWebsocketConsumer):
    """WebSocket-консьюмер для чата в стиле Instagram"""

    async def connect(self):
        """Подключение пользователя к WebSocket"""
        self.user = self.scope["user"]

        # Проверяем аутентификацию
        if not self.user.is_authenticated:
            await self.close()
            return

        # Получаем chat_id из маршрута
        self.chat_id = self.scope["url_route"]["kwargs"]["chat_id"]
        self.room_name = f"chat_{self.chat_id}"

        # Проверяем, является ли пользователь участником чата
        chat_exists = await self.check_chat_permission()
        if not chat_exists:
            await self.close()
            return

        # Присоединяемся к группе чата
        await self.channel_layer.group_add(self.room_name, self.channel_name)
        await self.accept()

        # Отмечаем сообщения как прочитанные при подключении
        await self.mark_messages_as_read()

        # Отправляем статус онлайн другим участникам
        await self.send_online_status(True)

    async def disconnect(self, close_code):
        """Отключение пользователя"""
        if hasattr(self, 'room_name'):
            # Отправляем статус оффлайн перед отключением
            await self.send_online_status(False)
            # Удаляем пользователя из группы чата
            await self.channel_layer.group_discard(self.room_name, self.channel_name)

    async def receive(self, text_data):
        """Обработка входящих сообщений"""
        data = json.loads(text_data)
        message_type = data.get("type", "text")

        if message_type == "message":
            # Обработка обычного сообщения
            await self.handle_chat_message(data)
        elif message_type == "typing":
            # Обработка статуса печатания
            await self.handle_typing_status(data)
        elif message_type == "read":
            # Обработка отметки о прочтении
            await self.handle_read_status(data)
        elif message_type == "like":
            # Обработка лайка сообщения
            await self.handle_message_like(data)
        elif message_type == "delete":
            # Обработка удаления сообщения
            await self.handle_message_delete(data)
        elif message_type == "media":
            # Обработка медиа-сообщения (изображение/видео/аудио)
            await self.handle_media_message(data)
        elif message_type == "story_reply":
            # Обработка ответа на сторис
            await self.handle_story_reply(data)
        elif message_type == "post_share":
            # Обработка пересылки поста
            await self.handle_post_share(data)
        elif message_type == "disappearing":
            # Обработка исчезающего сообщения
            await self.handle_disappearing_message(data)

    # ---- Обработчики различных типов сообщений ----

    async def handle_chat_message(self, data):
        """Обработка текстового сообщения"""
        message_text = data.get("message", "")
        if not message_text.strip():
            return

        # Сохраняем сообщение в базе данных
        message = await self.save_message(message_text)

        # Создаем уведомление для получателя
        await self.create_notification(message)

        # Обновляем время последнего сообщения в чате
        await self.update_last_message_time()

        # Отправляем сообщение всем участникам чата
        await self.channel_layer.group_send(
            self.room_name,
            {
                "type": "chat_message",
                "message": message_text,
                "sender_id": self.user.id,
                "sender_username": self.user.username,
                "message_id": message.id,
                "timestamp": str(message.timestamp),
            }
        )

    async def handle_typing_status(self, data):
        """Обработка статуса печатания"""
        is_typing = data.get("is_typing", False)

        # Отправляем статус печатания всем участникам чата
        await self.channel_layer.group_send(
            self.room_name,
            {
                "type": "typing_status",
                "user_id": self.user.id,
                "username": self.user.username,
                "is_typing": is_typing,
            }
        )

    async def handle_read_status(self, data):
        """Обработка отметки о прочтении"""
        # Отмечаем сообщения как прочитанные
        count = await self.mark_messages_as_read()

        if count > 0:
            # Отправляем статус прочтения всем участникам чата
            await self.channel_layer.group_send(
                self.room_name,
                {
                    "type": "read_status",
                    "user_id": self.user.id,
                    "username": self.user.username,
                    "timestamp": str(timezone.now()),
                }
            )

    async def handle_message_like(self, data):
        """Обработка лайка сообщения"""
        message_id = data.get("message_id")
        action = data.get("action", "like")  # like или unlike

        if not message_id:
            return

        # Обновляем статус лайка в базе данных
        success = await self.toggle_message_like(message_id, action == "like")

        if success:
            # Отправляем информацию о лайке всем участникам чата
            await self.channel_layer.group_send(
                self.room_name,
                {
                    "type": "message_like",
                    "message_id": message_id,
                    "action": action,
                    "user_id": self.user.id,
                    "username": self.user.username,
                }
            )

    async def handle_message_delete(self, data):
        """Обработка удаления сообщения"""
        message_id = data.get("message_id")

        if not message_id:
            return

        # Проверяем права на удаление и удаляем сообщение
        success = await self.delete_message(message_id)

        if success:
            # Отправляем информацию об удалении всем участникам чата
            await self.channel_layer.group_send(
                self.room_name,
                {
                    "type": "message_delete",
                    "message_id": message_id,
                }
            )

    async def handle_media_message(self, data):
        """Обработка медиа-сообщения"""
        media_type = data.get("media_type", "image")  # image, video, audio
        media_data = data.get("media_data", "")  # Base64-encoded данные
        caption = data.get("caption", "")

        if not media_data:
            return

        # Сохраняем медиа-сообщение
        message = await self.save_media_message(media_type, media_data, caption)

        if message:
            # Создаем уведомление
            await self.create_notification(message)

            # Обновляем время последнего сообщения
            await self.update_last_message_time()

            # Формируем URL медиа-файла
            media_url = ""
            if media_type == "image" and message.image:
                media_url = message.image.url
            elif media_type == "video" and message.video:
                media_url = message.video.url
            elif media_type == "audio" and message.audio:
                media_url = message.audio.url

            # Отправляем медиа-сообщение всем участникам
            await self.channel_layer.group_send(
                self.room_name,
                {
                    "type": "media_message",
                    "media_type": media_type,
                    "media_url": media_url,
                    "caption": caption,
                    "message_id": message.id,
                    "sender_id": self.user.id,
                    "sender_username": self.user.username,
                    "timestamp": str(message.timestamp),
                }
            )

    async def handle_story_reply(self, data):
        """Обработка ответа на историю"""
        story_id = data.get("story_id")
        reply_text = data.get("reply", "")

        if not story_id or not reply_text.strip():
            return

        # Сохраняем ответ на историю
        message = await self.save_story_reply(story_id, reply_text)

        if message:
            # Создаем уведомление
            await self.create_notification(message)

            # Обновляем время последнего сообщения
            await self.update_last_message_time()

            # Отправляем ответ на историю всем участникам
            await self.channel_layer.group_send(
                self.room_name,
                {
                    "type": "story_reply",
                    "story_id": story_id,
                    "reply": reply_text,
                    "message_id": message.id,
                    "sender_id": self.user.id,
                    "sender_username": self.user.username,
                    "timestamp": str(message.timestamp),
                }
            )

    async def handle_post_share(self, data):
        """Обработка пересылки поста"""
        post_id = data.get("post_id")
        comment = data.get("comment", "")

        if not post_id:
            return

        # Сохраняем пересылку поста
        message = await self.save_post_share(post_id, comment)

        if message:
            # Создаем уведомление
            await self.create_notification(message)

            # Обновляем время последнего сообщения
            await self.update_last_message_time()

            # Отправляем информацию о пересылке поста всем участникам
            await self.channel_layer.group_send(
                self.room_name,
                {
                    "type": "post_share",
                    "post_id": post_id,
                    "comment": comment,
                    "message_id": message.id,
                    "sender_id": self.user.id,
                    "sender_username": self.user.username,
                    "timestamp": str(message.timestamp),
                }
            )

    async def handle_disappearing_message(self, data):
        """Обработка исчезающего сообщения"""
        message_text = data.get("message", "")
        duration = data.get("duration", 60)  # Длительность в секундах (по умолчанию 60 секунд)

        if not message_text.strip():
            return

        # Рассчитываем время истечения
        expire_time = timezone.now() + timezone.timedelta(seconds=duration)

        # Сохраняем исчезающее сообщение
        message = await self.save_disappearing_message(message_text, expire_time)

        if message:
            # Создаем уведомление
            await self.create_notification(message)

            # Обновляем время последнего сообщения
            await self.update_last_message_time()

            # Отправляем исчезающее сообщение всем участникам
            await self.channel_layer.group_send(
                self.room_name,
                {
                    "type": "disappearing_message",
                    "message": message_text,
                    "expire_at": str(expire_time),
                    "message_id": message.id,
                    "sender_id": self.user.id,
                    "sender_username": self.user.username,
                    "timestamp": str(message.timestamp),
                }
            )

    # ---- Отправка сообщений клиентам ----

    async def chat_message(self, event):
        """Отправка текстового сообщения клиенту"""
        await self.send(text_data=json.dumps({
            "type": "message",
            "message": event["message"],
            "sender_id": event["sender_id"],
            "sender_username": event["sender_username"],
            "message_id": event["message_id"],
            "timestamp": event["timestamp"],
        }))

    async def typing_status(self, event):
        """Отправка статуса печатания клиенту"""
        await self.send(text_data=json.dumps({
            "type": "typing",
            "user_id": event["user_id"],
            "username": event["username"],
            "is_typing": event["is_typing"],
        }))

    async def read_status(self, event):
        """Отправка статуса прочтения клиенту"""
        await self.send(text_data=json.dumps({
            "type": "read",
            "user_id": event["user_id"],
            "username": event["username"],
            "timestamp": event["timestamp"],
        }))

    async def message_like(self, event):
        """Отправка информации о лайке клиенту"""
        await self.send(text_data=json.dumps({
            "type": "like",
            "message_id": event["message_id"],
            "action": event["action"],
            "user_id": event["user_id"],
            "username": event["username"],
        }))

    async def message_delete(self, event):
        """Отправка информации об удалении сообщения клиенту"""
        await self.send(text_data=json.dumps({
            "type": "delete",
            "message_id": event["message_id"],
        }))

    async def media_message(self, event):
        """Отправка медиа-сообщения клиенту"""
        await self.send(text_data=json.dumps({
            "type": "media",
            "media_type": event["media_type"],
            "media_url": event["media_url"],
            "caption": event["caption"],
            "message_id": event["message_id"],
            "sender_id": event["sender_id"],
            "sender_username": event["sender_username"],
            "timestamp": event["timestamp"],
        }))

    async def story_reply(self, event):
        """Отправка ответа на историю клиенту"""
        await self.send(text_data=json.dumps({
            "type": "story_reply",
            "story_id": event["story_id"],
            "reply": event["reply"],
            "message_id": event["message_id"],
            "sender_id": event["sender_id"],
            "sender_username": event["sender_username"],
            "timestamp": event["timestamp"],
        }))

    async def post_share(self, event):
        """Отправка информации о пересылке поста клиенту"""
        await self.send(text_data=json.dumps({
            "type": "post_share",
            "post_id": event["post_id"],
            "comment": event["comment"],
            "message_id": event["message_id"],
            "sender_id": event["sender_id"],
            "sender_username": event["sender_username"],
            "timestamp": event["timestamp"],
        }))

    async def disappearing_message(self, event):
        """Отправка исчезающего сообщения клиенту"""
        await self.send(text_data=json.dumps({
            "type": "disappearing_message",
            "message": event["message"],
            "expire_at": event["expire_at"],
            "message_id": event["message_id"],
            "sender_id": event["sender_id"],
            "sender_username": event["sender_username"],
            "timestamp": event["timestamp"],
        }))

    async def online_status(self, event):
        """Отправка статуса онлайн клиенту"""
        await self.send(text_data=json.dumps({
            "type": "online_status",
            "user_id": event["user_id"],
            "username": event["username"],
            "is_online": event["is_online"],
        }))

    # ---- Вспомогательные методы для работы с базой данных ----

    @database_sync_to_async
    def check_chat_permission(self):
        """Проверяет, имеет ли пользователь доступ к чату"""
        try:
            profile = self.user.profile  # Предполагается, что у User есть связь с UserProfile
            chat = Chat.objects.get(id=self.chat_id)
            self.chat = chat

            # Пользователь должен быть участником чата
            if profile != chat.user1 and profile != chat.user2:
                return False

            return True
        except (Chat.DoesNotExist, UserProfile.DoesNotExist):
            return False

    @database_sync_to_async
    def save_message(self, text):
        """Сохраняет текстовое сообщение в базе данных"""
        profile = self.user.profile
        return Message.objects.create(
            chat=self.chat,
            sender=profile,
            text=text
        )

    @database_sync_to_async
    def save_media_message(self, media_type, media_data, caption=""):
        """Сохраняет медиа-сообщение в базе данных"""
        try:
            # Удаляем префикс из Base64-строки
            if 'base64,' in media_data:
                header, media_data = media_data.split('base64,')

            # Декодируем Base64
            decoded_data = base64.b64decode(media_data)

            # Создаем уникальное имя файла
            file_name = f"{uuid.uuid4()}"

            profile = self.user.profile
            message = Message(
                chat=self.chat,
                sender=profile,
                text=caption
            )

            # Сохраняем соответствующий тип медиа
            if media_type == "image":
                message.image.save(f"{file_name}.jpg", ContentFile(decoded_data))
            elif media_type == "video":
                message.video.save(f"{file_name}.mp4", ContentFile(decoded_data))
            elif media_type == "audio":
                message.audio.save(f"{file_name}.mp3", ContentFile(decoded_data))

            message.save()
            return message
        except Exception as e:
            print(f"Error saving media message: {e}")
            return None

    @database_sync_to_async
    def save_story_reply(self, story_id, reply_text):
        """Сохраняет ответ на историю"""
        profile = self.user.profile
        return Message.objects.create(
            chat=self.chat,
            sender=profile,
            text=reply_text,
            is_story_reply=True,
            story_id=story_id
        )

    @database_sync_to_async
    def save_post_share(self, post_id, comment=""):
        """Сохраняет пересылку поста"""
        profile = self.user.profile
        return Message.objects.create(
            chat=self.chat,
            sender=profile,
            text=comment,
            is_post_share=True,
            post_id=post_id
        )

    @database_sync_to_async
    def save_disappearing_message(self, text, expire_at):
        """Сохраняет исчезающее сообщение"""
        profile = self.user.profile
        return Message.objects.create(
            chat=self.chat,
            sender=profile,
            text=text,
            is_disappearing=True,
            expire_at=expire_at
        )

    @database_sync_to_async
    def mark_messages_as_read(self):
        """Отмечает все непрочитанные сообщения как прочитанные"""
        return self.chat.mark_all_as_read(self.user)

    @database_sync_to_async
    def toggle_message_like(self, message_id, is_like):
        """Устанавливает или снимает лайк с сообщения"""
        try:
            message = Message.objects.get(id=message_id, chat=self.chat)

            if is_like:
                message.like()
            else:
                message.unlike()

            return True
        except Message.DoesNotExist:
            return False

    @database_sync_to_async
    def delete_message(self, message_id):
        """Удаляет сообщение (только если пользователь является отправителем)"""
        try:
            message = Message.objects.get(id=message_id, chat=self.chat)

            # Проверяем, что пользователь является отправителем
            if message.sender == self.user.profile:
                message.delete()
                return True

            return False
        except Message.DoesNotExist:
            return False

    @database_sync_to_async
    def create_notification(self, message):
        """Создает уведомление о новом сообщении для получателя"""
        # Определяем получателя (не отправителя)
        profile = self.user.profile
        recipient = self.chat.user2 if profile == self.chat.user1 else self.chat.user1

        # Создаем уведомление
        return ChatNotification.objects.create(
            user=recipient,
            chat=self.chat,
            message=message
        )

    @database_sync_to_async
    def update_last_message_time(self):
        """Обновляет время последнего сообщения в чате"""
        self.chat.last_message_at = timezone.now()
        self.chat.save()

    async def send_online_status(self, is_online):
        """Отправляет статус онлайн другим участникам чата"""
        await self.channel_layer.group_send(
            self.room_name,
            {
                "type": "online_status",
                "user_id": self.user.id,
                "username": self.user.username,
                "is_online": is_online,
            }
        )


# Консьюмер для получения уведомлений о новых сообщениях
class NotificationConsumer(AsyncWebsocketConsumer):
    """WebSocket-консьюмер для уведомлений о новых сообщениях"""

    async def connect(self):
        """Подключение пользователя к WebSocket уведомлений"""
        self.user = self.scope["user"]

        # Проверяем аутентификацию
        if not self.user.is_authenticated:
            await self.close()
            return

        # Создаем персональную комн

