from django.db import models
from register_user.models import UserProfile

class Chat(models.Model):
    """Модель личного чата между двумя пользователями"""
    user1 = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name="chats_as_user1")
    user2 = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name="chats_as_user2")
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Чат {self.user1} и {self.user2}"


class Message(models.Model):
    """Сообщение в чате"""
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE, related_name='messages')
    author = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    text = models.CharField(max_length=355, null=True, blank=True)
    image = models.ImageField(upload_to='message_image', null=True, blank=True)
    video = models.FileField(upload_to='message_video', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Сообщение от {self.author} в чате {self.chat.id}"
