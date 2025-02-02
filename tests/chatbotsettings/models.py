import pytest
import uuid
import os
from unittest import mock
from unittest.mock import MagicMock
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from chatbotsettings.models import ChatBotSettings
from businessdata.models import BusinessUserData


@pytest.mark.django_db
def test_create_chatbot_settings():
    """Test creating a ChatBotSettings instance."""
    user = User.objects.create_user(username="testuser", password="securepassword")

    business_user = BusinessUserData.objects.create(
        user=user,
        uuid=uuid.uuid4(),
        document_title="UserDoc",
        question_answer_data="Some QA Data",
    )

    chatbot = ChatBotSettings.objects.create(
        business_user=user,
        business_user_uuid=business_user,
        name="HelperBot",
        description="An AI bot helping users.",
    )

    assert chatbot.name == "HelperBot"
    assert chatbot.description == "An AI bot helping users."


@pytest.mark.django_db
def test_chatbot_settings_str():
    """Test string representation of ChatBotSettings."""
    user = User.objects.create_user(username="testuser2", password="securepassword")

    business_user = BusinessUserData.objects.create(
        user=user,
        uuid=uuid.uuid4(),
        document_title="UserDoc",
        question_answer_data="Some QA Data",
    )

    chatbot = ChatBotSettings.objects.create(
        business_user=user,
        business_user_uuid=business_user,
        name="HelperBot",
        description="An AI bot helping users.",
    )

    expected_str = f"HelperBot: An AI bot helping users....| From {user}-{business_user}"
    assert str(chatbot) == expected_str

@pytest.mark.django_db
def test_chatbot_avatar_uniqueness():
    """Test that an avatar file should be unique based on filename."""

    user = User.objects.create_user(username="testuser3", password="securepassword")

    business_user = BusinessUserData.objects.create(
        user=user,
        uuid=uuid.uuid4(),
        document_title="Avatar Test",
        question_answer_data="Some QA Data",
    )

    # ✅ Mock the queryset to simulate an existing file with the same name
    ChatBotSettings.objects.filter = MagicMock(
        return_value=MagicMock(first=lambda: True)  # Simulate an existing entry
    )

    chatbot = ChatBotSettings(
        business_user=user,
        business_user_uuid=business_user,
        name="TestBot",
        avatar="test_avatar.jpg",
    )

    # ✅ Call clean_avatar to check if ValidationError is triggered
    with pytest.raises(ValidationError, match="This image filename is already being used by another ChatBot."):
        chatbot.clean_avatar()

@pytest.mark.django_db
@mock.patch("os.path.isfile", return_value=True)
@mock.patch("os.remove")
def test_chatbot_settings_delete(mock_remove, mock_isfile):
    """Test that deleting ChatBotSettings also removes the associated avatar file."""
    user = User.objects.create_user(username="testuser4", password="securepassword")

    business_user = BusinessUserData.objects.create(
        user=user,
        uuid=uuid.uuid4(),
        document_title="Delete Test",
        question_answer_data="Some QA Data",
    )

    avatar_file = SimpleUploadedFile("delete_avatar.jpg", b"fake_image_data")

    chatbot = ChatBotSettings.objects.create(
        business_user=user,
        business_user_uuid=business_user,
        name="DeleteBot",
        avatar=avatar_file,
    )

    chatbot.delete()

    # ✅ Ensure file removal was attempted
    mock_remove.assert_called_once_with(os.path.join(chatbot.avatar.storage.location, chatbot.avatar.name))
