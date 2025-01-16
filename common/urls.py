from django.urls import path
from . import views


app_name = 'common'

urlpatterns = [
    path('runloganalyzer', views.runLogAnalyzer, name='runloganalyzer'),
]
