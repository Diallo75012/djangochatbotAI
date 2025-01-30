import pytest
from businessdata.forms import BusinessUserDataForm, BusinessUserDataUpdateForm
from businessdata.models import BusinessUserData
from django.contrib.auth.models import User
from chatbotsettings.models import ChatBotSettings

@pytest.mark.django_db
def test_business_user_data_form_valid():
    """Test BusinessUserDataForm with valid data."""
    chatbot = ChatBotSettings.objects.create(name="Test Bot")  # Mock ChatBotSettings
    form_data = {
        "document_title": "Test Document",
        "question_answer_data": {"Q1": "A1", "Q2": "A2"},
        "chat_bot": chatbot.id
    }
    form = BusinessUserDataForm(data=form_data)
    assert form.is_valid(), form.errors

@pytest.mark.django_db
def test_business_user_data_form_invalid_json():
    """Test BusinessUserDataForm with invalid JSON."""
    form_data = {
        "document_title": "Invalid JSON Test",
        "question_answer_data": "Invalid JSON String",  # ❌ Should be a dictionary
        "chat_bot": None
    }
    form = BusinessUserDataForm(data=form_data)
    assert not form.is_valid()
    assert "question_answer_data" in form.errors

@pytest.mark.django_db
def test_business_user_data_update_form_valid():
    """Test BusinessUserDataUpdateForm with valid data."""
    chatbot = ChatBotSettings.objects.create(name="Update Bot")  # Mock ChatBotSettings
    form_data = {
        "document_title": "Updated Document",
        "question_answer_data": {"Q1": "New Answer"},
        "chat_bot": chatbot.id
    }
    form = BusinessUserDataUpdateForm(data=form_data)
    assert form.is_valid(), form.errors

@pytest.mark.django_db
def test_business_user_data_update_form_missing_data():
    """Test BusinessUserDataUpdateForm with missing required fields."""
    form_data = {
        "document_title": "",  # ❌ Missing required title
        "question_answer_data": {},  # ❌ Empty JSON
        "chat_bot": None
    }
    form = BusinessUserDataUpdateForm(data=form_data)
    assert not form.is_valid()
    assert "document_title" in form.errors
    assert "question_answer_data" in form.errors
