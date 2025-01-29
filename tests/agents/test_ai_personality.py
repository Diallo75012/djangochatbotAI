import unittest
import json
import os
from agents.app_utils.ai_personality import personality_trait_formatting
from rust_lib import string_to_dict_py


class TestAIPersonality(unittest.TestCase):

    def test_string_to_dict_valid(self):
        """Test that a valid JSON string dictionary is correctly converted to a Python dictionary."""
        valid_json_string = '{"Key1": "value1", "Key2": "value2"}'  # ✅ FIX: Use JSON format
        expected_output = {"key1": "value1", "key2": "value2"}  # ✅ Ensures lowercase keys

        self.assertEqual(string_to_dict_py(valid_json_string), expected_output)  # ✅ FIXED

    def test_string_to_dict_invalid(self):
        """Test that an invalid string raises a ValueError."""
        invalid_string = "{invalid: json}"  # Still an invalid format
        with self.assertRaises(ValueError):
            string_to_dict_py(invalid_string)

    def test_personality_trait_formatting(self):
        """Test personality_trait_formatting with default values from environment variables."""
        
        # ✅ FIX: Use JSON format for `DEFAULT_AI_PERSONALITY_TRAIT`
        default_traits = {
            "chatbot_name": "AI-Bot",
            "chatbot_description": "An AI assistant",
            "chatbot_age": "5"
        }
        os.environ["DEFAULT_AI_PERSONALITY_TRAIT"] = json.dumps(default_traits)

        # Input traits (some fields empty)
        input_traits = {
            "chatbot_name": "",  # Should be replaced with "AI-Bot"
            "chatbot_description": "A custom assistant",  # Should remain unchanged
            "chatbot_age": ""  # Should be replaced with "5"
        }

        expected_output = {
            "chatbot_name": "AI-Bot",  # ✅ FIXED
            "chatbot_description": "A custom assistant",
            "chatbot_age": "5"  # ✅ FIXED
        }

        try:
            result = personality_trait_formatting(input_traits)
            print("\n=== Rust Function Debugging ===")
            print("Input Traits:", json.dumps(input_traits, indent=2))
            print("Default Traits:", json.dumps(default_traits, indent=2))
            print("Rust Function Output:", result)

            self.assertEqual(result, expected_output)
        except Exception as e:
            print("Rust function failed:", str(e))
            self.fail(f"Rust function failed unexpectedly: {str(e)}")

'''
if __name__ == "__main__":
    unittest.main()
'''
