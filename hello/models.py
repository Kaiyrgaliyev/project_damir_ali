from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

class LogMessage(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Добавляем связь с пользователе
    message = models.CharField(max_length=300)
    log_date = models.DateTimeField("date logged", default=timezone.now)  # Добавлено значение по умолчанию

    image = models.ImageField(upload_to='message_images/', blank=True, null=True)
    video = models.FileField(upload_to='message_videos/', blank=True, null=True)
    # Для внешних видео (например, YouTube)
    video_url = models.URLField(blank=True, null=True)

    def __str__(self):
        """Returns a string representation of a message."""
        date = timezone.localtime(self.log_date)
        return f"'{self.message}' logged on {date.strftime('%A, %d %B, %Y at %X')}"

class ChatMessage(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_messages')
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"From {self.sender} to {self.recipient}: {self.content[:20]}"
    
class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name
    
class Ad(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    is_promoted = models.BooleanField(default=False)  # Новое поле
    created_at = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to='ads/', blank=True, null=True)

    def __str__(self):
        return self.title
    
class Review(models.Model):
    reviewer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='given_reviews')
    reviewed_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_reviews')
    rating = models.PositiveSmallIntegerField()
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Review by {self.reviewer} for {self.reviewed_user}"