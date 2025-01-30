import pytest
from django.urls import reverse, resolve
from users import views

@pytest.mark.parametrize("url_name, view_func", [
    # Business user URLs
    ("users:registerbusinessuser", views.registerBusinessUser),
    ("users:loginbusinessuser", views.loginBusinessUser),
    ("users:logoutbusinessuser", views.logoutBusinessUser),
    ("users:updatebusinessuser", views.updateBusinessUser),
    
    # Client user URLs
    ("users:registerclientuser", views.registerClientUser),
    ("users:loginclientuser", views.loginClientUser),
    ("users:logoutclientuser", views.logoutClientUser),
    ("users:updateclientuser", views.updateClientUser),
])
def test_users_urls(url_name, view_func):
    """Test that all URLs resolve to the correct view functions."""
    url = reverse(url_name)  # Generate URL from its name
    assert resolve(url).func == view_func  # Ensure correct resolution
