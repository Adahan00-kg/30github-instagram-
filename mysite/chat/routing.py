from django.urls import path
from .cunsomers import ChatConsumer,NotificationConsumer

websocket_urlpatterns = [
    path('ws/chat/<int:chat_id>/', ChatConsumer.as_asgi()),
    path('ws/notifications/', NotificationConsumer.as_asgi()),  # Добавляем маршрут для уведомлений
]