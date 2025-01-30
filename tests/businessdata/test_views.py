import pytest
import json
from unittest.mock import patch
from django.contrib.auth.models import User, Group
from django.urls import reverse
from businessdata.models import BusinessUserData
from chatbotsettings.models import ChatBotSettings

@pytest.mark.django_db
def test_business_data_management_view(client):
    """Test the business data management page loads for authenticated business users."""
    business_user = User.objects.create_user(username="business_user", password="password123")
    business_group = Group.objects.create(name="business")
    business_user.groups.add(business_group)
    client.login(username="business_user", password="password123")

    response = client.get(reverse("businessdata:businessdatamanagement"))
    assert response.status_code == 200
    assert "business/businessdatamanagement.html" in [t.name for t in response.templates]


@pytest.mark.django_db
@patch("requests.Session.post")  # Mock the external request
def test_add_business_data_view(mock_post, client):
    """Test adding valid business data with a mocked embedding request."""
    mock_post.return_value.status_code = 200
    mock_post.return_value.json.return_value = {"success": True}

    business_user = User.objects.create_user(username="business_user", password="password123")
    business_group = Group.objects.create(name="business")
    business_user.groups.add(business_group)
    chatbot = ChatBotSettings.objects.create(name="Test ChatBot")
    client.login(username="business_user", password="password123")

    form_data = {
        "document_title": "New Business Doc",
        "question_answer_data": json.dumps({"Q1": "A1", "Q2": "A2"}),
        "chat_bot": chatbot.id
    }
    response = client.post(reverse("businessdata:addbusinessdata"), data=form_data, follow=True)

    assert response.status_code == 200
    assert BusinessUserData.objects.filter(document_title="New Business Doc").exists()
    mock_post.assert_called_once()  # Ensure embedding request was made


@pytest.mark.django_db
@patch("requests.Session.post")  # Mock external embedding request
def test_update_business_data_view(mock_post, client):
    """Test updating an existing business data entry and ensure embedding request is made."""
    mock_post.return_value.status_code = 200
    mock_post.return_value.json.return_value = {"success": True}

    business_user = User.objects.create_user(username="business_user", password="password123")
    business_group = Group.objects.create(name="business")
    business_user.groups.add(business_group)
    chatbot = ChatBotSettings.objects.create(name="Test ChatBot")

    # Ensure the initial data is different in length
    business_data = BusinessUserData.objects.create(
        user=business_user,
        document_title="Existing Doc",
        question_answer_data={"Q1": "Old Answer", "Q2": "Another Old Answer"},
        chat_bot=chatbot
    )
    client.login(username="business_user", password="password123")

    form_data = {
        "document_title": "Updated Doc",
        "question_answer_data": json.dumps({"Q1": "New Answer"}),  # Changed length
        "chat_bot": chatbot.id
    }

    response = client.post(reverse("businessdata:updatebusinessdata", kwargs={"pk": business_data.pk}), data=form_data, follow=True)

    assert response.status_code == 200
    business_data.refresh_from_db()
    assert business_data.document_title == "Updated Doc"
    assert business_data.question_answer_data == {"Q1": "New Answer"}

    # ✅ Ensure embedding request is triggered
    if len(json.dumps({"Q1": "New Answer"})) != len(json.dumps({"Q1": "Old Answer", "Q2": "Another Old Answer"})):
        mock_post.assert_called_once()
    else:
        pytest.fail("Embedding request was not triggered because question_answer_data length did not change.")

@pytest.mark.django_db
@patch("requests.Session.post")  # Mock external delete request
def test_delete_business_data_view(mock_post, client):
    """Test deleting business data."""
    mock_post.return_value.status_code = 200
    mock_post.return_value.json.return_value = {"success": True}

    business_user = User.objects.create_user(username="business_user", password="password123")
    business_group = Group.objects.create(name="business")
    business_user.groups.add(business_group)

    business_data = BusinessUserData.objects.create(
        user=business_user,
        document_title="To Be Deleted",
        question_answer_data={"Q1": "Answer"}
    )
    client.login(username="business_user", password="password123")

    response = client.post(reverse("businessdata:deletebusinessdata", kwargs={"pk": business_data.pk}), follow=True)

    assert response.status_code == 200
    assert not BusinessUserData.objects.filter(id=business_data.id).exists()
    mock_post.assert_called_once()


@pytest.mark.django_db
def test_add_business_data_invalid_form(client):
    """Test form validation error handling for adding business data."""
    business_user = User.objects.create_user(username="business_user", password="password123")
    business_group = Group.objects.create(name="business")
    business_user.groups.add(business_group)
    client.login(username="business_user", password="password123")

    form_data = {
        "document_title": "",  # ❌ Missing required title
        "question_answer_data": "",  # ❌ Invalid JSON
        "chat_bot": ""  # Fixed: `None` → `""`
    }
    response = client.post(reverse("businessdata:addbusinessdata"), data=form_data, follow=True)

    assert response.status_code == 200
    assert "Form submission incorrect" in response.content.decode()
