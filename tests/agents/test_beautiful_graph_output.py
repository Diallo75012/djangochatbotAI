import json
import pytest
from agents.app_utils.beautiful_graph_output import (
    convert_to_serializable,
    beautify_output,
    message_to_dict,
)
from langchain_core.messages import (
    AIMessage,
    BaseMessage,
    HumanMessage,
    SystemMessage,
    ToolMessage
)

def test_message_to_dict_aimessage():
    message = AIMessage(content="test content", additional_kwargs={"test_key": "test_value"}, response_metadata={"test_metadata_key": "test_metadata_value"}, tool_calls=[])
    expected_dict = {
        "content": "test content",
        "additional_kwargs": {"test_key": "test_value"},
        "response_metadata": {"test_metadata_key": "test_metadata_value"},
        "tool_calls": [],
        "usage_metadata": None,
        "id": None,
        "role": "ai",
    }
    assert message_to_dict(message) == expected_dict

def test_message_to_dict_humanmessage():
    message = HumanMessage(content="test content", additional_kwargs={"test_key": "test_value"}, response_metadata={"test_metadata_key": "test_metadata_value"}, tool_calls=[])
    expected_dict = {
        "content": "test content",
        "additional_kwargs": {"test_key": "test_value"},
        "response_metadata": {"test_metadata_key": "test_metadata_value"},
        "tool_calls": [],
        "usage_metadata": None,
        "id": None,
        "role": "human",
    }
    assert message_to_dict(message) == expected_dict

def test_message_to_dict_systemmessage():
    message = SystemMessage(content="test content", additional_kwargs={"test_key": "test_value"}, response_metadata={"test_metadata_key": "test_metadata_value"})
    expected_dict = {
        "content": "test content",
        "additional_kwargs": {"test_key": "test_value"},
        "response_metadata": {"test_metadata_key": "test_metadata_value"},
        "tool_calls": None,
        "usage_metadata": None,
        "id": None,
        "role": "system",
    }
    assert message_to_dict(message) == expected_dict

def test_message_to_dict_toolmessage():
    message = ToolMessage(content="test content", additional_kwargs={"test_key": "test_value"}, tool_call_id="test_tool_call_id", response_metadata={"test_metadata_key": "test_metadata_value"})
    expected_dict = {
        "content": "test content",
        "additional_kwargs": {"test_key": "test_value"},
        "response_metadata": {"test_metadata_key": "test_metadata_value"},
        "tool_calls": None,
        "usage_metadata": None,
        "id": None,
        "role": "tool",
    }
    assert message_to_dict(message) == expected_dict

def test_convert_to_serializable_list():
    data = [1, "string", {"key": "value"}]
    expected_data = [1, "string", {"key": "value"}]
    assert convert_to_serializable(data) == expected_data

def test_convert_to_serializable_dict():
    data = {"key1": 1, "key2": "string", "key3": {"nested_key": "nested_value"}}
    expected_data = {"key1": 1, "key2": "string", "key3": {"nested_key": "nested_value"}}
    assert convert_to_serializable(data) == expected_data

def test_convert_to_serializable_messages():
    ai_message = AIMessage(content="ai content", additional_kwargs={"ai_key": "ai_value"}, response_metadata={"test_metadata_key": "test_metadata_value"}, tool_calls=[])
    human_message = HumanMessage(content="human content", additional_kwargs={"human_key": "human_value"}, response_metadata={"test_metadata_key": "test_metadata_value"}, tool_calls=[])
    data = [ai_message, human_message]
    expected_data = [
        {
            "content": "ai content",
            "additional_kwargs": {"ai_key": "ai_value"},
            "response_metadata": {"test_metadata_key": "test_metadata_value"},
            "tool_calls": [],
            "usage_metadata": None,
            "id": None,
            "role": "ai",
        },
        {
            "content": "human content",
            "additional_kwargs": {"human_key": "human_value"},
             "response_metadata": {"test_metadata_key": "test_metadata_value"},
            "tool_calls": [],
            "usage_metadata": None,
            "id": None,
            "role": "human",
        }
    ]
    assert convert_to_serializable(data) == expected_data

def test_beautify_output():
    data = {"key": "value", "list": [1, 2, 3]}
    expected_output = json.dumps(data, indent=4)
    assert beautify_output(data) == expected_output
