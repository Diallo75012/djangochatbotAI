import uuid
from django.db import models
from django.contrib.auth.models import User
from chatbotsettings.models import ChatBotSettings


# no custom User model but use it directly in our first model
class BusinessUserData(models.Model):
  # will skip validation and not be editable and be generated automatically at every record
  # we need this for embedding relation to database eisting data
  # as we want just to embed questions and do similarity search on question
  # from user question, then fetch the answer from the database using the uuid
  # to find the corresponding answer.
  # Need to have LLM that summarize user query to a question form and short
  # Need to have LLM that will check if there is too much deviation from question to answer
  # , unique=False,
  uuid = models.UUIDField(default=uuid.uuid4, editable=False)
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
  chat_bot = models.ForeignKey(
    ChatBotSettings,
    null=True,
    blank=True,
    on_delete=models.SET_NULL
  )

  def __str__(self):
    if self.chat_bot is not None:
      if self.chat_bot.name:
        return f"{self.document_title}: {self.chat_bot.name}"
    else:
      data_length = len(self.question_answer_data)
      return f"Doc: {self.document_title} | Data length: {data_length}"

