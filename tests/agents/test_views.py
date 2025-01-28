import pytest
import json
from unittest.mock import patch, MagicMock
from django.http import HttpResponse
from django.urls import reverse
from agents.views import (
    retrieveData,
    embedData,
    deleteEmbeddingCollection,
    is_business_user,
    is_client_user,
)
from businessdata.models import BusinessUserData
from django.contrib.auth.models import User, Group
from django.test import RequestFactory
from dotenv import load_dotenv, set_key

# load env vars
load_dotenv(dotenv_path='.env', override=False)
load_dotenv(dotenv_path=".vars.env", override=True)

@pytest.fixture
def factory():
    return RequestFactory()

@pytest.fixture
def business_user():
    user = User.objects.create_user(username='businessuser', password='testpassword')
    group = Group.objects.create(name='business')
    user.groups.add(group)
    return user

@pytest.fixture
def client_user():
    user = User.objects.create_user(username='clientuser', password='testpassword')
    group = Group.objects.create(name='client')
    user.groups.add(group)
    return user

@pytest.fixture
def business_document(business_user):
    return BusinessUserData.objects.create(
        user=business_user,
        document_title="Test Document",
        question_answer_data={"question1": "answer1", "question2": "answer2"},
        uuid="test-uuid"
    )

def test_is_business_user(business_user):
    assert is_business_user(business_user) == True

def test_is_client_user(client_user):
    assert is_client_user(client_user) == True

def test_is_business_user_false(client_user):
    assert is_business_user(client_user) == False

def test_is_client_user_false(business_user):
    assert is_client_user(business_user) == False

@patch("agents.views.retrieval_agent_team")
def test_retrieveData_success(mock_retrieval_agent_team, factory, client_user):
    mock_retrieval_agent_team.return_value = json.dumps({"answer_to_user": {"messages": [{"role": "ai", "content": json.dumps({"response": "test response"})}]}})
    request = factory.get(reverse("agents:retrieve-data"))
    request.user = client_user
    response = retrieveData(request)
    assert response.status_code == 200
    assert json.loads(response.content) == {"answer": "test response"}

@patch("agents.views.retrieval_agent_team")
def test_retrieveData_error(mock_retrieval_agent_team, factory, client_user):
    mock_retrieval_agent_team.side_effect = Exception("Test error")
    request = factory.get(reverse("agents:retrieve-data"))
    request.user = client_user
    response = retrieveData(request)
    assert response.status_code == 400
    assert "error" in json.loads(response.content)

@patch("agents.views.embed_data.vector_db_create")
def test_embedData_success(mock_vector_db_create, factory, business_user, business_document):
    mock_vector_db_create.return_value = {"success": "Data correctly embedded!"}
    request = factory.post(reverse("agents:embed-data", kwargs={"pk": business_document.pk}))
    request.user = business_user
    response = embedData(request, business_document.pk)
    assert response.status_code == 200
    assert "success" in json.loads(response.content)

@patch("agents.views.embed_data.vector_db_create")
def test_embedData_error(mock_vector_db_create, factory, business_user, business_document):
    mock_vector_db_create.side_effect = Exception("Test error")
    request = factory.post(reverse("agents:embed-data", kwargs={"pk": business_document.pk}))
    request.user = business_user
    response = embedData(request, business_document.pk)
    assert response.status_code == 400
    assert "error" in json.loads(response.content)

def test_embedData_get_not_allowed(factory, business_user, business_document):
    request = factory.get(reverse("agents:embed-data", kwargs={"pk": business_document.pk}))
    request.user = business_user
    response = embedData(request, business_document.pk)
    assert response.status_code == 405
    assert "error" in json.loads(response.content)

@patch("agents.views.delete_embeddings.delete_embedding_collection")
def test_deleteEmbeddingCollection_success(mock_delete_embedding_collection, factory, business_user, business_document):
    mock_delete_embedding_collection.return_value = "success"
    request = factory.post(reverse("agents:delete-embedding-collection", kwargs={"pk": business_document.pk}))
    request.user = business_user
    response = deleteEmbeddingCollection(request, business_document.pk)
    assert response.status_code == 200
    assert "success" in json.loads(response.content)

@patch("agents.views.delete_embeddings.delete_embedding_collection")
def test_deleteEmbeddingCollection_error(mock_delete_embedding_collection, factory, business_user, business_document):
    mock_delete_embedding_collection.side_effect = Exception("Test error")
    request = factory.post(reverse("agents:delete-embedding-collection", kwargs={"pk": business_document.pk}))
    request.user = business_user
    response = deleteEmbeddingCollection(request, business_document.pk)
    assert response.status_code == 400
    assert "error" in json.loads(response.content)
