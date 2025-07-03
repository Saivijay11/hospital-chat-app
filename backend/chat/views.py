from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from users.models import CustomUser
from .models import Thread, Message
from .serializers import MessageSerializer
from django.db.models import Q


class MarkMessagesAsReadView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, username):
        target_user = CustomUser.objects.filter(username__iexact=username).first()
        if not target_user:
            return Response({"detail": "User not found"}, status=404)

        thread = Thread.get_or_create_thread(request.user, target_user)
        Message.objects.filter(thread=thread, is_read=False).exclude(sender=request.user).update(is_read=True)
        return Response({"detail": "Marked as read"})

class MessageHistoryView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, username):
        target_user = CustomUser.objects.filter(username__iexact=username).first()
        if not target_user:
            return Response({"detail": "User not found"}, status=404)

        thread = Thread.get_or_create_thread(request.user, target_user)
        messages = thread.messages.order_by('timestamp')
        return Response(MessageSerializer(messages, many=True).data)
    
class UnreadMessageCountView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        threads = Thread.objects.filter(Q(doctor=user) | Q(patient=user))

        counts = {}
        for thread in threads:
            unread = Message.objects.filter(thread=thread, is_read=False).exclude(sender=user)
            if unread.exists():
                sender = unread.last().sender.username
                counts[sender] = unread.count()

        return Response(counts)

    
class MarkMessagesAsReadView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, username):
        target_user = CustomUser.objects.filter(username__iexact=username).first()
        if not target_user:
            return Response({"detail": "User not found"}, status=404)

        thread = Thread.get_or_create_thread(request.user, target_user)
        Message.objects.filter(thread=thread, is_read=False).exclude(sender=request.user).update(is_read=True)
        return Response({"detail": "Marked as read"})
