import pytest
from django.contrib.auth.models import User
from users.models import ClientUser
from users.forms import (
    CreateBusinessUserForm,
    UpdateBusinessUserForm,
    CreateClientUserForm,
    UpdateClientUserForm
)


@pytest.mark.django_db
def test_create_business_user_form_valid():
    """Test CreateBusinessUserForm with valid data."""
    form_data = {
        "username": "testbusiness",
        "email": "business@example.com",
        "password1": "SecurePass123!",
        "password2": "SecurePass123!"
    }
    form = CreateBusinessUserForm(data=form_data)
    assert form.is_valid()


@pytest.mark.django_db
def test_create_business_user_form_invalid():
    """Test CreateBusinessUserForm with invalid password mismatch."""
    form_data = {
        "username": "testbusiness",
        "email": "business@example.com",
        "password1": "SecurePass123!",
        "password2": "WrongPass123!"
    }
    form = CreateBusinessUserForm(data=form_data)
    assert not form.is_valid()
    assert "password2" in form.errors


@pytest.mark.django_db
def test_update_business_user_form_valid():
    """Test UpdateBusinessUserForm with valid data."""
    user = User.objects.create_user(username="testuser", email="test@example.com")
    form_data = {
        "username": "updateduser",
        "email": "updated@example.com",
        "first_name": "John",
        "last_name": "Doe"
    }
    form = UpdateBusinessUserForm(instance=user, data=form_data)
    assert form.is_valid()
    updated_user = form.save()
    assert updated_user.username == "updateduser"
    assert updated_user.email == "updated@example.com"


@pytest.mark.django_db
def test_update_business_user_form_duplicate_email():
    """Test UpdateBusinessUserForm with duplicate email."""
    User.objects.create_user(username="existinguser", email="existing@example.com")
    user = User.objects.create_user(username="testuser", email="test@example.com")
    form_data = {
        "username": "updateduser",
        "email": "existing@example.com",  # ❌ Duplicate email
        "first_name": "John",
        "last_name": "Doe"
    }
    form = UpdateBusinessUserForm(instance=user, data=form_data)
    assert not form.is_valid()
    assert "email" in form.errors


@pytest.mark.django_db
def test_create_client_user_form_valid():
    """Test CreateClientUserForm with valid data."""
    form_data = {
        "nickname": "TestNick",
        "email": "client@example.com",
        "password1": "SecurePass123!",
        "password2": "SecurePass123!",
        "bio": "Short bio"
    }
    form = CreateClientUserForm(data=form_data)
    assert form.is_valid()
    user = form.save()
    assert user.username == "TestNick"
    assert user.email == "client@example.com"
    assert ClientUser.objects.filter(user=user).exists()


@pytest.mark.django_db
def test_create_client_user_form_invalid():
    """Test CreateClientUserForm with missing email."""
    form_data = {
        "nickname": "TestNick",
        "email": "",  # ❌ Missing email
        "password1": "SecurePass123!",
        "password2": "SecurePass123!"
    }
    form = CreateClientUserForm(data=form_data)
    assert not form.is_valid()
    assert "email" in form.errors


@pytest.mark.django_db
def test_update_client_user_form_valid():
    """Test UpdateClientUserForm updates both User and ClientUser."""
    user = User.objects.create_user(username="testuser", email="test@example.com")
    client_user = ClientUser.objects.create(user=user, nickname="OldNick", bio="Old Bio")
    
    form_data = {
        "email": "updated@example.com",
        "nickname": "NewNick",
        "bio": "Updated Bio"
    }
    form = UpdateClientUserForm(instance=user, data=form_data)
    assert form.is_valid()
    updated_user = form.save()
    
    client_user.refresh_from_db()
    assert updated_user.email == "updated@example.com"
    assert client_user.nickname == "NewNick"
    assert client_user.bio == "Updated Bio"


@pytest.mark.django_db
def test_update_client_user_form_duplicate_email():
    """Test UpdateClientUserForm fails on duplicate email."""
    User.objects.create_user(username="existinguser", email="existing@example.com")
    user = User.objects.create_user(username="testuser", email="test@example.com")
    form_data = {
        "email": "existing@example.com",  # ❌ Duplicate email
        "nickname": "NewNick",
        "bio": "Updated Bio"
    }
    form = UpdateClientUserForm(instance=user, data=form_data)
    assert not form.is_valid()
    assert "email" in form.errors
