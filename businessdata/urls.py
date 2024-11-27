from django.urls import path
from . import views


app_name = 'businessdata'

urlpatterns = [
  path('addbusinessdata', views.addBusinessData, name='addbusinessdata'),
  path('updatebusinessdata/<int:pk>/', views.updateBusinessData, name='updatebusinessdata'),
  path('deletebusinessdata/<int:pk>/', views.deleteBusinessData, name='deletebusinessdata'),
  path('businessdatamanagement', views.businessDataManagement, name='businessdatamanagement'),
]
