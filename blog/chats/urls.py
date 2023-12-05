from django.urls import path

from chats import views

urlpatterns = [
    path('start/', views.start_chat, name='start_chat'),
    path('<int:chat_id/', views.get_chat, name='get_chat'),
    path('', views.get_all_user_chats, name='get_all_user_chats')
]