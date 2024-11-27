from django.db import models
from django.contrib.auth.models import User


class ChatBotSettings(models.Model):
  business_user = models.ForeignKey(
    User,
    null=True,
    on_delete=models.CASCADE
  )
  name = models.CharField(max_length=40, unique=True)
  tone = models.CharField(max_length=40, blank=True)
  description = models.CharField(max_length=150, blank=True)
  expertise = models.CharField(max_length=100, blank=True)
  custom_greeting = models.CharField(max_length=100, blank=True)
  example_of_response = models.CharField(max_length=400, blank=True)
  origin = models.CharField(max_length=100, blank=True)
  age = models.IntegerField(default=18)
  dream = models.CharField(max_length=100, blank=True)
  # better than FileField as it validates if File is Image
  # file will be uploaded to MEDIA_ROOT/uploads
  avatar = models.ImageField(
    max_length=255,
    upload_to="uploads/chatbotsettings/",
    blank=True,
  )

  def __str__(self):
    return f"{self.name}: {self.description[:50]}..."

  # this overrides the Django native delete() method
  # it deletes the avatar if any then the instance
  def delete(self, *args, **kwargs):
    # Delete the avatar file if it exists
    if self.avatar:
      avatar_path = os.path.join(settings.MEDIA_ROOT, self.avatar.name)
      if os.path.isfile(avatar_path):
        os.remove(avatar_path)
    # Call the superclass delete method to delete the model instance
    super().delete(*args, **kwargs)
