import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from users.models import CustomUser
from .models import Thread, Message


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.target_username = self.scope['url_route']['kwargs']['username']
        self.user = self.scope['user']
        self.thread = await self.get_thread(self.user.username, self.target_username)
        self.room_name = f"chat_{self.thread.id}"

        await self.channel_layer.group_add(
            self.room_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_name,
            self.channel_name
        )

    async def receive(self, text_data):
        data = json.loads(text_data)
        message = data['message']
        msg = await self.save_message(self.user, message)

        await self.channel_layer.group_send(
            self.room_name,
        {
            'type': 'chat_message',
            'message': message,
            'sender': self.user.username,
            'timestamp': msg.timestamp.strftime("%I:%M:%S %p")
        }
    )

    async def chat_message(self, event):
        await self.send(text_data=json.dumps(event))

    @database_sync_to_async
    def get_thread(self, user1, user2):
        u1 = CustomUser.objects.get(username=user1)
        u2 = CustomUser.objects.get(username=user2)
        return Thread.get_or_create_thread(u1, u2)

    @database_sync_to_async
    def save_message(self, sender, message):
        return Message.objects.create(thread=self.thread, sender=sender, content=message)
