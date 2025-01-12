import pytest
import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from agents.app_utils import ai_personality
import ast

def test_string_to_dict_valid():
    input_str = "{'chatbot_name': 'Test Bot', 'chatbot_description': 'A test chatbot'}"
    expected_dict = {'chatbot_name': 'Test Bot', 'chatbot_description': 'A test chatbot'}
    
    output_dict = ai_personality.string_to_dict(input_str)
    assert len(output_dict) == len(expected_dict)
    for key, value in output_dict.items():
      assert key in expected_dict
      assert value == expected_dict[key]

def test_string_to_dict_invalid():
    input_str = "invalid string format"
    with pytest.raises(ValueError):
        ai_personality.string_to_dict(input_str)

def test_personality_trait_formatting_with_env():
    # Set up environment variables
    os.environ["AI_PERSONALITY_DEFAULT"] = "{'chatbot_name': 'Env Bot', 'chatbot_description': 'Env Description'}"

    trait_dict = {
            "chatbot_name": None,
            "chatbot_description": None,
        "chatbot_age": 20,
        "chatbot_origin": "world",
        "chatbot_draw": "test",
            "chatbot_expertise": "test"
        }
    
    expected_dict = {
        "chatbot_name": 'Env Bot', 
        "chatbot_description": 'Env Description',
        "chatbot_age": 20,
        "chatbot_origin": "world",
        "chatbot_draw": "test",
            "chatbot_expertise": "test"
        }
    result_dict = ai_personality.personality_trait_formatting(trait_dict)
    assert result_dict == expected_dict


def test_personality_trait_formatting_no_env():
    trait_dict = {
            "chatbot_name": "Original Bot",
        "chatbot_description": "Original Desc",
        "chatbot_age": 20,
        "chatbot_origin": "world",
        "chatbot_draw": "test",
            "chatbot_expertise": "test"
        }
    expected_dict = trait_dict
        
    result_dict = ai_personality.personality_trait_formatting(trait_dict)
    
    assert result_dict == expected_dict
        
def test_personality_trait_formatting_error():
    trait_dict = {
        "chatbot_name": "Original Bot",
        "chatbot_description": "Original Desc",
        "chatbot_age": 20,
        "chatbot_origin": "world",
        "chatbot_draw": "test",
        "chatbot_expertise": "test"
        }
    
    with pytest.raises(AttributeError):
            original = ai_personality.load_dotenv
            ai_personality.load_dotenv = None #make load_dotenv fail
            ai_personality.personality_trait_formatting(trait_dict)
            ai_personality.load_dotenv = original
