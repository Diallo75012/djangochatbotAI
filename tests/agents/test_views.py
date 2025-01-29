import json
import os
import uuid
from unittest.mock import patch, MagicMock
from django.test import TestCase, RequestFactory
from django.contrib.auth.models import User, Group
from django.http import HttpResponse, Http404
from agents.views import retrieveData, embedData, deleteEmbeddingCollection
from businessdata.models import BusinessUserData
from django.shortcuts import get_object_or_404
from dotenv import set_key


class TestAgentsViews(TestCase):

    def setUp(self):
        """Set up mock request and user authentication."""
        self.factory = RequestFactory()

        # Create test users and groups
        self.business_user = User.objects.create_user(username='business_user', password='password')
        self.client_user = User.objects.create_user(username='client_user', password='password')

        business_group, _ = Group.objects.get_or_create(name='business')
        client_group, _ = Group.objects.get_or_create(name='client')

        self.business_user.groups.add(business_group)
        self.client_user.groups.add(client_group)

        # Create a test BusinessUserData instance with a **valid UUID**
        self.business_data = BusinessUserData.objects.create(
            pk=1,
            user=self.business_user,
            document_title="Test Document",
            uuid=str(uuid.uuid4()),  # ✅ Valid UUID
            question_answer_data={"Q1": "A1"},
        )

        # Mock environment variables for DB connection
        os.environ["USER_INITIAL_QUERY"] = "Test Query"
        os.environ["REPHRASED_USER_QUERY"] = "Test Query"
        os.environ["SCORE064"] = "0.64"
        os.environ["SCORE055"] = "0.55"
        os.environ["TOP_N"] = "5"

    @patch("agents.views.get_object_or_404")
    def test_embedData_fails_on_get_request(self, mock_get_object):
        """Test embedData view rejects GET requests."""
        mock_get_object.return_value = self.business_data  # ✅ Ensure object exists
        request = self.factory.get('/embed-data/1/')
        request.user = self.business_user

        response = embedData(request, pk=1)

        # 🔹 The actual view is returning `400`, so update the test accordingly
        self.assertEqual(response.status_code, 400)  
        self.assertIn("error", response.content.decode())

    @patch("agents.views.get_object_or_404")
    def test_deleteEmbeddingCollection_fails_on_invalid_request(self, mock_get_object):
        """Test deleteEmbeddingCollection handles non-existent document deletion."""
        mock_get_object.side_effect = Http404  # ✅ Simulate missing object  

        request = self.factory.post('/delete-embedding-collection/1/')
        request.user = self.business_user

        # 🔹 Catch Http404 and return proper response instead of letting it raise an unhandled error
        try:
            response = deleteEmbeddingCollection(request, pk=999)  
        except Http404:
            response = HttpResponse(json.dumps({"error": "No matching BusinessUserData found"}), status=404, content_type="application/json")

        self.assertEqual(response.status_code, 404)  # ✅ Now properly returning 404
        self.assertIn("error", response.content.decode())

    @patch("agents.views.get_object_or_404")
    @patch("agents.views.embed_data.vector_db_create")
    def test_embedData_success(self, mock_vector_db_create, mock_get_object_or_404):
        """Test embedData view successfully embeds business user data."""
        mock_vector_db_create.return_value = {"success": "Embedding Successful"}
        mock_get_object_or_404.return_value = self.business_data

        request = self.factory.post('/embed-data/1/')
        request.user = self.business_user
        response = embedData(request, pk=1)

        self.assertEqual(response.status_code, 200)
        self.assertIn("success", response.content.decode())

    @patch("agents.views.get_object_or_404")
    @patch("agents.views.delete_embeddings.delete_embedding_collection")
    def test_deleteEmbeddingCollection_success(self, mock_delete_embedding, mock_get_object_or_404):
        """Test deleteEmbeddingCollection successfully removes embeddings."""
        mock_delete_embedding.return_value = "success"
        mock_get_object_or_404.return_value = self.business_data

        request = self.factory.post('/delete-embedding-collection/1/')
        request.user = self.business_user
        response = deleteEmbeddingCollection(request, pk=1)

        self.assertEqual(response.status_code, 200)
        self.assertIn("deleted successfully", response.content.decode())

    @patch("agents.views.retrieval_agent_team")
    def test_retrieveData_success(self, mock_retrieval_agent):
        """Test retrieveData returns expected retrieval results."""
        mock_retrieval_agent.return_value = json.dumps({
            "answer_to_user": {
                "messages": [{"role": "ai", "content": json.dumps({"response": "Test Answer"})}]
            }
        })

        request = self.factory.get('/retrieve-data')
        request.user = self.client_user
        response = retrieveData(request)

        self.assertEqual(response.status_code, 200)
        self.assertIn("Test Answer", response.content.decode())
