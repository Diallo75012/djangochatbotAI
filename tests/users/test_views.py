import pytest
from django.contrib.auth.models import User, Group
from django.contrib.messages import get_messages
from django.urls import reverse
from django.test import Client
from users.models import ClientUser


@pytest.mark.django_db
def test_register_business_user(client):
    """Test business user registration view."""
    form_data = {
        "username": "business_user",
        "email": "business@example.com",
        "password1": "SecurePass123!",
        "password2": "SecurePass123!"
    }
    response = client.post(reverse("users:registerbusinessuser"), data=form_data, follow=True)

    assert response.status_code == 200
    assert User.objects.filter(username="business_user").exists()
    assert Group.objects.filter(name="business").exists()

    messages = list(get_messages(response.wsgi_request))
    assert any("Account has been created" in str(msg) for msg in messages)


@pytest.mark.django_db
def test_login_business_user(client):
    """Test login functionality for a business user."""
    user = User.objects.create_user(username="biz_user", password="password123")
    business_group = Group.objects.create(name="business")
    user.groups.add(business_group)

    response = client.post(reverse("users:loginbusinessuser"), data={"username": "biz_user", "password": "password123"}, follow=True)

    assert response.status_code == 200
    assert response.wsgi_request.user.is_authenticated


@pytest.mark.django_db
def test_logout_business_user(client):
    """Test business user logout."""
    user = User.objects.create_user(username="biz_user", password="password123")
    client.login(username="biz_user", password="password123")

    response = client.get(reverse("users:logoutbusinessuser"), follow=True)

    assert response.status_code == 200
    assert not response.wsgi_request.user.is_authenticated


@pytest.mark.django_db
def test_register_client_user(client):
    """Test client user registration view."""
    form_data = {
        "nickname": "client_nick",
        "email": "client@example.com",
        "password1": "SecurePass123!",
        "password2": "SecurePass123!"
    }
    response = client.post(reverse("users:registerclientuser"), data=form_data, follow=True)

    assert response.status_code == 200
    assert User.objects.filter(username="client_nick").exists()
    assert ClientUser.objects.filter(nickname="client_nick").exists()


@pytest.mark.django_db
def test_login_client_user(client):
    """Test login functionality for a client user with a proper ClientUser record."""
    # Create user
    user = User.objects.create_user(username="client_user", password="password123")

    # Add to the client group
    client_group = Group.objects.create(name="client")
    user.groups.add(client_group)

    # Create associated ClientUser instance
    ClientUser.objects.create(user=user, nickname="ClientNickname", email="client@example.com")

    # Attempt login
    response = client.post(reverse("users:loginclientuser"), data={"username": "client_user", "password": "password123"}, follow=True)

    assert response.status_code == 200
    assert response.wsgi_request.user.is_authenticated

@pytest.mark.django_db
def test_logout_client_user(client):
    """Test client user logout and cache clearing."""
    user = User.objects.create_user(username="client_user", password="password123")
    client.login(username="client_user", password="password123")

    response = client.get(reverse("users:logoutclientuser"), follow=True)

    assert response.status_code == 200
    assert not response.wsgi_request.user.is_authenticated


@pytest.mark.django_db
def test_update_business_user(client):
    """Test updating business user profile."""
    user = User.objects.create_user(username="biz_user", email="business@example.com", password="password123")
    business_group = Group.objects.create(name="business")
    user.groups.add(business_group)

    client.login(username="biz_user", password="password123")

    form_data = {
        "username": "updated_biz",
        "email": "new_business@example.com",
        "first_name": "NewName",
        "last_name": "NewLastName"
    }
    response = client.post(reverse("users:updatebusinessuser"), data=form_data, follow=True)

    assert response.status_code == 200
    user.refresh_from_db()
    assert user.username == "updated_biz"
    assert user.email == "new_business@example.com"


@pytest.mark.django_db
def test_update_client_user(client):
    """Test updating client user profile."""
    user = User.objects.create_user(username="client_user", email="client@example.com", password="password123")
    client_group = Group.objects.create(name="client")
    user.groups.add(client_group)

    client.login(username="client_user", password="password123")

    form_data = {
        "email": "new_client@example.com",
        "nickname": "new_nickname",
        "bio": "Updated bio."
    }
    response = client.post(reverse("users:updateclientuser"), data=form_data, follow=True)

    assert response.status_code == 200
    user.refresh_from_db()
    client_user = ClientUser.objects.get(user=user)
    assert user.email == "new_client@example.com"
    assert client_user.nickname == "new_nickname"
    assert client_user.bio == "Updated bio."

