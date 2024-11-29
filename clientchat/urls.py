from django.urls import path, include
from . import views


app_name = 'clientchat'

urlpatterns = [
  path('clientuserchat', views.clientUserChat, name='clientuserchat'),
]
