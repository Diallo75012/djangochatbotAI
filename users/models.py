from django.db import models
# django built-in User model
from django.contrib.auth.models import User
import uuid


class ClientUser(models.Model):
  user = models.OneToOneField(
    User,
    null=True,
    on_delete=models.CASCADE
  )
  nickname = models.CharField(max_length=40)
  picture = models.ImageField(
    max_length=255,
    upload_to="uploads/client_user/",
    blank=True
  )
  bio = models.CharField(max_length=255, blank=True)
  email = models.EmailField(unique=True, blank=True)

  def __str__(self):
    return f"{self.nickname}: {self.bio[:50]}..."


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
