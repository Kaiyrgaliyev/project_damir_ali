from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django import forms
from django.contrib.auth.decorators import login_required

class LogMessage(models.Model):
    message = models.TextField()
    log_date = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='log_images/', blank=True, null=True)  # Поле для изображения

    def __str__(self):
        return self.message[:50]
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
