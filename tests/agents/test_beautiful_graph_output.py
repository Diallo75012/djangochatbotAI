import unittest
import json
from unittest.mock import MagicMock
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage, ToolMessage
from agents.app_utils.beautiful_graph_output import (
    message_to_dict,
    convert_to_serializable,
    beautify_output
)


class TestBeautifulGraphOutput(unittest.TestCase):

    def setUp(self):
        """Set up mock LangGraph messages for testing."""
        self.mock_ai_msg = AIMessage(content="AI response", id="123")
        self.mock_human_msg = HumanMessage(content="User message", id="456")
        self.mock_system_msg = SystemMessage(content="System response", id="789")
        self.mock_tool_msg = ToolMessage(
            content="Tool message",
            id="000",
            tool_call_id="tool_call_001"  # Required for ToolMessage
        )

    def test_message_to_dict(self):
        """Test message_to_dict correctly serializes LangChain messages."""
        expected_output = {
            "content": "AI response",
            "additional_kwargs": {},  # Default value
            "response_metadata": {},  # Langchain uses {} instead of None
            "tool_calls": [],  # Langchain uses [] instead of None
            "usage_metadata": None,  # Explicitly set as None
            "id": "123",
            "role": "ai"  # Matches the AIMessage type field
        }
        result = message_to_dict(self.mock_ai_msg)
        self.assertDictEqual(result, expected_output)

    def test_convert_to_serializable(self):
        """Test convert_to_serializable handles LangChain messages and nested structures."""
        data = {
            "ai": self.mock_ai_msg,
            "human": [self.mock_human_msg, self.mock_system_msg]
        }
        result = convert_to_serializable(data)

        self.assertIsInstance(result, dict)
        self.assertIsInstance(result["ai"], dict)
        self.assertIsInstance(result["human"], list)
        self.assertEqual(result["ai"]["content"], "AI response")
        self.assertEqual(result["human"][0]["content"], "User message")

    def test_beautify_output(self):
        """Test beautify_output generates formatted JSON from structured data."""
        data = {
            "ai": self.mock_ai_msg,
            "human": self.mock_human_msg
        }
        result = beautify_output(data)
        parsed_json = json.loads(result)  # Ensure valid JSON

        self.assertIsInstance(parsed_json, dict)
        self.assertEqual(parsed_json["ai"]["content"], "AI response")
        self.assertEqual(parsed_json["human"]["content"], "User message")

'''
if __name__ == "__main__":
    unittest.main()
'''
