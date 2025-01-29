import unittest
from unittest.mock import patch
from agents.app_utils.token_count_helper import token_counter


class TestTokenCountHelper(unittest.TestCase):

    @patch("agents.app_utils.token_count_helper.token_counter_py")
    def test_token_counter_success(self, mock_rust_token_counter):
        """Test token counting when Rust function works correctly."""
        mock_rust_token_counter.return_value = 42  # Simulated token count

        text_input = "This is a test string."
        result = token_counter(text_input)

        self.assertEqual(result, 42)
        mock_rust_token_counter.assert_called_once_with(text_input)

    @patch("agents.app_utils.token_count_helper.token_counter_py", side_effect=Exception("Rust function failed"))
    def test_token_counter_failure(self, mock_rust_token_counter):
        """Test token counting when Rust function raises an exception."""
        text_input = "This is a test string."
        result = token_counter(text_input)

        self.assertTrue(result.startswith("An error occured while trying to count tokens from rust helper:"))
        mock_rust_token_counter.assert_called_once_with(text_input)

'''
if __name__ == "__main__":
    unittest.main()
'''
