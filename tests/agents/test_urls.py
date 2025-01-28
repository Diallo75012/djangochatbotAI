from django.urls import reverse, resolve
from agents import views

def test_retrieve_data_url():
    """
    Test that the 'retrieve-data' URL is correctly mapped to the retrieveData view.
    """
    url = reverse('agents:retrieve-data')
    assert resolve(url).func == views.retrieveData

def test_embed_data_url():
    """
    Test that the 'embed-data' URL is correctly mapped to the embedData view.
    """
    url = reverse('agents:embed-data', kwargs={'pk': 1})
    assert resolve(url).func == views.embedData

def test_delete_embedding_collection_url():
    """
    Test that the 'delete-embedding-collection' URL is correctly mapped to the deleteEmbeddingCollection view.
    """
    url = reverse('agents:delete-embedding-collection', kwargs={'pk': 1})
    assert resolve(url).func == views.deleteEmbeddingCollection
