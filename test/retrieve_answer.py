import os
import json
import psycopg2
from typing import List, Dict, Any
from langchain_community.vectorstores.pgvector import PGVector, DistanceStrategy
# OllamaEmbeddings is dec=precated when imported from langchain_community
# from langchain_community.embeddings import OllamaEmbeddings
from langchain_ollama import OllamaEmbeddings
from dotenv import load_dotenv


#### UTILITY FUNCTIONS & CONF. VARS
# load env vars
load_dotenv(dotenv_path='../.env', override=False)
load_dotenv(dotenv_path="../.vars", override=True)

# Use Ollama to create embeddings
# in the OllamaEmbeddings class, temperature parameter is not supported anymore
embeddings = OllamaEmbeddings(model="mistral:7b") # temperature=float(os.getenv("EMBEDDINGS_TEMPERATURE")))

CONNECTION_STRING = PGVector.connection_string_from_db_params(
    driver=os.getenv("DRIVER"), # psycopg2
    host=os.getenv("DBHOST"),
    port=int(os.getenv("DBPORT")),
    database=os.getenv("DBNAME"),
    user=os.getenv("DBUSER"),
    password=os.getenv("DBPASSWORD"),
)

# we use document_title as collection name as it will be used by business user on his side when creating embedding
# this makes the search more targeted and accurate as it will fetch only from targeted area of embeddings
COLLECTION_NAME = os.getenv("DOCUMENT_TITLE")


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

def retrieval_view_response_transmit(retrieval_graph_output_json_loads, list_answers, list_errors):
  # handle errors
  for err in list_errors:
    if err in retrieval_json:
      response = json.dumps({ err: retrieval_json[err]})
      return response
  # handle answers
  for answer in list_answers:
    if answer in retrieval_json:
      response = json.dumps({answer: retrieval_json[answer]})
      return response
