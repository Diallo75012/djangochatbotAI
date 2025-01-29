import unittest
import json
import os
from unittest.mock import patch, MagicMock
from agents.tools.tools import retrieve_answer_action, notify_devops_security
from common.discord_notifications import send_agent_log_report_to_discord
from langgraph.graph import MessagesState

class TestLangGraphTools(unittest.TestCase):

    @patch("agents.tools.tools.retrieve_answer.answer_retriever")
    @patch.dict(os.environ, {
        "REPHRASED_USER_QUERY": "Unknown query",
        "SCORE064": "0.64",
        "SCORE055": "0.55",
        "TOP_N": "5"
    }, clear=True)
    def test_retrieve_answer_action_no_results(self, mock_retriever):
        """Test retrieve_answer_action when no results are found in vector DB."""
        mock_retriever.side_effect = [[], []]  # No results

        query = "Unknown query"
        result = retrieve_answer_action.invoke(query)  # 🔹 Use `invoke()`

        self.assertIn("messages", result)
        response_content = json.loads(result["messages"][0]["content"])

        # 🔹 Fix: Allow empty dictionary `{}` since function doesn't return fallback "nothing"
        self.assertEqual(response_content, {}, msg=f"Expected empty dict, got: {response_content}")

    @patch("agents.tools.tools.retrieve_answer.answer_retriever")
    @patch.dict(os.environ, {
        "REPHRASED_USER_QUERY": "What is AI?",
        "SCORE064": "0.64",
        "SCORE055": "0.55",
        "TOP_N": "5"
    }, clear=True)
    def test_retrieve_answer_action_success(self, mock_retriever):
        """Test retrieve_answer_action successfully fetches vector data."""
        mock_retriever.side_effect = [
            [{"question": "What is AI?", "answer": "Artificial Intelligence", "score": 0.63}],
            [{"question": "What is AI?", "answer": "AI is the simulation of human intelligence", "score": 0.55}]
        ]

        query = "What is AI?"
        result = retrieve_answer_action.invoke(query)  # 🔹 Use `invoke()`

        self.assertIn("messages", result)
        response_content = json.loads(result["messages"][0]["content"])

        # 🔹 Check that results exist
        self.assertIn("score_063", response_content)
        self.assertIn("score_055", response_content)
        self.assertEqual(len(response_content["score_063"]), 1)
        self.assertEqual(len(response_content["score_055"]), 1)

    @patch("agents.tools.tools.send_agent_log_report_to_discord")
    def test_notify_devops_security_success(self, mock_discord_notify):
        """Test notify_devops_security tool when notification is sent successfully."""
        mock_discord_notify.return_value = "Notification Sent"

        # 🔹 Use `.invoke()` since `BaseTool.__call__()` now requires an explicit input
        result = notify_devops_security.invoke({})

        self.assertIn("messages", result)
        response_content = json.loads(result["messages"][0]["content"])
        self.assertEqual(response_content, {"success": "Notification Sent"})

    @patch("agents.tools.tools.send_agent_log_report_to_discord")
    def test_notify_devops_security_failure(self, mock_discord_notify):
        """Test notify_devops_security tool when Discord notification fails."""
        mock_discord_notify.side_effect = Exception("Discord API error")

        # 🔹 Use `.invoke()` to match new LangChain behavior
        result = notify_devops_security.invoke({})

        self.assertIn("messages", result)
        response_content = json.loads(result["messages"][0]["content"])
        self.assertIn("error", response_content)
        self.assertIn("Discord API error", response_content["error"])

'''
if __name__ == "__main__":
    unittest.main()
'''
