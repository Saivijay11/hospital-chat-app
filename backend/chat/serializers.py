from rest_framework import serializers
from .models import Message
from users.models import CustomUser

class MessageSerializer(serializers.ModelSerializer):
    sender_username = serializers.CharField(source='sender.username', read_only=True)

    class Meta:
        model = Message
        fields = ['id', 'sender_username', 'content', 'timestamp', 'is_read']