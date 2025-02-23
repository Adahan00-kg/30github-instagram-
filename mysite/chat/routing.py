from django.urls import path
from .cunsomers import *

websocket_urlpatterns = [
    path('ws/chat/<int:chat_id>/',ChatConsumer.as_asgi()),
]