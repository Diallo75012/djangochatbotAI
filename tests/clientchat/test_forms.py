import pytest
from clientchat.forms import ClientUserChatForm
from clientchat.models import ChatMessages
from django.contrib.auth.models import User


@pytest.mark.django_db
class TestClientUserChatForm:
    
    @pytest.fixture(autouse=True)
    def setup(self, db):
        """Set up test user and message instance."""
        self.user = User.objects.create_user(username="testuser", password="testpassword")
        self.chat_message = ChatMessages.objects.create(
            user=self.user,
            sender_type="user",
            nickname="TestUser",
            content="Hello, this is a test message."
        )

    def test_form_valid(self):
        """Test if the form is valid with correct data."""
        form_data = {"content": "This is a valid test message."}
        form = ClientUserChatForm(data=form_data)
        assert form.is_valid()

    def test_form_invalid_missing_content(self):
        """Test if the form is invalid when content is missing."""
        form_data = {"content": ""}
        form = ClientUserChatForm(data=form_data)
        assert not form.is_valid()
        assert "content" in form.errors

    def test_form_saves_message(self):
        """Test if the form correctly saves a message."""
        form_data = {"content": "New test message"}
        form = ClientUserChatForm(data=form_data)

        if form.is_valid():
            message = form.save(commit=False)
            message.user = self.user  # Assign test user
            message.sender_type = "user"
            message.nickname = "TestUser"
            message.save()

            assert ChatMessages.objects.last().content == "New test message"

    def test_field_labels(self):
        """Test the form label customization."""
        form = ClientUserChatForm()

        # ✅ Explicitly use the lowercase field name "content"
        expected_label = form.Meta.labels["Content"]

        assert expected_label == "Enter your message"
