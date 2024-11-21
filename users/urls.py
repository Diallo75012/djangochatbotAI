from django.urls import path, include
from . import views
from . import viewsets
# FOR API
from rest_framework import routers

# FOR API
# wiring up with automatic routing URLS
router = routers.DefaultRouter()
router.register(r'users', viewsets.UserViewSet)
router.register(r'groups', viewsets.GroupViewSet)


app_name = 'users'

urlpatterns = [
  # user
  path('registeruser', views.registerUser, name='registeruser'),
  path('loginuser', views.loginUser, name='loginuser'),
  path('logoutuser', views.logoutUser, name='logoutuser'),
  path('updateuser', views.updateUser, name='updateuser'),

  # business data that will be later moved to its own application
  path('addbusinessdata', views.addBusinessData, name='addbusinessdata'),
  path('updatebusinessdata/<int:pk>/', views.updateBusinessData, name='updatebusinessdata'),
  path('deletebusinessdata/<int:pk>/', views.deleteBusinessData, name='deletebusinessdata'),

  # index
  path('index', views.index, name='index'),

  # FOR API
  path('', include(router.urls)),
]

