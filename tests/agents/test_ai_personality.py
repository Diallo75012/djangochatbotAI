import unittest
import json
import os
from dotenv import load_dotenv
from rust_lib import load_personality


class TestAIPersonality(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        """Load environment variables from `.vars.env` before tests."""
        dotenv_path = ".vars.env"
        assert os.path.exists(dotenv_path), "❌ .vars.env file is missing!"

        load_dotenv(dotenv_path=dotenv_path, override=True)

        cls.default_traits = os.getenv("AI_PERSONALITY_TRAITS")
        assert cls.default_traits, "❌ AI_PERSONALITY_TRAITS not found in .vars.env!"
        
        cls.default_traits_dict = json.loads(cls.default_traits)

    def test_personality_trait_formatting(self):
        """Test that `load_personality()` correctly fills missing fields from `.vars.env`."""

        # ✅ Input traits (some missing fields)
        input_traits = {
            "chatbot_name": "",  # Should be replaced with `.vars.env`
            "chatbot_description": "A custom assistant",  # Should remain unchanged
            "chatbot_age": ""  # Should be replaced with `.vars.env`
        }

        # ✅ Expected fields that must be updated
        expected_updates = {
            "chatbot_name": self.default_traits_dict["chatbot_name"],  # From `.vars.env`
            "chatbot_description": "A custom assistant",  # Remains unchanged
            "chatbot_age": self.default_traits_dict["chatbot_age"]  # From `.vars.env`
        }

        print("\n=== Rust Debugging: Calling `load_personality()` ===")
        print("📤 Input Traits:", json.dumps(input_traits, indent=2))
        print("📥 Default Traits:", json.dumps(self.default_traits_dict, indent=2))

        try:
            # ✅ Call Rust function
            result = load_personality(json.dumps(input_traits))
            print("✅ Rust Function Output:", json.dumps(result, indent=2))

            # 🔥 ✅ Check only expected fields, ignore extra fields
            for key, expected_value in expected_updates.items():
                self.assertEqual(result[key], expected_value, f"Mismatch on key: {key}")

        except Exception as e:
            print("\n❌ Rust function failed:", str(e))
            self.fail(f"Rust function failed unexpectedly: {str(e)}")


'''
if __name__ == "__main__":
    unittest.main()
'''
