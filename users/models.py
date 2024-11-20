from django.db import models
# django built-in User model
from django.contrib.auth.models import User


# no custom User model but use it directly in our first model
class BusinessUserData(models.Model):
  user = models.ForeignKey(
    User,
    null=True,
    on_delete=models.CASCADE
  )
  document_title = models.CharField(max_length=255, unique=True)
  question_answer_data = models.JSONField()


  def __str__(self):
    return f"{self.document_title}: {self.question_answer_data}"
