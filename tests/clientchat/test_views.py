import json
from unittest.mock import patch, mock_open, Mock # Import Mock
from django.test import TestCase, override_settings, Client
from django.urls import reverse
from django.contrib.auth.models import User, Group
from django.contrib.messages.middleware import MessageMiddleware
from django.contrib.sessions.middleware import SessionMiddleware
from django.http import HttpResponse, JsonResponse
from django.core.files.uploadedfile import SimpleUploadedFile
from clientchat.views import clientUserChat
from businessdata.models import BusinessUserData
from chatbotsettings.models import ChatBotSettings
from users.models import ClientUser
from clientchat.models import ChatMessages

@override_settings(MEDIA_ROOT='/tmp/test_media')
class TestClientUserChatView(TestCase):
    def setUp(self):
        self.client = Client()
        # Create a user and client group for testing
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        client_group, created = Group.objects.get_or_create(name='client')
        self.user.groups.add(client_group)
        ClientUser.objects.create(user=self.user, nickname='Test Client')
        self.client.force_login(self.user)

        # Create a BusinessUserData instance for testing
        self.business_data = BusinessUserData.objects.create(
            document_title="Test Document",
            user=self.user,
            question_answer_data="[]"
        )
        # Create ChatBotSettings with a dummy avatar
        self.chatbot_settings = ChatBotSettings.objects.create(
            name="Test Chatbot",
            description="Test Description",
            avatar=SimpleUploadedFile(
                "dummy_avatar.png",
                b"content",
                content_type="image/png"
            )
        )
        self.business_data.chat_bot = self.chatbot_settings
        self.business_data.save()


    @patch("clientchat.views.mc.get")
    @patch("clientchat.views.mc.set")
    def test_clientUserChat_get(self, mock_cache_set, mock_cache_get):
        """Test GET request renders the chat template."""
        mock_cache_get.return_value = None  # No cached messages

        response = self.client.get(reverse("clientchat:clientuserchat"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'clientchat/clientuserchat.html')


    @patch("clientchat.views.mc.get")
    @patch("clientchat.views.mc.set")
    @patch("clientchat.views.get_object_or_404")
    @patch("clientchat.views.ai_personality.personality_trait_formatting")
    @patch("clientchat.views.requests.Session.get") # Correctly patch requests.Session.get
    def test_clientUserChat_post_success(
        self, mock_requests_get, mock_ai_personality, mock_get_object, mock_cache_set, mock_cache_get
    ):
        """Test successful POST request for chatbot interaction."""
        mock_cache_get.return_value = []
        mock_get_object.return_value = self.business_data
        mock_ai_personality.return_value = {
            "chatbot_name": "AI Bot",
            "chatbot_description": "AI Assistant",
            "chatbot_age": "30",
            "chatbot_origin": "Virtual",
            "chatbot_dream": "To assist users",
            "chatbot_tone": "Friendly",
            "chatbot_expertise": "Tech"
        }
        # Mock successful retrieval agent response - use requests.Response mock
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"answer": "This is a mock response from the retrieval agent."}
        mock_requests_get.return_value = mock_response


        request_data = {
            "chatbot_name": "AI Bot",
            "chatbot_description": "AI Assistant",
            "message": "Hello AI!",
            "document_title_id": str(self.business_data.id),
        }

        response = self.client.post(
            reverse("clientchat:clientuserchat"),
            data=json.dumps(request_data),
            content_type="application/json"
        )
        self.assertEqual(response.status_code, 200) # Expect 200 for success
        response_data = json.loads(response.content)
        self.assertIn('bot_message', response_data)


    @patch("clientchat.views.mc.get")
    @patch("clientchat.views.mc.set")
    def test_clientUserChat_post_missing_fields(self, mock_cache_set, mock_cache_get):
        """Test POST request with missing chatbot fields."""
        mock_cache_get.return_value = []

        request_data = {
            "chatbot_name": "",
            "chatbot_description": "",
            "message": "Test message",
            "document_title_id": str(self.business_data.id),
        }

        response = self.client.post(
            reverse("clientchat:clientuserchat"),
            data=json.dumps(request_data),
            content_type="application/json"
        )
        self.assertEqual(response.status_code, 400)
        response_data = json.loads(response.content)
        self.assertIn('error', response_data)


    @patch("clientchat.views.mc.get")
    @patch("clientchat.views.mc.set")
    @patch("clientchat.views.requests.Session.get") # Correctly patch requests.Session.get
    def test_clientUserChat_post_retrieval_api_failure(
        self, mock_requests_get, mock_cache_set, mock_cache_get
    ):
        """Test failure when retrieval agent API returns an error."""
        mock_cache_get.return_value = []
        # Mock retrieval agent API returning an error (status code 400) - use requests.Response mock
        mock_response = Mock()
        mock_response.status_code = 400
        mock_response.json.return_value = {"error": "Retrieval API failed"}
        mock_requests_get.return_value = mock_response


        request_data = {
            "chatbot_name": "AI Bot",
            "chatbot_description": "AI Assistant",
            "message": "Hello AI!",
            "document_title_id": str(self.business_data.id),
        }

        response = self.client.post(
            reverse("clientchat:clientuserchat"),
            data=json.dumps(request_data),
            content_type="application/json"
        )
        self.assertEqual(response.status_code, 400) # Expect 400 as we mock retrieval API to return 400
        response_data = json.loads(response.content)
        self.assertIn('error', response_data)
