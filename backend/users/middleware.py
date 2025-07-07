import jwt
from django.conf import settings
from users.models import CustomUser
from urllib.parse import parse_qs
from channels.middleware import BaseMiddleware
from asgiref.sync import sync_to_async

#retrieving user based on token by using async function
@sync_to_async
def get_user(token):
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"]) #decoding jwt using the secret key of the project
        return CustomUser.objects.get(id=payload["user_id"]) # fetching the user by id from the token 
    except:
        return None #if token invaild or not there

class JWTAuthMiddleware(BaseMiddleware): 
    def __init__(self, inner):
        super().__init__(inner)

    async def __call__(self, scope, receive, send): #it is called on every websocket connection
        query_string = parse_qs(scope["query_string"].decode()) #parsing the query from the websocket connection
        token = query_string.get("token", [None])[0] # token is extracted fromt he query
        if token:
            scope["user"] = await get_user(token) #so authenticated here for the user usinf the provided data, if no token user is anonymous
        else:
            scope["user"] = None
        return await super().__call__(scope, receive, send) # control to the inner consumer with user info