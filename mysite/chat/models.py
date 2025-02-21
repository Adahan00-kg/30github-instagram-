from django.contrib.auth.models import AbstractUser
from django.db import models


class UserProfile(AbstractUser):
    bio = models.TextField(null=True, blank=True)
    image = models.ImageField(upload_to='user_image', null=True, blank=True)
    website = models.URLField(null=True, blank=True)

    def str(self):
        return self.username


class Group(models.Model):
    group_name = models.CharField(max_length=150)


class Chat(models.Model):
    person = models.ManyToManyField(UserProfile)
    created_date = models.DateField(auto_now_add=True)


class Message(models.Model):
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE, related_name='message')
    author = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    text = models.CharField(max_length=355, null=True, blank=True)
    image = models.ImageField(upload_to='message_image', null=True, blank=True)
    video = models.FileField(upload_to='message_video', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

