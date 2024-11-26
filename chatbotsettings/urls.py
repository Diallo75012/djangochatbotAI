from django.urls import path
from . import views


app_name = 'chatbotsettings'

urlpatterns = [
  path('chatbotsettingsview', views.chatbotSettingsView, name="chatbotsettingsview"),
]

