from django.db import models
from django.contrib.auth.models import User


class ChatMessages(models.Model):
  MESSAGE_TYPE_CHOICES = [
    ('user', 'User'),
    ('bot', 'Bot')
  ]
  user = models.ForeignKey(
    User,
    null=True,
    on_delete=models.CASCADE
  )
  sender_type = models.CharField(
    max_length=4,
    choices=MESSAGE_TYPE_CHOICES
  )
  nickname = models.CharField(max_length=40)
  content = models.TextField()
  timestamp = models.DateTimeField(auto_now_add=True)

  def __str__(self):
    return f"{self.nickname} ({self.sender_type}): {self.content[:20]}..."
