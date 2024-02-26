from django.db import models

# Create your models here.
from users.models import User


class Chat(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='chat_starter', null=True)
    companion = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='chat_companion', null=True)
    start_time = models.DateTimeField(auto_now=True)


class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    text = models.CharField(max_length=500, blank=True)
    attachment = models.FileField(blank=True)
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE)
    date_and_time = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('-date_and_time',)
