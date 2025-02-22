import json
from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async
from .models import Chat, Message
from mysite.register_user.models import UserProfile


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        """ Подключение к личному чату """
        self.user = self.scope["user"]
        self.chat_id = self.scope["url_route"]["kwargs"]["chat_id"]

        # Проверяем, является ли пользователь участником чата
        self.chat = await sync_to_async(Chat.objects.get)(id=self.chat_id)
        if self.user not in [self.chat.user1, self.chat.user2]:
            await self.close()
            return

        self.room_name = f"chat_{self.chat_id}"

        # Присоединяемся к личному чату
        await self.channel_layer.group_add(self.room_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        """ Отключение от чата """
        await self.channel_layer.group_discard(self.room_name, self.channel_name)

    async def receive(self, text_data):
        """ Получаем сообщение от пользователя """
        data = json.loads(text_data)
        text = data.get("text", "")

        # Создаём сообщение в БД
        message = await sync_to_async(Message.objects.create)(
            chat=self.chat, author=self.user, text=text
        )

        message_data = {
            "id": message.id,
            "chat_id": self.chat_id,
            "author": self.user.id,
            "text": text,
            "created_at": str(message.created_at),
        }

        # Отправляем сообщение только собеседнику
        await self.channel_layer.group_send(
            self.room_name, {"type": "chat_message", "message": message_data}
        )

    async def chat_message(self, event):
        """ Отправляем сообщение пользователю """
        message = event["message"]
        await self.send(text_data=json.dumps(message))
