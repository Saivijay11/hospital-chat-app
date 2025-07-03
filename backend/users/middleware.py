import jwt
from django.conf import settings
from users.models import CustomUser
from urllib.parse import parse_qs
from channels.middleware import BaseMiddleware
from asgiref.sync import sync_to_async

@sync_to_async
def get_user(token):
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
        return CustomUser.objects.get(id=payload["user_id"])
    except:
        return None

class JWTAuthMiddleware(BaseMiddleware):
    def __init__(self, inner):
        super().__init__(inner)

    async def __call__(self, scope, receive, send):
        query_string = parse_qs(scope["query_string"].decode())
        token = query_string.get("token", [None])[0]
        if token:
            scope["user"] = await get_user(token)
        else:
            scope["user"] = None
        return await super().__call__(scope, receive, send)
