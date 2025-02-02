import pytest
from django.urls import resolve, reverse
from chatbotsettings.views import (
    addChatBotSettings,
    updateChatBotSettings,
    deleteChatBotSettings,
    ChatBotSettingsManagement,
    getChatbotDetails,
)


@pytest.mark.parametrize("url_name, view_function, kwargs", [
    ("addchatbotsettings", addChatBotSettings, None),
    ("updatechatbotsettings", updateChatBotSettings, {"pk": 1}),
    ("deletechatbotsettings", deleteChatBotSettings, {"pk": 1}),
    ("chatbotsettingsmanagement", ChatBotSettingsManagement, None),
    ("getchatbotdetails", getChatbotDetails, {"business_data_id": 1}),
])
def test_url_resolves_correctly(url_name, view_function, kwargs):
    """Test that each URL correctly resolves to the expected view."""
    url = reverse(f"chatbotsettings:{url_name}", kwargs=kwargs) if kwargs else reverse(f"chatbotsettings:{url_name}")
    assert resolve(url).func == view_function
