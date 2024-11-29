from django.urls import path
from . import views


app_name = 'chatbotsettings'

urlpatterns = [
  path('addchatbotsettings', views.addChatBotSettings, name='addchatbotsettings'),
  path('updatechatbotsettings/<int:pk>/', views.updateChatBotSettings, name='updatechatbotsettings'),
  path('deletechatbotsettings/<int:pk>/', views.deleteChatBotSettings, name='deletechatbotsettings'),
  path('chatbotsettingsmanagement', views.ChatBotSettingsManagement, name='chatbotsettingsmanagement'),

  # route for Ajax frontend to have access to chatbotsettings details for user webui dynamic change when user picks a chatbot
  path('chatbotdetails/<int:chatbot_id>/', views.getChatbotDetails, name='getchatbotdetails'),
]
