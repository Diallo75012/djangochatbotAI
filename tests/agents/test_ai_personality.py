import unittest
from unittest.mock import patch
import os
from agents.app_utils.ai_personality import string_to_dict, personality_trait_formatting


class TestAIPersonality(unittest.TestCase):

    def test_string_to_dict_valid(self):
        """Test that a valid string dictionary is correctly converted to a Python dictionary."""
        valid_string = "{'Key1': 'value1', 'Key2': 'value2'}"
        expected_output = {"key1": "value1", "key2": "value2"}
        self.assertEqual(string_to_dict(valid_string), expected_output)

    def test_string_to_dict_invalid(self):
        """Test that an invalid string raises a ValueError."""
        invalid_string = "{invalid: json}"
        with self.assertRaises(ValueError):
            string_to_dict(invalid_string)

    @patch("agents.app_utils.ai_personality.string_to_dict_py")
    @patch("os.getenv")
    def test_personality_trait_formatting(self, mock_getenv, mock_string_to_dict_py):
        """Test personality_trait_formatting with default values from environment variables."""
        
        # Simulate env variable return
        mock_getenv.return_value = "{'chatbot_name': 'AI-Bot', 'chatbot_description': 'An AI assistant', 'chatbot_age': '5'}"
        mock_string_to_dict_py.return_value = {
            "chatbot_name": "AI-Bot",
            "chatbot_description": "An AI assistant",
            "chatbot_age": "5"
        }

        # Input traits (some fields empty)
        input_traits = {
            "chatbot_name": "",
            "chatbot_description": "A custom assistant",
            "chatbot_age": ""
        }

        # Expected result: empty fields should be replaced with defaults
        expected_output = {
            "chatbot_name": "AI-Bot",  # Filled from env
            "chatbot_description": "A custom assistant",  # Not empty, stays the same
            "chatbot_age": "5"  # Filled from env
        }

        self.assertEqual(personality_trait_formatting(input_traits), expected_output)

        # Ensure mocks were called correctly
        mock_getenv.assert_called_once_with("DEFAULT_AI_PERSONALITY_TRAIT")
        mock_string_to_dict_py.assert_called_once_with(mock_getenv.return_value)

'''
if __name__ == "__main__":
    unittest.main()
'''
