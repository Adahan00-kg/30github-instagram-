import json
from channels.generic.websocket import AsyncWebsocketConsumer
from django.contrib.auth import get_user_model
from asgiref.sync import sync_to_async
from .models import Chat, Message
from register_user.models import UserProfile  # Импортируем кастомную модель пользователя
from rest_framework import serializers


class ChatConsumer(AsyncWebsocketConsumer):
    """WebSocket-консьюмер для чата"""

    async def connect(self):
        """ Подключение пользователя к WebSocket """
        self.user = self.scope["user"]  # Получаем текущего пользователя
        self.chat_id = self.scope["url_route"]["kwargs"]["chat_id"]


        # Проверяем, является ли пользователь участником чата
        self.chat = await sync_to_async(Chat.objects.get)(id=self.chat_id)
        if self.user.profile not in [self.chat.user1, self.chat.user2]:  # Проверяем по UserProfile
            await self.close()
            return


        self.room_name = f"chat_{self.chat_id}"  # Уникальное имя комнаты WebSocket
        await self.channel_layer.group_add(self.room_name, self.channel_name)
        await self.accept()  # Подключаем пользователя


    async def disconnect(self, close_code):
        """ Отключение пользователя """
        await self.channel_layer.group_discard(self.room_name, self.channel_name)


    async def receive(self, text_data):
        """ Обработка входящих сообщений """
        data = json.loads(text_data)
        message_text = data.get("message")

