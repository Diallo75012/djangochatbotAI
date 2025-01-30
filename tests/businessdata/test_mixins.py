import unittest
import json
from django.core.exceptions import ValidationError
from businessdata.mixins import JSONFieldValidationMixin


class TestJSONFieldValidationMixin(unittest.TestCase):

    class MockForm(JSONFieldValidationMixin):
        """Mock form to simulate Django's form behavior with cleaned_data."""
        def __init__(self, cleaned_data):
            self.cleaned_data = cleaned_data

    def test_clean_question_answer_data_valid_dict(self):
        """Test validation with a valid dictionary input."""
        form = self.MockForm({"question_answer_data": {"Q1": "A1", "Q2": "A2"}})
        result = form.clean_question_answer_data()
        expected = {"Q1": "A1", "Q2": "A2"}
        self.assertEqual(result, expected)

    def test_clean_question_answer_data_valid_json_string(self):
        """Test validation with a valid JSON string input."""
        json_string = '{"Q1": "A1", "Q2": "A2"}'
        form = self.MockForm({"question_answer_data": json_string})
        result = form.clean_question_answer_data()
        expected = json.loads(json_string)
        self.assertEqual(result, expected)

    def test_clean_question_answer_data_invalid_json_string(self):
        """Test validation failure with an invalid JSON string."""
        invalid_json_string = '{"Q1": "A1", "Q2": "A2"'  # Missing closing bracket
        form = self.MockForm({"question_answer_data": invalid_json_string})

        with self.assertRaises(ValidationError) as context:
            form.clean_question_answer_data()
        
        self.assertIn("Invalid JSON format", str(context.exception))

    def test_clean_question_answer_data_none_input(self):
        """Test validation failure when question_answer_data is None."""
        form = self.MockForm({"question_answer_data": None})

        with self.assertRaises(ValidationError) as context:
            form.clean_question_answer_data()
        
        self.assertIn("No data provided for question_answer_data", str(context.exception))

    def test_clean_question_answer_data_non_json_string(self):
        """Test validation failure when input is a non-JSON string."""
        non_json_string = "Just a normal string, not JSON."
        form = self.MockForm({"question_answer_data": non_json_string})

        with self.assertRaises(ValidationError) as context:
            form.clean_question_answer_data()
        
        self.assertIn("Invalid JSON format", str(context.exception))

'''
if __name__ == "__main__":
    unittest.main()
'''
