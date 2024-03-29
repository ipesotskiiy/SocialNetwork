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
        fields = ('user', 'companion', 'last_message')

    def get_last_message(self, instance):
        message = instance.message_set.first()
        if message:
            return {
                'id': message.id,
                'text': message.text,
                'sender': message.sender.id,
                'timestamp': message.date_and_time,
                'attachment': message.attachment
            }
        else:
            return None


class ChatSerializer(serializers.ModelSerializer):
    user = CompanionSerializer()
    companion = CompanionSerializer()
    message_set = MessageSerializer(many=True)

    def create(self, validated_data):
        user_login = validated_data['user']['login']
        user, created = User.objects.get_or_create(login=user_login)
        companion_login = validated_data['companion']['login']
        companion, created = User.objects.get_or_create(login=companion_login)

        chat = Chat.objects.create(user=user, companion=companion)

        messages_data = validated_data.pop('message_set', [])

        for message_data in messages_data:
            sender_login = message_data.pop('sender')['login']
            sender, created = User.objects.get_or_create(
                login=sender_login)
            message_data['sender'] = sender
            message = Message.objects.create(chat=chat, **message_data)

        return chat


    class Meta:
        model = Chat
        fields = ('user', 'companion', 'message_set')
