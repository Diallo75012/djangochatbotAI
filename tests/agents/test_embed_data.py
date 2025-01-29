import unittest
from unittest.mock import patch, MagicMock
from langchain.docstore.document import Document
from agents.app_utils.embed_data import vector_db_create


class TestEmbedData(unittest.TestCase):

    @patch("agents.app_utils.embed_data.PGVector")
    @patch("agents.app_utils.embed_data.OllamaEmbeddings")
    def test_vector_db_create_success(self, mock_embeddings, mock_pgvector):
        """Test vector_db_create successfully stores embeddings in PGVector."""
        # Mock PGVector instance
        mock_pg_instance = MagicMock()
        mock_pgvector.return_value = mock_pg_instance

        # Mock embeddings instance
        mock_embeddings_instance = MagicMock()
        mock_embeddings.return_value = mock_embeddings_instance

        # Create a mock document
        mock_doc = Document(
            page_content="Sample document content",
            metadata={"id": "123"}
        )

        # Call function
        result = vector_db_create([mock_doc])

        # Assertions
        self.assertEqual(result, {"success": "Data correctly embedded!"})
        mock_pgvector.assert_called_once()  # Ensures PGVector was initialized
        mock_pg_instance.add_documents.assert_called_once()  # Ensures add_documents was called

    @patch("agents.app_utils.embed_data.PGVector", side_effect=Exception("DB Connection Error"))
    def test_vector_db_create_failure(self, mock_pgvector):
        """Test vector_db_create handles errors correctly."""
        mock_doc = Document(
            page_content="Sample document content",
            metadata={"id": "123"}
        )

        result = vector_db_create([mock_doc])

        self.assertIsInstance(result, Exception)
        self.assertEqual(str(result), "DB Connection Error")

'''
if __name__ == "__main__":
    unittest.main()
'''
