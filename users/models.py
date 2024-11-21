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
  # can also override here Django built-in error message
  # for invalid JSON and use your custom one instead of "Enter a valid JSON"
  # question_answer_data = models.JSONField(error_messages={
    # use this message for unti tests of views.py functions
    #'invalid': "Invalid JSON format. Please enter valid JSON data"
  #})


  def __str__(self):
    return f"{self.document_title}: {self.question_answer_data}"
