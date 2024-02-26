from django.urls import path

from chats.views import get_chat, chats, StartChatView

urlpatterns = [
    path('start/', StartChatView.as_view(), name='start_chat'),
    path('<int:chat_id>/', get_chat, name='get_chat'),
    path('', chats, name='chat')
]