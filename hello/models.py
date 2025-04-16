from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

class LogMessage(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Добавляем связь с пользователе
    message = models.CharField(max_length=300)
    log_date = models.DateTimeField("date logged", default=timezone.now)  # Добавлено значение по умолчанию

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