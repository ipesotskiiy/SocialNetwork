from channels.db import database_sync_to_async
from django.contrib.auth.models import AnonymousUser
from rest_framework_simplejwt.exceptions import InvalidToken
from rest_framework_simplejwt.tokens import AccessToken, TokenError
from channels.middleware import BaseMiddleware

from users.models import User



@database_sync_to_async
def get_user(user_id):
    try:
        return User.objects.get(id=user_id)
    except User.DoesNotExist:
        return AnonymousUser()


class TokenAuthMiddleware(BaseMiddleware):
    def __call__(self, scope, receive, send):
        token = self.get_token_from_scope(scope)
        user =  self.get_user_from_token(token)
        scope['user'] = user
        return super().__call__(scope, receive, send)

    def get_token_from_scope(self, scope):
        headers = dict(scope["headers"])
        authorization_header = headers.get(b'authorization')
        if authorization_header:
            auth_header = authorization_header.decode('utf-8')
            parts = auth_header.split()
            if len(parts) == 2 and parts[0].lower() == "bearer":
                return parts[1]
        return None

    def get_user_from_token(self, token):
        try:
            access_token = AccessToken(token)
            user_id = access_token.payload.get('user_id')
            return user_id
        except InvalidToken as e:
            print("InvalidToken:", e)
            return None
        except TokenError as e:
            print("TokenError:", e)
            return None
