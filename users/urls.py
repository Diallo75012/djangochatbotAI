from django.urls import path, include
from . import views


app_name = 'users'

urlpatterns = [
  # business user
  path('registerbusinessuser', views.registerBusinessUser, name='registerbusinessuser'),
  path('loginbusinessuser', views.loginBusinessUser, name='loginbusinessuser'),
  path('logoutbusinessuser', views.logoutBusinessUser, name='logoutbusinessuser'),
  path('updatebusinessuser', views.updateBusinessUser, name='updatebusinessuser'),

  # client user
  path('clientuserchat', views.clientUserChat, name='clientuserchat'),
  path('registerclientuser', views.registerClientUser, name='registerclientuser'),
  path('loginclientuser', views.loginClientUser, name='loginclientuser'),
  path('logoutclientuser', views.logoutClientUser, name='logoutclientuser'),
  path('updateclientuser', views.updateClientUser, name='updateclientuser'),
  # path('clientusersettings', views.clientUserSettings, name='clientusersettings'),
]

