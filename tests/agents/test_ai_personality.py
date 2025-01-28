import os
import pytest
from agents.app_utils.ai_personality import (
    string_to_dict,
    personality_trait_formatting,
)

@pytest.fixture
def default_ai_personality_trait():
    # Set a default value for the environment variable for testing
    os.environ["DEFAULT_AI_PERSONALITY_TRAIT"] = '{"chatbot_name": "TestBot", "chatbot_description": "A test chatbot.", "chatbot_age": "1", "chatbot_origin": "TestLand", "chatbot_dream": "To pass tests", "chatbot_tone": "Testy", "chatbot_expertise": "Testing"}'
    yield
    # Clean up the environment variable after the test
    del os.environ["DEFAULT_AI_PERSONALITY_TRAIT"]

def test_string_to_dict_valid():
    test_string = '{"key1": "value1", "key2": "value2"}'
    expected_dict = {"key1": "value1", "key2": "value2"}
    assert string_to_dict(test_string) == expected_dict

def test_string_to_dict_invalid():
    test_string = "invalid string"
    with pytest.raises(ValueError, match="Error converting string to dictionary"):
        string_to_dict(test_string)

def test_string_to_dict_not_dict():
    test_string = '"not a dict"'
    with pytest.raises(ValueError, match="Error converting string to dictionary"):
        string_to_dict(test_string)

def test_personality_trait_formatting_with_empty_values(default_ai_personality_trait):
    trait_dict = {
        "chatbot_name": "",
        "chatbot_description": "Custom description",
        "chatbot_age": "",
        "chatbot_origin": "",
        "chatbot_dream": "",
        "chatbot_tone": "",
        "chatbot_expertise": "",
    }
    expected_dict = {
        "chatbot_name": "TestBot",
        "chatbot_description": "Custom description",
        "chatbot_age": "1",
        "chatbot_origin": "TestLand",
        "chatbot_dream": "To pass tests",
        "chatbot_tone": "Testy",
        "chatbot_expertise": "Testing",
    }
    assert personality_trait_formatting(trait_dict) == expected_dict

def test_personality_trait_formatting_no_empty_values(default_ai_personality_trait):
    trait_dict = {
        "chatbot_name": "Custom Name",
        "chatbot_description": "Custom description",
        "chatbot_age": "2",
        "chatbot_origin": "CustomLand",
        "chatbot_dream": "To be the best",
        "chatbot_tone": "CustomTone",
        "chatbot_expertise": "Custom Expertise",
    }
    expected_dict = {
        "chatbot_name": "Custom Name",
        "chatbot_description": "Custom description",
        "chatbot_age": "2",
        "chatbot_origin": "CustomLand",
        "chatbot_dream": "To be the best",
        "chatbot_tone": "CustomTone",
        "chatbot_expertise": "Custom Expertise",
    }
    assert personality_trait_formatting(trait_dict) == expected_dict
