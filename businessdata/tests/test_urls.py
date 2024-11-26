import pytest
from django.urls import reverse, resolve
from users import views


# Test URLs
@pytest.mark.parametrize("url_name, view_name", [
  ('users:registeruser', views.registerUser),
  ('users:loginuser', views.loginUser),
  ('users:logoutuser', views.logoutUser),
  ('users:updateuser', views.updateUser),
  ('users:addbusinessdata', views.addBusinessData),
  ('users:index', views.index),
])
@pytest.mark.django_db
def test_url_resolves_to_correct_view(url_name, view_name):
  """
  Ensure each URL resolves to the correct view.
  """
  url = reverse(url_name)
  resolver = resolve(url)
  assert resolver.func == view_name


@pytest.mark.parametrize("url_name, view_name, kwargs", [
  ('users:updatebusinessdata', views.updateBusinessData, {'pk': 1}),
  ('users:deletebusinessdata', views.deleteBusinessData, {'pk': 1}),
])
@pytest.mark.django_db
def test_url_with_kwargs_resolves_to_correct_view(url_name, view_name, kwargs):
  """
  Ensure URLs with arguments resolve to the correct views.
  """
  url = reverse(url_name, kwargs=kwargs)
  resolver = resolve(url)
  assert resolver.func == view_name
