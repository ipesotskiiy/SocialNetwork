from rest_framework import serializers

from chats.models import Message, Chat
from users.serializers import UserSerializer


class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        exclude = ('chat',)


class ChatListSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    companion = UserSerializer()
    last_message = serializers.SerializerMethodField()

    class Meta:
        model = Chat
        field = ('user', 'companion', 'last_message')

    def get_last_message(self, instance):
        message = instance.message_set.first()
        return MessageSerializer(instance=message)


class ChatSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    companion = UserSerializer()
    message_set = MessageSerializer(many=True)

    class Meta:
        model = Chat
        fields = ('user', 'companion', 'message_set')
