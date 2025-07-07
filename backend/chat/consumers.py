import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from users.models import CustomUser
from .models import Thread, Message

# This is my main WebSocket consumer for handling chat between users
class ChatConsumer(AsyncWebsocketConsumer):

    # This runs when a user connects to the WebSocket like you can say opening a chat page 
    async def connect(self):
        # gets the username of the person who we are chatting from the url
        self.target_username = self.scope['url_route']['kwargs']['username']

        # so took help of jwt middleware to store the logged in user in the websocket scope
        self.user = self.scope['user']

        # Get or create a chat thread between the two users
        self.thread = await self.get_thread(self.user.username, self.target_username)

        # Generate a unique room name using the thread ID
        self.room_name = f"chat_{self.thread.id}"

        # Add the current socket connection to this room group
        await self.channel_layer.group_add(
            self.room_name,
            self.channel_name
        )

        # accepts the connection which is req to complete the socket connection or else handshakle
        await self.accept()

    # initialized when connection is closed
    async def disconnect(self, close_code):
        #removes the connection from the group
        await self.channel_layer.group_discard(
            self.room_name,
            self.channel_name
        )

    # This runs every time the client sends a message through the socket
    async def receive(self, text_data):
        # Convert the incoming message into a Python dict
        data = json.loads(text_data)
        message = data['message']

        # Save the message to the database 
        msg = await self.save_message(self.user, message)

        # Broadcast the message to everyone else in the same room (including self)
        await self.channel_layer.group_send(
            self.room_name,
            {
                'type': 'chat_message',  # Triggers the chat_message handler below
                'message': message,
                'sender': self.user.username,
                'timestamp': msg.timestamp.strftime("%I:%M:%S %p")  # for formatting
            }
        )

    # This handles incoming messages sent to the group
    async def chat_message(self, event):
        # Just send the message back to the frontend as JSON
        await self.send(text_data=json.dumps(event))

    # this method checks or will create a new thread obj which is chat room bw 2 users
    @database_sync_to_async
    def get_thread(self, user1, user2):
        u1 = CustomUser.objects.get(username=user1)
        u2 = CustomUser.objects.get(username=user2)
        return Thread.get_or_create_thread(u1, u2)

    # This creates a new Message entry in the DB for the chat 
    @database_sync_to_async
    def save_message(self, sender, message):
        return Message.objects.create(thread=self.thread, sender=sender, content=message)
