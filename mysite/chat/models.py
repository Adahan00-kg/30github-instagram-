from django.db import models
from register_user.models import UserProfile


class Chat(models.Model):
    """Модель личного чата между двумя пользователями"""
    user1 = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name="chats_as_user1")
    user2 = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name="chats_as_user2")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['user1', 'user2']  # Уникальность чатов (чтобы чат между двумя пользователями был один)

    def __str__(self):
        return f"Chat between {self.user1} and {self.user2}"

class Message(models.Model):
    """Модель сообщений в чате"""
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE, related_name="messages")
    sender = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    text = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to="chat_images/", blank=True, null=True)
    is_read = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Message from {self.sender} in chat {self.chat.id}"
