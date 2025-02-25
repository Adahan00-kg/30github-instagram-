from channels.middleware import BaseMiddleware
from channels.db import database_sync_to_async
from django.contrib.auth.models import AnonymousUser
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from urllib.parse import parse_qs
import jwt
from django.conf import settings

User = get_user_model()


@database_sync_to_async
def get_user(user_id):
    try:
        return User.objects.get(id=user_id)
    except User.DoesNotExist:
        return AnonymousUser()


class JWTAuthMiddleware(BaseMiddleware):
    def __init__(self, inner):
        super().__init__(inner)

    async def __call__(self, scope, receive, send):
        # Получаем токен из URL параметров или заголовков
        query_params = parse_qs(scope["query_string"].decode())
        token = None

        # Проверяем заголовки
        headers = dict(scope["headers"])
        if b'authorization' in headers:
            auth_header = headers[b'authorization'].decode('utf-8')
            if auth_header.startswith('Bearer '):
                token = auth_header.split(' ')[1]

        # Если токена нет в заголовках, ищем в query параметрах
        if not token and 'token' in query_params:
            token = query_params['token'][0]

        if token:
            try:
                # Декодируем JWT токен
                payload = jwt.decode(
                    token,
                    settings.SECRET_KEY,
                    algorithms=["HS256"]
                )
                user_id = payload.get('user_id')
                if user_id:
                    # Получаем пользователя из базы
                    scope["user"] = await get_user(user_id)
                else:
                    scope["user"] = AnonymousUser()
            except (InvalidToken, TokenError, jwt.PyJWTError):
                scope["user"] = AnonymousUser()
        else:
            scope["user"] = AnonymousUser()

        return await super().__call__(scope, receive, send)


def JWTAuthMiddlewareStack(inner):
    return JWTAuthMiddleware(inner)
