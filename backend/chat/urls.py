from django.urls import path
from .views import MessageHistoryView
from .views import UnreadMessageCountView
from .views import MarkMessagesAsReadView

urlpatterns = [
path("history/<str:username>/", MessageHistoryView.as_view(), name="chat-history"),
path("unread-counts/", UnreadMessageCountView.as_view(), name="unread-counts"),
path("mark-read/<str:username>/", MarkMessagesAsReadView.as_view(), name="mark-read")
]
