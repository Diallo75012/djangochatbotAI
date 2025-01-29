import unittest
import json
import sys
from unittest.mock import patch
from agents.app_utils.json_dumps_manager import safe_json_dumps


class TestJsonDumpsManager(unittest.TestCase):

    def test_safe_json_dumps_valid(self):
        """Test safe_json_dumps correctly serializes valid JSON objects."""
        data = {"name": "AI", "age": 3}
        expected_output = json.dumps(data, indent=4)

        result = safe_json_dumps(data)

        self.assertEqual(result, expected_output)

    @patch("sys.stderr")
    def test_safe_json_dumps_non_serializable(self, mock_stderr):
        """Test safe_json_dumps handles non-serializable objects gracefully."""

        class NonSerializable:
            pass

        non_serializable_obj = NonSerializable()
        result = safe_json_dumps(non_serializable_obj)

        self.assertIsInstance(result, str)
        self.assertIn("object", result)  # Should contain string representation of the object
        mock_stderr.write.assert_called()  # Ensure error logging happens

    def test_safe_json_dumps_list(self):
        """Test safe_json_dumps with a list of dictionaries."""
        data = [{"key1": "value1"}, {"key2": "value2"}]
        expected_output = json.dumps(data, indent=4)

        result = safe_json_dumps(data)

        self.assertEqual(result, expected_output)

    def test_safe_json_dumps_string(self):
        """Test safe_json_dumps with a plain string input."""
        data = "This is a test string."
        expected_output = json.dumps(data, indent=4)

        result = safe_json_dumps(data)

        self.assertEqual(result, expected_output)

'''
if __name__ == "__main__":
    unittest.main()
'''
