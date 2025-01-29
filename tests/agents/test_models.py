import unittest
from django.test import TestCase
from agents.models import LogAnalyzer

class TestLogAnalyzerModel(TestCase):

    def test_create_log_analyzer_entry(self):
        """Test creating a LogAnalyzer model instance."""
        log_entry = LogAnalyzer.objects.create(
            chunk="Example log message",
            log_level="WARNING"
        )

        self.assertEqual(log_entry.chunk, "Example log message")
        self.assertEqual(log_entry.log_level, "WARNING")

    def test_blank_fields(self):
        """Test that blank fields are allowed as per model definition."""
        log_entry = LogAnalyzer.objects.create()

        self.assertEqual(log_entry.chunk, "")
        self.assertEqual(log_entry.log_level, "")

    def test_str_representation(self):
        """Test string representation of LogAnalyzer model."""
        log_entry = LogAnalyzer.objects.create(
            chunk="Critical system failure",
            log_level="ERROR"
        )

        expected_str = f"LogAnalyzer(chunk='Critical system failure', log_level='ERROR')"
        actual_str = f"LogAnalyzer(chunk='{log_entry.chunk}', log_level='{log_entry.log_level}')"

        self.assertEqual(actual_str, expected_str)

'''
if __name__ == "__main__":
    unittest.main()
'''
