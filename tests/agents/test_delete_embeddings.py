import unittest
from unittest.mock import patch
from agents.app_utils.delete_embeddings import delete_embedding_collection


class TestDeleteEmbeddings(unittest.TestCase):

    @patch("agents.app_utils.delete_embeddings.delete_collection_py")
    def test_delete_embedding_collection_success(self, mock_rust_delete):
        """Test successful deletion of an embedding collection."""
        mock_rust_delete.return_value = "Deleted successfully"

        connection_string = "postgresql://user:pass@localhost/db"
        collection_name = "test_collection"
        
        result = delete_embedding_collection(connection_string, collection_name)

        self.assertEqual(result, "success")
        mock_rust_delete.assert_called_once_with(connection_string, collection_name)

    @patch("agents.app_utils.delete_embeddings.delete_collection_py", side_effect=Exception("Rust function failed"))
    def test_delete_embedding_collection_failure(self, mock_rust_delete):
        """Test failure when Rust function raises an exception."""
        connection_string = "postgresql://user:pass@localhost/db"
        collection_name = "test_collection"

        result = delete_embedding_collection(connection_string, collection_name)

        self.assertTrue(result.startswith("error: Rust function failed"))
        mock_rust_delete.assert_called_once_with(connection_string, collection_name)

'''
if __name__ == "__main__":
    unittest.main()
'''
