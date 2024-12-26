import threading
from django.utils.deprecation import MiddlewareMixin  # For Django middleware
from django.http import HttpRequest


_user = threading.local()

class CurrentUserMiddleware:
  def __init__(self, get_response):
    self.get_response = get_response

  def __call__(self, request):
    # Set the current user
    _user.value = getattr(request, 'user', None)
    response = self.get_response(request)
    # Clear the current user after the response
    _user.value = None
    return response

def get_current_user():
  return getattr(_user, 'value', None)
