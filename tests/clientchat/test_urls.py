import unittest
from django.urls import reverse, resolve
from clientchat.views import clientUserChat


class TestClientChatUrls(unittest.TestCase):

    def test_clientuserchat_url_resolves(self):
        """Test that the 'clientuserchat' URL resolves to the correct view."""
        url = reverse("clientchat:clientuserchat")
        self.assertEqual(resolve(url).func, clientUserChat)

    def test_clientchat_app_name(self):
        """Test that the app name is correctly set to 'clientchat'."""
        self.assertEqual(reverse("clientchat:clientuserchat"), "/clientchat/clientuserchat")


'''
if __name__ == "__main__":
    unittest.main()
'''
