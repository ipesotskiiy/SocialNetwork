from rest_framework import serializers
#
from chats.models import Message, Chat
from users.models import User
from users.serializers import UserSerializer, CompanionSerializer


class MessageSerializer(serializers.ModelSerializer):
    attachment = serializers.FileField(source='message.attachment', required=True, allow_null=True)
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
        last_message = instance.message_set.last()
        if last_message:
            message_data = {
                'id': last_message.id,
                'text': last_message.text,
                'sender': last_message.sender.id,
                'timestamp': last_message.date_and_time,
                'attachment': None
            }
            if last_message.attachment:
                message_data['attachment'] = last_message.attachment.url
            return message_data
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
