from django.urls import path

from chats.views import GetChatView, ChatsView, StartChatView

urlpatterns = [
    path('start/', StartChatView.as_view(), name='start_chat'),
    path('<int:chat_id>/', GetChatView.as_view(), name='get_chat'),
    path('', ChatsView.as_view(), name='chat')
]