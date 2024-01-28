from django.urls import path

from chats.views import get_chat, get_all_user_chats, CreateChatView

urlpatterns = [
    path('start/', CreateChatView.as_view(), name='start_chat'),
    path('<int:chat_id/', get_chat, name='get_chat'),
    path('', get_all_user_chats, name='get_all_user_chats')
]