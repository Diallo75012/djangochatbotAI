from django.db import models
# django built-in User model
from django.contrib.auth.models import User
from chatbotsettings.models import ChatBotSettings


class ClientUser(models.Model):
  user = models.ForeignKey(
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
  preferred_chatbot = models.ForeignKey(
    ChatBotSettings,
    null=True,
    blank=True,
    on_delete=models.SET_NULL
  )

  def __str__(self):
    return f"{self.nickname}: {self.bio[:50]}..."




