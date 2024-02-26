from rest_framework import serializers
#
from chats.models import Message, Chat
from users.models import User
from users.serializers import UserSerializer, CompanionSerializer


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
    user = CompanionSerializer()
    companion = CompanionSerializer()
    message_set = MessageSerializer(many=True)

    def create(self, validated_data):
        user_login = validated_data['user']['login']
        # Получить или создать объект User на основе user_login
        user, created = User.objects.get_or_create(login=user_login)
        companion_login = validated_data['companion']['login']
        companion, created = User.objects.get_or_create(login=companion_login)
        messages_data = validated_data.get('message_set', [])  # Получаем сообщения из данных
        chat = Chat.objects.create(user=user,
                                   companion=companion)
        for message_data in messages_data:
            # Создаем объект сообщения и связываем с чатом
            Message.objects.create(chat=chat, **message_data)
        return chat

    class Meta:
        model = Chat
        fields = ('user', 'companion', 'message_set')
