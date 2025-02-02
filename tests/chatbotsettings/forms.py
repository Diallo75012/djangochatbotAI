import pytest
from chatbotsettings.forms import ChatBotSettingsForm, ChatBotSettingsUpdateForm
from chatbotsettings.models import ChatBotSettings

@pytest.mark.django_db
@pytest.mark.django_db
def test_chatbot_settings_form_valid_data():
    form_data = {
        "name": "AI Assistant",
        "tone": "Friendly",
        "description": "A helpful AI chatbot",
        "expertise": "Technology",
        "custom_greeting": "Hello! How can I help you?",
        "example_of_response": "Sure, I can help with that!",
        "origin": "Digital World",
        "age": 2,  # Fixed: Use an integer
        "dream": "To assist humans efficiently",
        "avatar": None,
    }
    form = ChatBotSettingsForm(data=form_data)
    assert form.is_valid(), form.errors

@pytest.mark.django_db
def test_chatbot_settings_form_missing_required_fields():
    form_data = {
        "tone": "Friendly",  # 'name' is missing
        "description": "A helpful AI chatbot",
        "expertise": "Technology",
        "custom_greeting": "Hello! How can I help you?",
        "example_of_response": "Sure, I can help with that!",
        "origin": "Digital World",
        "age": "2 years",
        "dream": "To assist humans efficiently",
        "avatar": None,
    }
    form = ChatBotSettingsForm(data=form_data)
    assert not form.is_valid()
    assert "name" in form.errors  # 'name' is required

@pytest.mark.django_db
def test_chatbot_settings_update_form_valid_data():
    form_data = {
        "name": "Updated Bot",
        "tone": "Professional",
        "description": "A more advanced AI chatbot",
        "expertise": "Business",
        "custom_greeting": "Good day! How may I assist you?",
        "example_of_response": "I can help you with financial advice.",
        "origin": "AI Labs",
        "age": 5,  # Fixed: Use an integer
        "dream": "To become the best AI assistant",
        "avatar": None,
    }
    form = ChatBotSettingsUpdateForm(data=form_data)
    assert form.is_valid(), form.errors

@pytest.mark.django_db
def test_chatbot_settings_update_form_missing_required_fields():
    form_data = {
        "tone": "Professional",  # 'name' is missing
        "description": "A more advanced AI chatbot",
        "expertise": "Business",
        "custom_greeting": "Good day! How may I assist you?",
        "example_of_response": "I can help you with financial advice.",
        "origin": "AI Labs",
        "age": "5 years",
        "dream": "To become the best AI assistant",
        "avatar": None,
    }
    form = ChatBotSettingsUpdateForm(data=form_data)
    assert not form.is_valid()
    assert "name" in form.errors  # 'name' is required

@pytest.mark.django_db
def test_chatbot_settings_form_labels():
    form = ChatBotSettingsForm()
    assert form.fields["name"].label == "Bot name"
    assert form.fields["tone"].label == "Tone of voice"
    assert form.fields["description"].label == "Bot description"
    assert form.fields["expertise"].label == "Expert in ..."
    assert form.fields["custom_greeting"].label == "How should the Bot greets?"
    assert form.fields["example_of_response"].label == "Optional example of response"
    assert form.fields["origin"].label == "Where is the Bot from?"
    assert form.fields["age"].label == "How old is the Bot?"
    assert form.fields["dream"].label == "What is the Bot dreaming of?"
    assert form.fields["avatar"].label == "Bot logo or picture"
