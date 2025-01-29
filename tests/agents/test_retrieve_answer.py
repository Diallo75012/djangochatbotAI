import unittest
from unittest.mock import patch, MagicMock
import json
import os
from langgraph.graph import MessagesState
from langchain.docstore.document import Document
from agents.app_utils.retrieve_answer import (
    retrieve_answer_action,
    answer_retriever,
    retrieve_relevant_vectors
)


class TestRetrieveAnswer(unittest.TestCase):

    @patch("agents.app_utils.retrieve_answer.PGVector")
    @patch("agents.app_utils.retrieve_answer.OllamaEmbeddings")
    def test_retrieve_relevant_vectors_success(self, mock_embeddings, mock_pgvector):
        """Test retrieving relevant vectors successfully."""
        # Mock PGVector instance
        mock_pg_instance = MagicMock()
        mock_pgvector.return_value = mock_pg_instance

        # Mock similarity_search_with_score return value
        mock_doc = Document(page_content="Test content", metadata={"answer": "Test Answer", "question": "Test Question"})
        mock_pg_instance.similarity_search_with_score.return_value = [(mock_doc, 0.8)]

        # Call function
        result = retrieve_relevant_vectors("test query", top_n=1)

        # Assertions
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]["answer"], "Test Answer")
        self.assertEqual(result[0]["question"], "Test Question")
        self.assertEqual(result[0]["score"], 0.8)

    @patch("agents.app_utils.retrieve_answer.retrieve_relevant_vectors")
    def test_answer_retriever_success(self, mock_retrieve_vectors):
        """Test answer retrieval with valid vectors."""
        mock_retrieve_vectors.return_value = [
            {"answer": "Relevant answer", "score": 0.7, "question": "Sample question"}
        ]

        result = answer_retriever("test query", relevance_score=0.5, top_n=1)

        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]["answer"], "Relevant answer")
        self.assertEqual(result[0]["question"], "Sample question")

    @patch("agents.app_utils.retrieve_answer.answer_retriever")
    @patch("agents.app_utils.retrieve_answer.os.getenv")
    def test_retrieve_answer_action_success(self, mock_getenv, mock_answer_retriever):
        """Test retrieve_answer_action returns structured results."""
        # Mock environment variables
        mock_getenv.side_effect = lambda key: {
            "REPHRASED_USER_QUERY": "test query",
            "SCORE063": "0.63",
            "SCORE055": "0.55",
            "TOP_N": "1"
        }.get(key, None)

        # Mock vector retrieval response
        mock_answer_retriever.side_effect = [
            [{"answer": "Best answer", "score": 0.7, "question": "Test question"}],  # First retrieval
            [{"answer": "Other question", "score": 0.6, "question": "Alternative"}]  # Second retrieval
        ]

        state = MessagesState()
        result = retrieve_answer_action(state)

        # Parse JSON response
        response_content = json.loads(result["messages"][0]["content"])
        self.assertIn("answers", response_content)
        self.assertEqual(response_content["answers"]["score_063"], "Best answer")
        self.assertEqual(response_content["answers"]["score_055"], "Alternative")

    @patch("agents.app_utils.retrieve_answer.answer_retriever", return_value=[])
    @patch("agents.app_utils.retrieve_answer.os.getenv")
    def test_retrieve_answer_action_no_results(self, mock_getenv, mock_answer_retriever):
        """Test retrieve_answer_action returns 'nothing' when no results are found."""
        mock_getenv.side_effect = lambda key: {
            "REPHRASED_USER_QUERY": "test query",
            "SCORE063": "0.63",
            "SCORE055": "0.55",
            "TOP_N": "1"
        }.get(key, None)

        state = MessagesState()
        result = retrieve_answer_action(state)

        response_content = json.loads(result["messages"][0]["content"])
        self.assertIn("nothing", response_content)

'''
if __name__ == "__main__":
    unittest.main()
'''
