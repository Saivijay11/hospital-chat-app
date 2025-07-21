import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from users.models import CustomUser
from .models import Thread, Message

class ChatConsumer(AsyncWebsocketConsumer):
    """
    Handles WebSocket chat communication between users.
    """

    async def connect(self):
        # Extract target username from URL
        self.target_username = self.scope['url_route']['kwargs']['username']

        # Get the currently authenticated user from JWT scope
        self.user = self.scope['user']

        # Reject unauthenticated users (extra production safety)
        if not self.user.is_authenticated:
            await self.close()
            return

        # Get or create thread (chat room) between self and target user
        self.thread = await self.get_thread(self.user.username, self.target_username)

        # Define room name using thread ID
        self.room_name = f"chat_{self.thread.id}"

        # Join the channel group (room)
        await self.channel_layer.group_add(
            self.room_name,
            self.channel_name
        )

        # Accept WebSocket connection
        await self.accept()

    async def disconnect(self, close_code):
        # Leave the group when the socket disconnects
        await self.channel_layer.group_discard(
            self.room_name,
            self.channel_name
        )

    async def receive(self, text_data):
        """
        Triggered when the client sends a message over WebSocket.
        """
        data = json.loads(text_data)
        raw_message = data.get('message', '').strip()

        if not raw_message:
            return  # Skip empty messages

        # Optional: Add prefix or tracking
        message = f"{raw_message}"

        # Save message to DB
        msg_obj = await self.save_message(self.user, message)

        # Send message to all connected clients in the room
        await self.channel_layer.group_send(
            self.room_name,
            {
                'type': 'chat_message',
                'message': message,
                'sender': self.user.full_name or self.user.username,
                'timestamp': msg_obj.timestamp.strftime("%I:%M:%S %p"),
            }
        )

    async def chat_message(self, event):
        """
        Called when a message is sent to the group.
        """
        await self.send(text_data=json.dumps(event))

    @database_sync_to_async
    def get_thread(self, username1, username2):
        try:
            u1 = CustomUser.objects.get(username=username1)
            u2 = CustomUser.objects.get(username=username2)
        except CustomUser.DoesNotExist:
            return None  # Optional: handle user not found

        return Thread.get_or_create_thread(u1, u2)

    @database_sync_to_async
    def save_message(self, sender, message):
        return Message.objects.create(thread=self.thread, sender=sender, content=message)
