from django.urls import path, include
from . import views


app_name = 'agents'

urlpatterns = [
  # raw route to call llms already implemented in Rust
  #path('call-llm-api', views.callLlmApi, name='call-llm-api'),
  # route for embeddings to be implemeted in Rust
  #path('embed-data', views.embedData, name='EmbedData'),
  # route for retrieval to be implemented in Rust
  path('retrieve-data', views.retrieveData, name='retrieve-data'),
  # route for embedding to be done on document title(which will be collection name)
  path('embed-data/<int:pk>/', views.embedData, name='embed-data'),
  # route for data manipulation in DB to be implemented in Rust
  #path('', views., name=''),
  # route for other utils functions to be implemented in Rust

]
