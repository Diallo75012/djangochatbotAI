from django.test import SimpleTestCase
from django.urls import reverse, resolve
from agents import views

class TestAgentsURLs(SimpleTestCase):

    def test_retrieve_data_url_resolves(self):
        """Test if 'retrieve-data' URL resolves to the correct view."""
        url = reverse('agents:retrieve-data')
        self.assertEqual(resolve(url).func, views.retrieveData)

    def test_embed_data_url_resolves(self):
        """Test if 'embed-data' URL resolves to the correct view."""
        url = reverse('agents:embed-data', args=[1])  # Example primary key (1)
        self.assertEqual(resolve(url).func, views.embedData)

    def test_delete_embedding_collection_url_resolves(self):
        """Test if 'delete-embedding-collection' URL resolves to the correct view."""
        url = reverse('agents:delete-embedding-collection', args=[1])  # Example primary key (1)
        self.assertEqual(resolve(url).func, views.deleteEmbeddingCollection)

