import pytest
import uuid
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from businessdata.models import BusinessUserData
from chatbotsettings.models import ChatBotSettings  # Ensure this model exists


@pytest.mark.django_db
class TestBusinessUserDataModel:

    def setup_method(self):
        """Set up test users and related objects."""
        self.user = User.objects.create_user(username="testuser", password="password123")
        self.chat_bot = ChatBotSettings.objects.create(name="Test Bot")

    def test_create_business_user_data(self):
        """Test creating a valid BusinessUserData instance."""
        data = {"Q1": "A1", "Q2": "A2"}
        business_data = BusinessUserData.objects.create(
            user=self.user,
            document_title="Test Document",
            question_answer_data=data,
            chat_bot=self.chat_bot
        )

        assert isinstance(business_data.uuid, uuid.UUID)  # ✅ UUID should be auto-generated
        assert business_data.document_title == "Test Document"
        assert business_data.question_answer_data == data
        assert business_data.chat_bot.name == "Test Bot"

    def test_unique_document_title(self):
        """Test that document_title must be unique."""
        BusinessUserData.objects.create(
            user=self.user,
            document_title="Unique Document",
            question_answer_data={"Q1": "A1"}
        )

        with pytest.raises(Exception):  # ✅ Django raises IntegrityError for duplicates
            BusinessUserData.objects.create(
                user=self.user,
                document_title="Unique Document",
                question_answer_data={"Q2": "A2"}
            )

    # invalid json fields are filtered front frontend which does even let it enter in database so we dont test it at `model.py` level


    def test_str_representation_with_chat_bot(self):
        """Test string representation when a chat bot is present."""
        business_data = BusinessUserData.objects.create(
            user=self.user,
            document_title="Test Doc",
            question_answer_data={"Q1": "A1"},
            chat_bot=self.chat_bot
        )

        expected_str = f"Test Doc: {self.chat_bot.name}| Legal: {business_data.uuid}"
        assert str(business_data) == expected_str

    def test_str_representation_without_chat_bot(self):
        """Test string representation when no chat bot is present."""
        business_data = BusinessUserData.objects.create(
            user=self.user,
            document_title="Test Doc",
            question_answer_data={"Q1": "A1", "Q2": "A2"},
            chat_bot=None
        )

        expected_str = f"Doc: Test Doc | Data length: 2 | Legal: {business_data.uuid}"
        assert str(business_data) == expected_str
