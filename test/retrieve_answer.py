import os
import json
import psycopg2
import math
import uuid
from typing import List, Dict, Any
from langgraph.graph import MessagesState
#from langchain_community.vectorstores.pgvector import PGVector, DistanceStrategy
from langchain_postgres.vectorstores import PGVector, DistanceStrategy
# OllamaEmbeddings is dec=precated when imported from langchain_community
# from langchain_community.embeddings import OllamaEmbeddings
from langchain_ollama import OllamaEmbeddings
from dotenv import load_dotenv
from formatters import collection_normalize_name


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
    #distance_strategy=DistanceStrategy.COSINE,
    #use_jsonb=True,
  )

def retrieve_relevant_vectors(query: str, top_n: int = 3) -> List[Dict[str, Any]]:
  """Retrieve the most relevant vectors from PGVector."""
  db = vector_db_retrieve(COLLECTION_NAME, CONNECTION_STRING, embeddings)

  docs_and_similarity_score = db.similarity_search_with_score(query)
  print("Type docs_and_similarity_score: ", type(docs_and_similarity_score), "\nContent: ", docs_and_similarity_score)
  results = []

  # Iterate over each tuple in the result
  if top_n > 1:
    print("docs_and_similarity_score(if): ", docs_and_similarity_score)
    for doc, score in docs_and_similarity_score[:top_n]:
      print("Top_n > 1 -> Doc: ", doc, "\nScore: ", score, "\nDoc metadata answer: ", doc.metadata["answer"])
      # we just grab the answer from the metadata
      answer = doc.metadata["answer"]
      question = doc.metadata["question"]
      # check if there is a score, as some have score == NaN
      if math.isnan(score) != True:
        try:
          # Append to the result in a special format
          results.append({'answer': answer, 'score': score, "question": question})
        except Exception as e:
          '''
            Log error for Devops/Security team
          '''
          print(f"Error while trying to get similarity score: {e}")
          # gracefully continue don't break the app
          continue
  else:
    print("docs_and_similarity_score(else): ", docs_and_similarity_score)
    for doc, score in docs_and_similarity_score:
      print("Doc: ", doc, "Score: ", score)
      print("Top_n = 1 -> Doc: ", doc, "\nScore: ", score, "\nDoc metadata answer: ", doc.metadata["answer"])
      # we just grab the answer from the metadata
      answer = doc.metadata["answer"]
      question = doc.metadata["question"]
      # check if there is a score, as some have score == NaN
      if math.isnan(score) != True:
        try:
          # Append to the result in a special format
          results.append({'answer': answer, 'score': score, "question": question})
        except Exception as e:
          '''
            Log error for Devops/Security team
          '''
          print(f"Error while trying to get similarity score: {e}")
          # gracefully continue don't break the app
          continue

  print("Results from retrieve_relevant_vectors: ", results)
  return results


