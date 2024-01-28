# import jwt
# from channels.db import database_sync_to_async
# from channels.exceptions import DenyConnection
# from channels.middleware import BaseMiddleware
#
# from blog import settings
# from users.models import User
#
#
# @database_sync_to_async
# def get_user(user_id):
#     try:
#         return User.objects.get(id=user_id)
#     except User.DoesNotExist:
#         return None
#
#
# class JWTAuthMiddleware(BaseMiddleware):
#     async def __call__(self, scope, receive, send):
#         headers = dict(scope["headers"])
#         if b'authorization' in headers:
#             try:
#                 _, token = headers[b'authorization'].decode().split()
#                 decode = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
#                 user_id = decode['user_id']
#                 scope['user'] = await get_user(user_id)
#             except (ValueError, jwt.exceptions.DecodeError):
#                 raise DenyConnection('Invalid token')
#         return await super().__call__(scope, receive, send)

import os
from datetime import datetime

import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

import jwt
from channels.auth import AuthMiddlewareStack
from django.conf import settings
from django.contrib.auth.models import AnonymousUser
from channels.db import database_sync_to_async
from channels.middleware import BaseMiddleware

from django.contrib.auth.models import User
from django.db import close_old_connections

ALGORITHM = "HS256"


@database_sync_to_async
def get_user(token):
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=ALGORITHM)
        print('payload', payload)
    except:
        print('no payload')
        return AnonymousUser()

    token_exp = datetime.fromtimestamp(payload['exp'])
    if token_exp < datetime.utcnow():
        print("no date-time")
        return AnonymousUser()

    try:
        user = User.objects.get(id=payload['user_id'])
        print('user', user)
    except User.DoesNotExist:
        print('no user')
        return AnonymousUser()

    return user


class TokenAuthMiddleware(BaseMiddleware):

    async def __call__(self, scope, receive, send):
        close_old_connections()
        # token_key = scope['query_string'].decode().split('=')[-1]
        try:
            token_key = (dict((x.split('=') for x in scope['query_string'].decode().split("&")))).get('token', None)
        except ValueError:
            token_key = None
        # try:
        #     token_key = dict(scope['headers'])[b'sec-websocket-protocol'].decode('utf-8')
        #     print('d1', token_key)
        # except ValueError:
        #     token_key = None

        scope['user'] = await get_user(token_key)
        print('d2', scope['user'])
        return await super().__call__(scope, receive, send)


def JwtAuthMiddlewareStack(inner):
    return TokenAuthMiddleware(inner)
