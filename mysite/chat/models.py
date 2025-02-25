from django.db import models
from django.utils import timezone
from register_user.models import UserProfile


class Chat(models.Model):
    """Модель личного чата между двумя пользователями"""
    user1 = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name="chats_as_user1")
    user2 = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name="chats_as_user2")
    created_at = models.DateTimeField(auto_now_add=True)
    last_message_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['user1', 'user2']  # Уникальность чатов
        ordering = ['-last_message_at']  # Сортировка чатов по времени последнего сообщения

    def __str__(self):
        return f"Chat between {self.user1.user.username} and {self.user2.user.username}"

    @property
    def get_last_message(self):
        """Получить последнее сообщение в чате"""
        return self.messages.order_by('-timestamp').first()

    def mark_all_as_read(self, user):
        """Отметить все сообщения как прочитанные для указанного пользователя"""
        unread_messages = self.messages.filter(is_read=False).exclude(sender=user.profile)
        unread_messages.update(is_read=True, read_at=timezone.now())
        return unread_messages.count()

    def get_unread_count(self, user):
        """Получить количество непрочитанных сообщений для пользователя"""
        return self.messages.filter(is_read=False).exclude(sender=user.profile).count()

    @classmethod
    def get_or_create_chat(cls, user1, user2):
        """Получить существующий чат или создать новый между двумя пользователями"""
        # Проверяем существование чата в обоих направлениях
        chat = cls.objects.filter(
            models.Q(user1=user1, user2=user2) |
            models.Q(user1=user2, user2=user1)
        ).first()

        if not chat:
            chat = cls.objects.create(user1=user1, user2=user2)

        return chat


class Message(models.Model):
    """Модель сообщений в чате"""
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE, related_name="messages")
    sender = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name="sent_messages")
    text = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to="chat_images/", blank=True, null=True)
    video = models.FileField(upload_to="chat_videos/", blank=True, null=True)
    audio = models.FileField(upload_to="chat_audio/", blank=True, null=True)
    sticker = models.CharField(max_length=100, blank=True, null=True)  # Стикеры как в Instagram
    is_read = models.BooleanField(default=False)
    read_at = models.DateTimeField(null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    # Флаги для специальных типов сообщений
    is_story_reply = models.BooleanField(default=False)
    story_id = models.IntegerField(null=True, blank=True)
    is_post_share = models.BooleanField(default=False)
    post_id = models.IntegerField(null=True, blank=True)
    # Для instagram-специфичных функций
    is_disappearing = models.BooleanField(default=False)  # Исчезающие сообщения
    expire_at = models.DateTimeField(null=True, blank=True)
    is_liked = models.BooleanField(default=False)  # Лайк на сообщение (сердечко)

    class Meta:
        ordering = ['timestamp']

    def __str__(self):
        return f"Message from {self.sender.user.username} in chat {self.chat.id}"

    def mark_as_read(self):
        """Отметить сообщение как прочитанное"""
        if not self.is_read:
            self.is_read = True
            self.read_at = timezone.now()
            self.save()

    def like(self):
        """Поставить лайк на сообщение"""
        self.is_liked = True
        self.save()

    def unlike(self):
        """Убрать лайк с сообщения"""
        self.is_liked = False
        self.save()

    @property
    def is_expired(self):
        """Проверить, истекло ли исчезающее сообщение"""
        if self.is_disappearing and self.expire_at:
            return timezone.now() > self.expire_at
        return False


class ChatNotification(models.Model):
    """Модель для уведомлений о сообщениях"""
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name="chat_notifications")
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE)
    message = models.ForeignKey(Message, on_delete=models.CASCADE)
    is_seen = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Notification for {self.user.user.username} in chat {self.chat.id}"