#########################################
### JUST EXPORT THIS ONE TO RETRIEVE ####
#########################################
def answer_retriever(query: str, relevance_score: float, top_n: int) -> List[Dict[str, Any]]:
  """Retrieve answers using PGVector"""
  relevant_answers = retrieve_relevant_vectors(query, top_n)
  print("Type relevant_answers: ", type(relevant_answers), "\nContent: ", relevant_answers)
  results = []
  # [{'answer': answer, 'score': score}]
  for answer in relevant_answers:
    print(f"this is the : {answer['score']} {type(answer['score'])}and this is the revelevance score {relevance_score} {type(relevance_score)} . is it bigger or not: {answer['score'] > relevance_score}")
    if answer["score"] > relevance_score:
      print("Vector: ", answer, ", Vectore score: ", answer["score"], f" vs relevant score: {relevance_score}")
      print("Vector: ", answer)
      results.append({
        'answer': answer['answer'],
        'score': answer['score'],
        'question': answer['question']
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

def retrieve_answer_action(state: MessagesState):
#def retrieve_answer_action():
  """
  Retrieves best answer for user query from the vector database

  Parameter:
  query: str = user question

  returns:
  retrieved answer for that specific user question
  """
  #messages = state['messages']
  #last_message = messages[-1].content
  rephrased_user_query = os.getenv("REPHRASED_USER_QUERY")

  # vars
  query: str = os.getenv("REPHRASED_USER_QUERY")
  print("query: ", query)
  # we will perform two retrieval with different scores
  score063: float = float(os.getenv("SCORE063"))
  score055: float = float(os.getenv("SCORE055"))
  print("score 063: ", score063, ", score055: ", score055)
  top_n: int = int(os.getenv("TOP_N"))
  print("top_n", top_n, type(top_n))
  vector_responses: dict = {}

  # Perform vector search with score if semantic search is not relevant
  try:
    vector_response_063 = answer_retriever(query, score063, top_n)
    print("RESPONSE 063: ", vector_response_063)
    '''
      # Returns
      [{
        'answer': vector['answer'],
        'score': vector['score'],
      }]
    '''
    if top_n > 1:
      # do a for loop as we might have more than one answer retrieved
      count = 1
      for answer in vector_response_063:
        vector_responses[f"score_063_{count}"] = answer["answer"]
        count += 1
    else:
      if vector_response_063:
        # update to vector_response
        vector_responses["score_063"] = vector_response_063[0]["answer"]

  except Exception as e:
    print(f"An error occured while trying to perform vectordb search 063 query {e}")
    #return e
    return {"messages": [{"role": "ai", "content": json.dumps({"error_vector": f"An error occured while trying to perform vectordb search 063 query: {e}"})}]}

  try:
    vector_response_055 = answer_retriever(query, score055, top_n)
    if top_n > 1:
      # do a for loop as we might have more than one answer retrieved
      count = 1
      for answer in vector_response_055:
        vector_responses[f"score_055_{count}"] = answer["question"]
        count += 1
    else:
      if vector_response_055:
        # update to vector_response
        vector_responses["score_055"] = vector_response_055[0]["question"]

  except Exception as e:
    print(f"An error occured while trying to perform vectordb search 055 query {e}")
    #return e
    return {"messages": [{"role": "ai", "content": json.dumps({"error_vector": f"An error occured while trying to perform vectordb search 055 query: {e}"})}]}
  # vector_response is: List[Dict]
  if vector_responses:
    print("Vector responses: ", vector_responses)
    #return vector_responses
    return {"messages": [{"role": "ai", "content": json.dumps({"answers": vector_responses})}]}
  else:
    # If no relevant result found, return a default response, and perform maybe after that an internet search and cache the query and the response
    #return "nothingu"
    return {"messages": [{"role": "ai", "content": json.dumps({"nothing": "nothing_in_cache_nor_vectordb"})}]}




######################################
### TEST EMBEDDING THEN RETRIEVE   ###
######################################

import embed_data
from langchain.docstore.document import Document

# test embed then retrieve:
def embed(business_document_question_answer, business_document_title):


  count = 0
  list_of_docs = []
  business_document_title = collection_normalize_name(business_document_title)
  print("formatted business document title: ", business_document_title)
  # loop through the list
  for question, answer in business_document_question_answer.items():
    print("quesiton_answer: ", question, answer)
    # format the document to be embedded using langchain `Document` on the fly and add to list of docs
    count += 1
    doc = Document(
      # in content we just put question
      # as this is what we are searching against for and will get answer from metadata
      page_content=f"{question} {answer}",
      metadata= {
        "document_title": business_document_title,
        "question": question,
        "answer": answer,
        # id's have to be unique otherwise pgvector can override the existing one even if in another collection
         "id": uuid.uuid4(),
      }
    )
    print(f"Doc {count}: {doc}")
    list_of_docs.append(doc)
  # try to embed each set of question answers
  try:
    # here the collection will use document_title as name. put `doc` in a list `[]`. document title is the business collection name
    print(f"Embedding document {count}... please wait...")
    embed_data_result = embed_data.vector_db_create(list_of_docs, business_document_title , CONNECTION_STRING, embeddings)
  except Exception as e:
    print(f"An exception occured while trying to embed data: {e}")


business_document_question_answer: dict = {
  "What is a manga kissa?": "A manga kissa is a Japanese café where you can read manga, relax, and sometimes use private booths.",
  "Can I stay overnight at a manga kissa?": "Yes, many manga kissa offer overnight plans with reclining seats or private booths.",
  "Do manga kissa have internet?": "Yes, manga kissa typically provide high-speed internet and computers for browsing.",
  "What snacks are available at manga kissa?": "Snacks include instant noodles, drinks, and sometimes free soft drinks or coffee.",
  "Are manga kissa expensive?": "Rates are affordable, starting around 400-600 yen per hour. Overnight packages may cost 1,500-2,000 yen.",
  "Can foreigners visit manga kissa?": "Yes, manga kissa are open to everyone, though some may have limited English support.",
  "What facilities do manga kissa offer?": "Facilities include manga collections, private booths, internet access, showers, and reclining seats.",
  "Are manga kissa suitable for families?": "Some manga kissa are family-friendly, but others cater more to solo travelers or adults.",
  "What is the atmosphere of a manga kissa?": "It is quiet and cozy, designed for relaxation and reading manga.",
  "Where can I find manga kissa in Tokyo?": "You can find manga kissa in Akihabara, Shinjuku, and Ikebukuro, among other areas in Tokyo."
}

#print(embed(business_document_question_answer, "Tokyo Manga Kissa Guide"))
#print(retrieve_answer_action())
