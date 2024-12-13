import os
import json
import psycopg2
import math
from typing import List, Dict, Any
from langgraph.graph import MessagesState
#from langchain_community.vectorstores.pgvector import PGVector, DistanceStrategy
from langchain_postgres.vectorstores import PGVector, DistanceStrategy
# OllamaEmbeddings is dec=precated when imported from langchain_community
# from langchain_community.embeddings import OllamaEmbeddings
from langchain_ollama import OllamaEmbeddings
from dotenv import load_dotenv


#### UTILITY FUNCTIONS & CONF. VARS
# load env vars
load_dotenv(dotenv_path='../.env', override=False)
load_dotenv(dotenv_path="../.vars.env", override=True)

# Use Ollama to create embeddings
# in the OllamaEmbeddings class, temperature parameter is not supported anymore
embeddings = OllamaEmbeddings(model="mistral:7b") # temperature=float(os.getenv("EMBEDDINGS_TEMPERATURE")))

'''
CONNECTION_STRING = PGVector.connection_string_from_db_params(
    driver=os.getenv("DRIVER"), # psycopg2
    host=os.getenv("DBHOST"),
    port=int(os.getenv("DBPORT")),
    database=os.getenv("DBNAME"),
    user=os.getenv("DBUSER"),
    password=os.getenv("DBPASSWORD"),
)
'''
# db connection vars
driver=os.getenv("DRIVER") # not psycopg2 as now it required psycopg3 (we install both: pip install psycopg2 psycopg)
host=os.getenv("DBHOST")
port=int(os.getenv("DBPORT"))
database=os.getenv("DBNAME")
user=os.getenv("DBUSER")
password=os.getenv("DBPASSWORD")
CONNECTION_STRING = f"postgresql+{driver}://{user}:{password}@{host}:{port}/{database}"

# we use document_title as collection name as it will be used by business user on his side when creating embedding
# this makes the search more targeted and accurate as it will fetch only from targeted area of embeddings
COLLECTION_NAME = os.getenv("DOCUMENT_TITLE")


def vector_db_retrieve(collection: str, connection: str, embedding: OllamaEmbeddings) -> PGVector:
  """Retrieve the vector database instance."""
  return PGVector(
    collection_name=collection,
    connection=connection,
    embeddings=embedding,
  )

def retrieve_relevant_vectors(query: str, top_n: int = 3) -> List[Dict[str, Any]]:
  """Retrieve the most relevant vectors from PGVector."""
  db = vector_db_retrieve(COLLECTION_NAME, CONNECTION_STRING, embeddings)

  docs_and_similarity_score = db.similarity_search_with_score(query)
  print("Type docs_and_similarity_score: ", type(docs_and_similarity_score), "\nContent: ", docs_and_similarity_score)
  results = []

  # Iterate over each tuple in the result
  for doc, score in docs_and_similarity_score[:top_n]:
    # Skip entries with NaN scores
    if score is None or math.isnan(score):
      print(f"Skipping document with NaN score: {doc.metadata}")
      continue

    print("Score: ", score)

    try:
      # Parse the JSON content from the Document
      data = json.loads(doc.page_content)
    except json.JSONDecodeError as e:
      print(f"Error parsing page_content for document {doc.metadata['id']}: {e}")
      continue

    # Iterate through the parsed JSON data to extract relevant info
    for info in data:
      # Append the extracted info to the results list
      results.append({'question': info['question'], 'answer': info['answer'], 'score': score})

  print("Results from retrieve_relevant_vectors: ", results)
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
    if vector["score"] != None:
      print("Vector score: ", vector["score"])
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

##########################################################
### INSTEAD USE THIS ONE FUNCTION TO PERFORM RETRIEVAL ###
##########################################################
#def retrieve_answer_action(query: str, state: MessagesState = MessagesState()):
def retrieve_answer_action():
  """
  Retrieves best answer for user query from the vector database

  Parameter:
  query: str = user question

  returns:
  retrieved answer for that specific user question
  """
  # vars
  query: str = os.getenv("REPHRASED_USER_QUERY")
  # we will perform two retrieval with different scores
  score063: float = float(os.getenv("SCORE064"))
  score055: float = float(os.getenv("SCORE055"))
  top_n: int = int(os.getenv("TOP_N"))
  vector_responses: dict = {}

  # Perform vector search with score if semantic search is not relevant
  try:
    vector_response_063 = answer_retriever(query, score063, top_n)
    print("JSON RESPONSE 063: ", json.dumps(vector_response_063, indent=2))
    '''
      # Returns
      {
        'question': vector['question'],
        'answer': vector['answer'],
        'score': vector['score'],
      }
    '''
    if vector_response_063:
      # update to vector_response
      vector_responses["score_063"] = vector_response_063

  except Exception as e:
    print(f"An error occured while trying to perform vectordb search 063 query {e}")
    return e
    #return {"messages": [{"role": "ai", "content": json.dumps({"error_vector": f"An error occured while trying to perform vectordb search 063 query: {e}"})}]}

  try:
    vector_response_055 = answer_retriever(query, score055, top_n)
    print("JSON RESPONSE 055: ", json.dumps(vector_response_055, indent=2))
    if vector_response_055:
      # update to vector_response
      vector_responses["score_055"] = vector_response_055
  except Exception as e:
    print(f"An error occured while trying to perform vectordb search 055 query {e}")
    return e
    #return {"messages": [{"role": "ai", "content": json.dumps({"error_vector": f"An error occured while trying to perform vectordb search 055 query: {e}"})}]}

  if vector_responses:
    print("Vector responses: ", vector_responses)
    return vector_responses
    #return {"messages": [{"role": "ai", "content": json.dumps(vector_responses)}]} 
  else:
    # If no relevant result found, return a default response, and perform maybe after that an internet search and cache the query and the response
    return "nothingu"
    # return {"messages": [{"role": "ai", "content": json.dumps({"nothing": "nothing_in_cache_nor_vectordb"})}]}

print(retrieve_answer_action())
