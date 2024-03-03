import base64
import secrets

from django.core.files.base import ContentFile

from users.models import User
from .models import Message, Chat
from .serializers import MessageSerializer
from asgiref.sync import sync_to_async

from channels.generic.websocket import AsyncWebsocketConsumer
import json


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = f"chat_{self.room_name}"

        # Присоединение к комнате чата
        await self.channel_layer.group_add(
            self.room_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # Покидание комнаты чата
        await self.channel_layer.group_discard(
            self.room_name,
            self.channel_name
        )

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']

        # Отправка сообщения в комнату чата
        await self.channel_layer.group_send(
            self.room_name,
            {
                'type': 'chat.message',
                'message': message
            }
        )

    async def chat_message(self, event):
        text_data_json = event.copy()
        text_data_json.pop("type")
        message = text_data_json["message"]
        attachment = text_data_json.get("attachment")

        conversation = await sync_to_async(Chat.objects.get)(id=int(self.room_name))

        user_id = self.scope['user']
        sender = await sync_to_async(User.objects.get)(id=user_id)

        if attachment:
            file_str, file_ext = attachment["data"], attachment["format"]
            file_data = ContentFile(base64.b64decode(file_str), name=f"{secrets.token_hex(8)}.{file_ext}")

            _message = await sync_to_async(Message.objects.create)(
                sender=sender, attachment=file_data, text=message, chat=conversation
            )
        else:
            _message = await sync_to_async(Message.objects.create)(
                sender=sender, text=message, chat=conversation
            )

        serializer = MessageSerializer(instance=_message)
        await self.send(text_data=json.dumps(serializer.data))
