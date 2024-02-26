from django.db.models import Q
from django.shortcuts import render, redirect, reverse

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

from chats.models import Chat
from chats.serializers import ChatSerializer, ChatListSerializer
from users.models import User


# @api_view(['POST'])
# def start_chat(request, ):
#     data = request.data
#     login = data.pop('login')
#     try:
#         participant = User.objects.get(login=login)
#     except User.DoesNotExist:
#         return Response({'message': 'You cannot chat with a non existent user'})
#
#     conversation = Chat.objects.filter(Q(user=request.user, companion=participant) |
#                                                Q(user=participant, companion=request.user))
#     if conversation.exists():
#         return redirect(reverse('get_chat', args=(conversation[0].id,)))
#     else:
#         conversation = Chat.objects.create(user=request.user, companion=participant)
#         return Response(ChatSerializer(instance=conversation).data)

class StartChatView(APIView):
    def post(self, request, format=None):
        # Создание и валидация сериализатора
        serializer = ChatSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            # Обработка случая, когда данные не валидны
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def get_chat(request, chat_id):
    conversation = Chat.objects.filter(id=chat_id)
    if not conversation.exists():
        return Response({'message': 'Chat does not exist'})
    else:
        serializer = ChatSerializer(instance=conversation[0])
        return Response(serializer.data)


@api_view(['GET'])
def chats(request):
    chat_list = Chat.objects.filter(Q(user=request.user) |
                                                    Q(companion=request.user))
    serializer = ChatListSerializer(instance=chat_list, many=True)
    return Response(serializer.data)
