import unittest
from unittest.mock import patch
from agents.app_utils.formatters import string_to_dict, collection_normalize_name


class TestFormatters(unittest.TestCase):

    def test_string_to_dict_valid_json(self):
        """Test string_to_dict with valid JSON string."""
        json_string = '{"KeyOne": "Value1", "KeyTwo": 2, "keyThree": true}'
        expected_dict = {"keyone": "Value1", "keytwo": 2, "keythree": True}

        result = string_to_dict(json_string)
        self.assertEqual(result, expected_dict)

    def test_string_to_dict_invalid_json(self):
        """Test string_to_dict with an invalid JSON string, expecting a ValueError."""
        invalid_json_string = '{"keyOne": "Value1", "keyTwo": 2, keyThree: true}'  # Missing quotes around `keyThree`

        with self.assertRaises(ValueError) as context:
            string_to_dict(invalid_json_string)

        self.assertIn("Error converting string to dictionary", str(context.exception))

    @patch("agents.app_utils.formatters.collection_normalize_name_py")
    def test_collection_normalize_name(self, mock_rust_function):
        """Test collection_normalize_name using the Rust counterpart."""
        mock_rust_function.return_value = "normalized-collection"

        input_name = "  My Collection Name  "
        expected_output = "normalized-collection"

        result = collection_normalize_name(input_name)

        # Ensure mock was called with the exact argument
        mock_rust_function.assert_called_once_with(input_name)  # No `.strip()`
        self.assertEqual(result, expected_output)

'''
if __name__ == "__main__":
    unittest.main()
'''
