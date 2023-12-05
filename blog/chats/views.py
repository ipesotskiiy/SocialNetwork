from django.db.models import Q
from django.shortcuts import render, redirect, reverse

from rest_framework.decorators import api_view
from rest_framework.response import Response

from chats.models import Chat
from chats.serializers import ChatSerializer, ChatListSerializer
from users.models import User


@api_view(['POST'])
def start_chat(request, ):
    data = request.data
    login = data.pop('login')
    try:
        participant = User.objects.get(login=login)
    except User.DoesNotExist:
        return Response({'message': 'You cannot chat with a non existent user'})

    chat = Chat.objects.filter(Q(user=request.user, companion=participant)
                               | Q(user=participant, companion=request.user))

    if chat.exists():
        return redirect(reverse('get_chat', args=(chat[0].id,)))

    else:
        chat = Chat.objects.create(user=request.user, companion=participant)
        return Response(ChatSerializer(instance=chat).data)


@api_view(['GET'])
def get_chat(request, chat_id):
    chat = Chat.objects.get(id=chat_id)
    if not chat.exists():
        return Response({'message': 'Chat does not exist'})
    else:
        serializer = ChatSerializer(instance=chat[0])
        return Response(serializer.data)


@api_view(['GET'])
def get_all_user_chats(request):
    chats_list = Chat.objects.filter(Q(user=request.user)
                                     | Q(companion= request.user))
    serializer = ChatListSerializer(instance=chats_list, many=True)
    return Response(serializer.data)
