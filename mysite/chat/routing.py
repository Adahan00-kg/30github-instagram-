from django.urls import path
from .cunsomers import *

websocket_urlpatterns = [
    path('ws/chat/<str:chat_id>/',ChatConsumer.as_asgi()),
]