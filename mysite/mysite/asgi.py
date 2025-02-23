"""
ASGI config for mysite project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/howto/deployment/asgi/
"""
import os
import django
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack

# 1️⃣ Устанавливаем переменную окружения перед импортами Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mysite.settings")

# 2️⃣ Загружаем Django перед импортами моделей и маршрутов
django.setup()

# 3️⃣ Теперь можно импортировать маршруты WebSocket
from chat.routing import websocket_urlpatterns

# 4️⃣ Создаем ASGI-приложение
application = ProtocolTypeRouter({
    "http": get_asgi_application(),  # Django HTTP-приложение
    "websocket": AuthMiddlewareStack(
        URLRouter(websocket_urlpatterns)
    ),
})
