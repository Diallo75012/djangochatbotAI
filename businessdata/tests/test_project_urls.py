# tests/test_project_urls.py

import pytest
from django.urls import reverse, resolve
from django.urls import include
from chatbotAI import urls  # Assuming your project is named chatbotAI


@pytest.mark.parametrize("url_name, expected_url_pattern", [
  ('admin:index', 'admin/'),  # Test for the admin URL
  ('users:index', 'users/index'),  # Test for users app URLs
])
def test_project_url_patterns(url_name, expected_url_pattern):
  """
  Ensure URLs in the main urls.py are properly included.
  """
  try:
    url = reverse(url_name)
    assert expected_url_pattern in url
  except Exception as e:
    pytest.fail(f"URL reverse failed for {url_name}: {e}")
