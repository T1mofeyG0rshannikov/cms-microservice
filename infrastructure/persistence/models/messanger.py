from django.db import models

from infrastructure.persistence.models.user.user import User


class Chat(models.Model):
    class Meta:
        app_label = "messanger"


class ChatUser(models.Model):
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE, related_name="chat_users")
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="chat_users")

    class Meta:
        app_label = "messanger"


class Message(models.Model):
    chat_user = models.ForeignKey(ChatUser, on_delete=models.CASCADE, related_name="messages")
    text = models.TextField(max_length=300, null=True)
    time = models.DateTimeField(auto_now_add=True, verbose_name="")
    readen = models.BooleanField(default=False)

    class Meta:
        app_label = "messanger"
        ordering = ["time"]
