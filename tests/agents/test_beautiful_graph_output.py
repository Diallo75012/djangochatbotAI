import unittest
import json
from agents.app_utils.beautiful_graph_output import message_to_dict
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage, ToolMessage


class TestBeautifulGraphOutput(unittest.TestCase):

    def setUp(self):
        """Create mock LangChain messages with FIXED validation."""
        self.mock_tool_msg = ToolMessage(
            content="Tool response",
            additional_kwargs={},
            response_metadata={},  # ✅ FIX: Ensure dict
            tool_calls=[],
            usage_metadata=None,
            tool_call_id="tool_123"  # ✅ FIX: Add required `tool_call_id`
        )
        self.mock_tool_msg.id = "321"
        self.mock_tool_msg.role = "tool"

    def test_message_to_dict_tool_message(self):
        """Test ToolMessage conversion to dict (includes tool_call_id)."""
        expected_output = {
            "content": "Tool response",
            "additional_kwargs": {},
            "response_metadata": {},  # ✅ FIX: Ensure dict
            "tool_calls": [],
            "usage_metadata": None,
            "id": "321",
            "role": "tool",
            "tool_call_id": "tool_123"  # ✅ FIX: Ensure `tool_call_id` is included
        }
        result = message_to_dict(self.mock_tool_msg)
        print("\n=== ToolMessage Debugging ===")
        print("Expected:", json.dumps(expected_output, indent=2))
        print("Actual:", json.dumps(result, indent=2))

        self.assertEqual(result, expected_output)

'''
if __name__ == "__main__":
    unittest.main()
'''
