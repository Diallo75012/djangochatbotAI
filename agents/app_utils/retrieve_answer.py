import os
import json
import psycopg2
from typing import List, Dict, Any
from langchain_community.vectorstores.pgvector import PGVector, DistanceStrategy
from langchain_community.embeddings import OllamaEmbeddings
from dotenv import load_dotenv


#### UTILITY FUNCTIONS & CONF. VARS
# load env vars
load_dotenv(dotenv_path='.env', override=False)
load_dotenv(dotenv_path=".vars", override=True)

# Use Ollama to create embeddings
embeddings = OllamaEmbeddings(model="mistral:7b", temperature=float(os.getenv("EMBEDDINGS_TEMPERATURE")))

CONNECTION_STRING = PGVector.connection_string_from_db_params(
    driver=os.getenv("DRIVER"),
    host=os.getenv("DBHOST"),
    port=int(os.getenv("DBPORT")),
    database=os.getenv("DBNAME"),
    user=os.getenv("DBUSER"),
    password=os.getenv("DBPASSWORD"),
)
COLLECTION_NAME = os.getenv("COLLECTION_NAME")


def vector_db_retrieve(collection: str, connection: str, embedding: OllamaEmbeddings) -> PGVector:
  """Retrieve the vector database instance."""
  return PGVector(
    collection_name=collection,
    connection_string=connection,
    embedding_function=embedding,
  )

def retrieve_relevant_vectors(query: str, top_n: int = 3) -> List[Dict[str, Any]]:
  """Retrieve the most relevant vectors from PGVector."""
  db = vector_db_retrieve(COLLECTION_NAME, CONNECTION_STRING, embeddings)

  docs_and_similarity_score = db.similarity_search_with_score(query)
  print("Type docs_and_similarity_score: ", type(docs_and_similarity_score), "\nContent: ", docs_and_similarity_score)
  results = []

  # Iterate over each tuple in the result
  for doc, score in docs_and_similarity_score[:top_n]:
    # Parse the JSON content from the Document
    data = json.loads(doc.page_content)

    # Iterate through the parsed JSON data to extract relevant info
    for info in data:
      # Append the extracted info to the results list
      '''
      HERE WE WILL NEED TO ADJUST IT DEPENDING OF THE DOC FORMATING WHEN EMBEDDING
      '''
      results.append({'question': info['question'], 'answer': info['answer'], 'score': score})

  return results


#########################################
### JUST EXPORT THIS ONE TO RETRIEVE ####
#########################################
def answer_retriever(query: str, relevance_score: float, top_n: int) -> List[Dict[str, Any]]:
  """Retrieve answers using PGVector"""
  relevant_vectors = retrieve_relevant_vectors(query, top_n)
  print("Type relevant_vectors: ", type(relevant_vectors), "\nContent: ", relevant_vectors)
  results = []
  for vector in relevant_vectors:
    if vector["score"] > relevance_score:
      print("Vector: ", vector, ", Vectore score: ", vector["score"], f" vs relevant score: {relevance_score}")
      print("Vector: ", vector)
      results.append({
        'question': vector['question'],
        'answer': vector['answer'],
        'score': vector['score'],
      })
  return results
