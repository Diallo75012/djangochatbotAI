import unittest
from unittest.mock import MagicMock, patch
from langchain_core.messages import AIMessage
from agents.app_utils.call_llm import call_llm
from agents.prompts.prompts import analyse_user_query_safety_prompt
from agents.structured_output.structured_output import analyse_user_query_safety_schema


class TestCallLLM(unittest.TestCase):

    @patch("agents.app_utils.call_llm.ChatGroq")
    def test_call_llm_no_exceptions_occur(self, mock_chat_groq):
        """Ensure call_llm never returns an error and always provides valid structured output."""
        mock_model = MagicMock()
        mock_chat_groq.return_value = mock_model

        # Simulate an API failure response
        mock_model.invoke.side_effect = Exception("API Error")

        query = "How are manga kissa in Japan?"
        prompt_template_part = analyse_user_query_safety_prompt["system"]["template"]
        schema = analyse_user_query_safety_schema

        # Call function - even with an API error, it should return valid output
        result = call_llm(query, prompt_template_part, schema, mock_model)

        # Assert that no 'error' key exists because the function is perfect
        self.assertNotIn("error", result, "call_llm should never return an error key!")

        # Assert that the function still returns valid structured output
        self.assertIn("safe", result)
        self.assertIn("unsafe", result)
        self.assertIn(result["safe"], ["valid", "invalid"])
        self.assertIn(result["unsafe"], ["valid", "invalid"])

    @patch("agents.app_utils.call_llm.ChatGroq")
    def test_call_llm_always_corrects_invalid_json(self, mock_chat_groq):
        """Ensure call_llm never returns an error even when LLM outputs malformed JSON."""
        mock_model = MagicMock()
        mock_chat_groq.return_value = mock_model

        # Malformed JSON response from LLM
        mock_model.invoke.return_value = AIMessage(content="```json\n{invalid JSON}\n```")

        query = "How is climate affecting Shibuya crossing diversity?"
        prompt_template_part = analyse_user_query_safety_prompt["system"]["template"]
        schema = analyse_user_query_safety_schema

        # Call function
        result = call_llm(query, prompt_template_part, schema, mock_model)

        # Ensure that no error is returned
        self.assertNotIn("error", result, "call_llm should never return an error key!")

        # Ensure valid structured output is still returned
        self.assertIn("safe", result)
        self.assertIn("unsafe", result)
        self.assertIn(result["safe"], ["valid", "invalid"])
        self.assertIn(result["unsafe"], ["valid", "invalid"])

    @patch("agents.app_utils.call_llm.ChatGroq")
    def test_call_llm_success_markdown_response(self, mock_chat_groq):
        """Test call_llm when LLM returns structured JSON in markdown format."""
        mock_model = MagicMock()
        mock_chat_groq.return_value = mock_model

        # Mock response wrapped in markdown format
        mock_model.invoke.return_value = AIMessage(content="```json\n{\"safe\": \"valid\", \"unsafe\": \"invalid\"}\n```")

        query = "What is an Akiya in Japan?"
        prompt_template_part = analyse_user_query_safety_prompt["system"]["template"]
        schema = analyse_user_query_safety_schema

        result = call_llm(query, prompt_template_part, schema, mock_model)

        expected_result = {"safe": "valid", "unsafe": "invalid"}

        self.assertDictEqual(result, expected_result)

    @patch("agents.app_utils.call_llm.ChatGroq")
    def test_call_llm_success_plain_json(self, mock_chat_groq):
        """Test call_llm with a plain JSON response (no markdown)."""
        mock_model = MagicMock()
        mock_chat_groq.return_value = mock_model

        # Mock response with direct JSON content
        mock_model.invoke.return_value = AIMessage(content='{"safe": "valid", "unsafe": "invalid"}')

        query = "How can I register a business in Japan as a foreigner?"
        prompt_template_part = analyse_user_query_safety_prompt["system"]["template"]
        schema = analyse_user_query_safety_schema

        result = call_llm(query, prompt_template_part, schema, mock_model)

        expected_result = {"safe": "valid", "unsafe": "invalid"}

        self.assertDictEqual(result, expected_result)

'''
if __name__ == "__main__":
    unittest.main()
'''
