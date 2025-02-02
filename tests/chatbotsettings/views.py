import pytest
import uuid
from unittest.mock import patch, MagicMock
from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse
from django.test import Client
from chatbotsettings.models import ChatBotSettings
from businessdata.models import BusinessUserData


@pytest.mark.django_db
def test_add_chatbot_settings(client):
    """Test adding chatbot settings successfully."""
    user = User.objects.create_user(username="testuser", password="securepassword")
    client.login(username="testuser", password="securepassword")

    # Mock avatar file upload
    avatar_file = SimpleUploadedFile("test_avatar.jpg", b"fake_image_data")

    response = client.post(
        reverse("chatbotsettings:addchatbotsettings"),
        {
            "name": "TestBot",
            "description": "An AI chatbot.",
            "avatar": avatar_file,
        },
        follow=True
    )

    assert response.status_code == 200
    assert ChatBotSettings.objects.filter(name="TestBot").exists()
    assert "ChatBot settings added successfully!" in response.content.decode()


@pytest.mark.django_db
def test_update_chatbot_settings(client):
    """Test updating chatbot settings successfully."""
    user = User.objects.create_user(username="testuser", password="securepassword")
    client.login(username="testuser", password="securepassword")

    chatbot = ChatBotSettings.objects.create(
        business_user=user,
        name="UpdateBot",
        description="Before update"
    )

    response = client.post(
        reverse("chatbotsettings:updatechatbotsettings", args=[chatbot.id]),
        {"name": "UpdateBot", "description": "Updated description"},
        follow=True
    )

    assert response.status_code == 200
    chatbot.refresh_from_db()
    assert chatbot.description == "Updated description"
    assert "ChatBot has been updated successfully." in response.content.decode()


@pytest.mark.django_db
def test_delete_chatbot_settings(client):
    """Test deleting chatbot settings."""
    user = User.objects.create_user(username="testuser", password="securepassword")
    client.login(username="testuser", password="securepassword")

    chatbot = ChatBotSettings.objects.create(
        business_user=user,
        name="DeleteBot",
        description="To be deleted"
    )

    response = client.post(
        reverse("chatbotsettings:deletechatbotsettings", args=[chatbot.id]),
        follow=True
    )

    assert response.status_code == 200
    assert not ChatBotSettings.objects.filter(name="DeleteBot").exists()
    assert "ChatBot settings has been successfully deleted." in response.content.decode()


@pytest.mark.django_db
def test_get_chatbot_details(client):
    """Test fetching chatbot details."""
    user = User.objects.create_user(username="testuser", password="securepassword")

    business_data = BusinessUserData.objects.create(
        user=user,
        uuid=uuid.uuid4(),
        document_title="Test Business",
        question_answer_data="Data QA"
    )

    chatbot = ChatBotSettings.objects.create(
        business_user=user,
        name="TestChatbot",
        description="A helpful bot",
    )

    business_data.chat_bot = chatbot
    business_data.save()

    response = client.get(reverse("chatbotsettings:getchatbotdetails", args=[business_data.id]))

    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "TestChatbot"
    assert data["description"] == "A helpful bot"
