from django.urls import path, include
from . import views


app_name = 'users'

urlpatterns = [
  # user
  path('registerbusinessuser', views.registerBusinessUser, name='registerbusinessuser'),
  path('loginbusinessuser', views.loginBusinessUser, name='loginbusinessuser'),
  path('logoutbusinessuser', views.logoutBusinessUser, name='logoutbusinessuser'),
  path('updatebusinessuser', views.updateBusinessUser, name='updatebusinessuser'),

]

