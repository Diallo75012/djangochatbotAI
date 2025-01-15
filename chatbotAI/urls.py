from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
  path('admin/', admin.site.urls),
  path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
  # path for other apps
  path('users/', include('users.urls')),
  path('businessdata/', include('businessdata.urls')),
  path('chatbotsettings/', include('chatbotsettings.urls')),
  path('clientchat/', include('clientchat.urls')),
  path('agents/', include('agents.urls')),
  path('common/', include('common.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
