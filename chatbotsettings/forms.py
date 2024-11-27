from django.forms import ModelForm
from .models import ChatBotSettings
from django.contrib.auth.models import User


# ChatBotSetting record form
class ChatBotSettingsForm(ModelForm):
  class Meta:
    model = ChatBotSettings
    fields = [
      'name', 'tone', 'description', 'expertise', 'custom_greeting', 'example_of_response', 'origin', 'age', 'dream', 'avatar',
    ]
    labels = {
      'name': 'Bot name',
      'tone': 'Tone of voice',
      'description': 'Bot description',
      'expertise': 'Expert in ...',
      'custom_greeting': 'How should the Bot greets?',
      'example_of_response': 'Optional example of response',
      'origin': 'Where is the Bot from?',
      'age': 'How old is the Bot?',
      'dream': 'What is the Bot dreaming of?',
       'avatar': 'Bot logo or picture',
    }

# ChatBotSettings Update data records
class ChatBotSettingsUpdateForm(ModelForm):
  class Meta:
    model = ChatBotSettings
    fields = [
      'name', 'tone', 'description', 'expertise', 'custom_greeting', 'example_of_response', 'origin', 'age', 'dream', 'avatar',
    ]
    labels = {
      'name': 'Bot name',
      'tone': 'Tone of voice',
      'description': 'Bot description',
      'expertise': 'Expert in ...',
      'custom_greeting': 'How should the Bot greets?',
      'example_of_response': 'Optional example of response',
      'origin': 'Where is the Bot from?',
      'age': 'How old is the Bot?',
      'dream': 'What is the Bot dreaming of?',
       'avatar': 'Bot logo or picture',
    }
