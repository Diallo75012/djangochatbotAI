from django.urls import path
from . import views


app_name = 'chatbotsettings'

urlpatterns = [
  path('addchatbotsettings', views.addChatBotSettings, name='addchatbotsettings'),
  path('updatechatbotsettings/<int:pk>/', views.updateChatBotSettings, name='updatechatbotsettings'),
  path('deletechatbotsettings/<int:pk>/', views.deleteChatBotSettings, name='deletechatbotsettings'),
  path('chatbotsettingsmanagement', views.ChatBotSettingsManagement, name='chatbotsettingsmanagement'),
]
