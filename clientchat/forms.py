from django.forms import ModelForm
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django import forms
from .models import ChatMessages


# client user chat form
class ClientUserChatForm(forms.ModelForm):
  class Meta:
    model = ChatMessages
    fields = ["content"]
    labels = {
      "Content": "Enter your message",
    }
