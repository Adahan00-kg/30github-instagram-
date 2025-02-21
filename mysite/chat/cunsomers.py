import json
from channels.generic.websocket import AsyncWebsocketConsumer
from .models import Chat, Message, UserProfile
from asgiref.sync import sync_to_async




class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.chat_id = self.scope['url_route']['kwargs']['chat_id']
        self.chat_group_name = f'chat_{self.chat_id}'

        # Присоединяемся к группе чата
        await self.channel_layer.group_add(
            self.chat_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # Покидаем группу чата
        await self.channel_layer.group_discard(
            self.chat_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        data = json.loads(text_data)
        author_id = data['author']
        text = data.get('text', '')

        author = await sync_to_async(UserProfile.objects.get)(id=author_id)
        chat = await sync_to_async(Chat.objects.get)(id=self.chat_id)

        # Создаём сообщение в БД
        message = await sync_to_async(Message.objects.create)(
            chat=chat,
            author=author,
            text=text
        )

        message_data = {
            'id': message.id,
            'chat': self.chat_id,
            'author': author.id,
            'text': text,
            'created_at': str(message.created_at)
        }

        # Отправляем сообщение всем участникам чата
        await self.channel_layer.group_send(
            self.chat_group_name,
            {
                'type': 'chat_message',
                'message': message_data
            }
        )

    async def chat_message(self, event):
        message = event['message']
        await self.send(text_data=json.dumps(message))

