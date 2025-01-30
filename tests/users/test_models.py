import pytest
from django.contrib.auth.models import User
from users.models import ClientUser
from django.db.utils import IntegrityError

@pytest.mark.django_db
def test_create_client_user():
    """Test successful creation of a ClientUser instance."""
    user = User.objects.create_user(username="testuser", password="securepassword")
    client_user = ClientUser.objects.create(
        user=user,
        nickname="TestNick",
        bio="This is a test bio",
        email="testuser@example.com"
    )

    assert client_user.user == user
    assert client_user.nickname == "TestNick"
    assert client_user.bio == "This is a test bio"
    assert client_user.email == "testuser@example.com"
    assert client_user.picture == ""

@pytest.mark.django_db
def test_one_to_one_constraint():
    """Test that a User can only have one ClientUser."""
    user = User.objects.create_user(username="testuser", password="securepassword")
    ClientUser.objects.create(user=user, nickname="Nick1", email="user1@example.com")

    with pytest.raises(IntegrityError):
        ClientUser.objects.create(user=user, nickname="Nick2", email="user2@example.com")

@pytest.mark.django_db
def test_unique_email_constraint():
    """Test that ClientUser email must be unique."""
    user1 = User.objects.create_user(username="user1", password="password1")
    user2 = User.objects.create_user(username="user2", password="password2")

    ClientUser.objects.create(user=user1, nickname="Nick1", email="unique@example.com")

    with pytest.raises(IntegrityError):
        ClientUser.objects.create(user=user2, nickname="Nick2", email="unique@example.com")  # Should fail

@pytest.mark.django_db
def test_client_user_str():
    """Test the string representation of ClientUser."""
    user = User.objects.create_user(username="testuser", password="securepassword")
    client_user = ClientUser.objects.create(
        user=user,
        nickname="NickName",
        bio="A very long biography that will be truncated in the __str__ method.",
        email="test@example.com"
    )

    # Ensure consistent truncation
    expected_bio = client_user.bio[:50]  # Match model truncation logic
    expected_str = f"NickName: {expected_bio}..."
    
    assert str(client_user) == expected_str
