import unittest
import json
from agents.app_utils.beautiful_graph_output import message_to_dict, beautify_output
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage, ToolMessage


class TestBeautifulGraphOutput(unittest.TestCase):

    def setUp(self):
        """Mock LangChain MessagesState outputs for different cases."""

        # ✅ AI Message Mock (AI Assistant Response)
        self.mock_ai_msg = AIMessage(
            content="Hello, I am an AI.",
            additional_kwargs={},
            response_metadata={},
            tool_calls=[],
            usage_metadata={
                "input_tokens": 10,
                "output_tokens": 20,
                "total_tokens": 30
            }
        )
        self.mock_ai_msg.id = "ai_001"
        self.mock_ai_msg.role = "ai"

        # ✅ Human Message Mock (User's Input)
        self.mock_human_msg = HumanMessage(
            content="Hello AI, how are you?",
            additional_kwargs={},
            response_metadata={},
            tool_calls=[],
            usage_metadata={"input_tokens": 5, "output_tokens": 0, "total_tokens": 5}
        )
        self.mock_human_msg.id = "user_001"
        self.mock_human_msg.role = "human"

        # ✅ System Message Mock (System Instructions)
        self.mock_system_msg = SystemMessage(
            content="System initialized.",
            additional_kwargs={},
            response_metadata={},
            tool_calls=[],
            usage_metadata={"input_tokens": 2, "output_tokens": 0, "total_tokens": 2}
        )
        self.mock_system_msg.id = "sys_001"
        self.mock_system_msg.role = "system"

        # ✅ Tool Message Mock (Simulating a LangGraph Tool Call)
        self.mock_tool_msg = ToolMessage(
            content="Tool response",
            response_metadata={},
            tool_calls=[],
            usage_metadata={"input_tokens": 15, "output_tokens": 10, "total_tokens": 25},
            tool_call_id="tool_123"
        )
        self.mock_tool_msg.id = "tool_001"
        self.mock_tool_msg.role = "tool"

    def test_message_to_dict_ai_message(self):
        """Test conversion of AIMessage to dictionary."""

        expected_output = {
            "content": "Hello, I am an AI.",
            "additional_kwargs": {},
            "response_metadata": {},
            "tool_calls": [],
            "usage_metadata": {
                "input_tokens": 10,
                "output_tokens": 20,
                "total_tokens": 30
            },
            "id": "ai_001",
            "role": "ai"
        }

        result = message_to_dict(self.mock_ai_msg)
        self.assertEqual(result, expected_output)

    def test_message_to_dict_human_message(self):
        """Test conversion of HumanMessage to dictionary."""

        expected_output = {
            "content": "Hello AI, how are you?",
            "additional_kwargs": {},
            "response_metadata": {},
            "tool_calls": [],
            "usage_metadata": {
                "input_tokens": 5,
                "output_tokens": 0,
                "total_tokens": 5
            },
            "id": "user_001",
            "role": "human"
        }

        result = message_to_dict(self.mock_human_msg)
        self.assertEqual(result, expected_output)

    def test_message_to_dict_system_message(self):
        """Test conversion of SystemMessage to dictionary."""

        expected_output = {
            "content": "System initialized.",
            "additional_kwargs": {},
            "response_metadata": {},
            "tool_calls": [],
            "usage_metadata": {
                "input_tokens": 2,
                "output_tokens": 0,
                "total_tokens": 2}
            ,
            "id": "sys_001",
            "role": "system"
        }

        result = message_to_dict(self.mock_system_msg)
        self.assertEqual(result, expected_output)

    def test_message_to_dict_tool_message(self):
        """Test conversion of ToolMessage (Simulating LangGraph Tool Call)."""
        result = message_to_dict(self.mock_tool_msg)

        expected_output = {
            "content": "Tool response",
            "additional_kwargs": {},
            "response_metadata": {},
            "tool_calls": [],
            "usage_metadata": {
                "input_tokens": 15,
                "output_tokens": 10,
                "total_tokens": 25
            },
            "id": "tool_001",
            "role": "tool",
        }

        self.assertEqual(result, expected_output)

    def test_beautify_output(self):
        """Test beautify_output() for formatting multiple messages."""

        input_data = [self.mock_ai_msg, self.mock_human_msg, self.mock_system_msg, self.mock_tool_msg]
        expected_output = json.dumps(
            [
                message_to_dict(self.mock_ai_msg),
                message_to_dict(self.mock_human_msg),
                message_to_dict(self.mock_system_msg),
                message_to_dict(self.mock_tool_msg)
            ],
            indent=4
        )

        result = beautify_output(input_data)
        self.assertEqual(result, expected_output)
