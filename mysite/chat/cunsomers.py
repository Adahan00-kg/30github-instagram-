import json
from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async
from .models import Chat, Message
from register_user.models import UserProfile

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.chat_id = self.scope["url_route"]["kwargs"]["chat_id"]
        self.chat, created = await sync_to_async(Chat.objects.get_or_create)(id=self.chat_id)
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
