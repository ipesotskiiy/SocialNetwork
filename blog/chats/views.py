from django.db.models import Q

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

from chats.models import Chat
from chats.serializers import ChatSerializer, ChatListSerializer


class StartChatView(APIView):
    def post(self, request, format=None):
        serializer = ChatSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class GetChatView(APIView):
    def get(self, request, chat_id):
        conversation = Chat.objects.filter(id=chat_id)
        if not conversation.exists():
            return Response({'message': 'Chat does not exist'})
        else:
            serializer = ChatSerializer(instance=conversation[0])
            return Response(serializer.data)


class ChatsView(APIView):
    def get(self, request):
        chat_list = Chat.objects.filter(Q(user=request.user) | Q(companion=request.user))
        serializer = ChatListSerializer(instance=chat_list, many=True)
        return Response(serializer.data)

# @api_view(['GET'])
# def get_chat(request, chat_id):
#     conversation = Chat.objects.filter(id=chat_id)
#     if not conversation.exists():
#         return Response({'message': 'Chat does not exist'})
#     else:
#         serializer = ChatSerializer(instance=conversation[0])
#         return Response(serializer.data)
#
#
# @api_view(['GET'])
# def chats(request):
#     chat_list = Chat.objects.filter(Q(user=request.user) |
#                                     Q(companion=request.user))
#     serializer = ChatListSerializer(instance=chat_list, many=True)
#     return Response(serializer.data)
