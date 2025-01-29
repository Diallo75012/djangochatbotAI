import unittest
from agents.app_utils.prompt_creation import prompt_creation


class TestPromptCreation(unittest.TestCase):

    def test_prompt_creation_with_variables(self):
        """Test prompt creation with a template containing input variables."""
        prompt_dict = {
            "template": "Hello {name}, welcome to {place}!",
            "input_variables": ["name", "place"]
        }
        kwargs = {"name": "Alice", "place": "Tokyo"}
        expected_output = "Hello Alice, welcome to Tokyo!"

        result = prompt_creation(prompt_dict, **kwargs)
        self.assertEqual(result, expected_output)

    def test_prompt_creation_without_variables(self):
        """Test prompt creation when no input variables are defined."""
        prompt_dict = {
            "template": "This is a static message.",
            "input_variables": []
        }
        expected_output = "This is a static message."

        result = prompt_creation(prompt_dict)
        self.assertEqual(result, expected_output)

    def test_prompt_creation_missing_template_key(self):
        """Test prompt creation when the 'template' key is missing."""
        prompt_dict = {
            "input_variables": ["name"]
        }

        with self.assertRaises(KeyError):
            prompt_creation(prompt_dict, name="Alice")

    def test_prompt_creation_missing_input_variable(self):
        """Test prompt creation when an expected input variable is not provided in kwargs."""
        prompt_dict = {
            "template": "Hello {name}, welcome!",
            "input_variables": ["name"]
        }

        with self.assertRaises(KeyError):
            prompt_creation(prompt_dict)  # Missing `name` argument

'''
if __name__ == "__main__":
    unittest.main()
'''
