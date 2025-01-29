import pytest
from django.contrib.auth.models import User
from clientchat.models import ChatMessages


@pytest.mark.django_db
class TestChatMessages:

    def test_create_chat_message(self):
        """Test creating a ChatMessages instance."""
        user = User.objects.create_user(username="testuser", password="password")
        message = ChatMessages.objects.create(
            user=user,
            sender_type="user",
            nickname="TestUser",
            content="Hello, this is a test message."
        )

        assert message.id is not None
        assert message.user == user
        assert message.sender_type == "user"
        assert message.nickname == "TestUser"
        assert message.content == "Hello, this is a test message."
        assert message.timestamp is not None  # Auto-generated

    def test_sender_type_choices(self):
        """Test that only valid sender_type choices are accepted."""
        user = User.objects.create_user(username="testuser", password="password")

        with pytest.raises(Exception):
            ChatMessages.objects.create(
                user=user,
                sender_type="invalid",  # ❌ Should fail (invalid choice)
                nickname="InvalidSender",
                content="This should not be allowed."
            )

    def test_str_representation(self):
        """Test the string representation of ChatMessages."""
        message = ChatMessages(
            sender_type="bot",
            nickname="AI",
            content="This is a bot response."
        )

        # 🔹 Extract dynamic content prefix
        expected_prefix = message.content[:20] + "..."
        expected_str = f"{message.nickname} ({message.sender_type}): {expected_prefix}"

        assert str(message) == expected_str
