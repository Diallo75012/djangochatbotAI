import os
import json
from django.shortcuts import render
from django.http import HttpResponse
from agents.app_utils import (
  custom_chunk_and_embed_to_vectordb,
  is_path_or_text,
  process_query,
  retrieve_answer,
  embed_data,
)
from django.contrib.auth.decorators import login_required, user_passes_test
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404
from langchain.docstore.document import Document
from langchain_community.vectorstores.pgvector import PGVector
from langchain_ollama import OllamaEmbeddings
from agents.graph import retrieval_agent_graph
from businessdata.models import BusinessUserData
from dotenv import load_dotenv, set_key

# load env vars
load_dotenv(dotenv_path='.env', override=False)
load_dotenv(dotenv_path=".vars.env", override=True)

embeddings = OllamaEmbeddings(model="mistral:7b") # temperature=float(os.getenv("EMBEDDINGS_TEMPERATURE")))

# db connection vars
driver=os.getenv("DRIVER") # not psycopg2 as now it required psycopg3 (we install both: pip install psycopg2 psycopg)
host=os.getenv("DBHOST")
port=int(os.getenv("DBPORT"))
database=os.getenv("DBNAME")
user=os.getenv("DBUSER")
password=os.getenv("DBPASSWORD")
# use of psycog3 driver `psycopg`
CONNECTION_STRING = f"postgresql+{driver}://{user}:{password}@{host}:{port}/{database}"
"""
CONNECTION_STRING = PGVector.connection_string_from_db_params(
    driver=os.getenv("DRIVER"), # psycopg2
    host=os.getenv("DBHOST"),
    port=int(os.getenv("DBPORT")),
    database=os.getenv("DBNAME"),
    user=os.getenv("DBUSER"),
    password=os.getenv("DBPASSWORD"),
)
"""
BUSINESS_COLLECTION_NAME = os.getenv("BUSINESS_COLLECTION_NAME")

# check if user is business and use this in decorator to it test
def is_business_user(user):
  return user.groups.filter(name='business').exists()


def callLlmApi(request):
  return HttpResponse("calling API")

'''
 no need to parametrize user query in url, we will just use env var and fetch it from here
'''

@csrf_exempt
@login_required(login_url='users:loginbusinessuser')
@user_passes_test(is_business_user, login_url='users:loginbusinessuser')
def retrieveData(request):
  user_query = os.getenv("USER_INITIAL_QUERY")
  retrieval_response = retrieval_agent_graph(user_query)
  retrieval_json = json.loads(retrieval_response)
  # all error types returned by graph: "error", "error_vector", "error_reponse_nothing", "error_reponse_063", "error_reponse_055"
  list_errors = ["error", "error_vector", "error_response_nothing", "error_response_063", "error_response_055"]
  list_answers = ["response_nothing", "response_063", "response_055"]

  # response here will be type json_dumps() so we can sent it like that and json.load it in javascript passing through the client_chat view which has the csrf token
  # key of dict is `"answer"`
  response = retrieve_answer.retrieval_view_response_transmit(retrieval_json, list_answers, list_errors)
  return HttpResponse(response, content_type='application/json', status=200)


# we need this decorator for internal API calls to not require any CSRF token
# decorators are read from next to function to out
# here is the correct order, we check the test if user is business, if user is logged in, and examplt csrf token for internal API call
@csrf_exempt
#@login_required(login_url='users:loginbusinessuser')
#@user_passes_test(is_business_user, login_url='users:loginbusinessuser')
def embedData(request, pk):

  # fetch required data from databaase to prepare documents to be embedded
  business_document = get_object_or_404(BusinessUserData, pk=pk) #user=request.user)
  business_document_title = business_document.document_title
  business_document_question_answer = business_document.question_answer_data
  print("business question answers: ", business_document_question_answer, type(business_document_question_answer))
  # will store all custom docs to be embedded
  list_of_docs = []
  # will count the number of documents embeded
  count = 0
  
  if request.method == 'POST':

    # set env var for business collection name which will have document_title as name for if we need it in the helper function side
    set_key(".vars.env", "BUSINESS_COLLECTION_NAME", json.dumps(business_document_title))

    # loop through the list
    for question, answer in business_document_question_answer.items():
      print("quesiton_answer: ", question, answer)
      # format the document to be embedded using langchain `Document` on the fly and add to list of docs
      count += 1
      doc = Document(
        page_content=f"{question} {answer}",
        metadata= {
          "document_title": business_document_title,
          "question": question,
          "answer": answer,
          "id": count,
        }
      )
      list_of_docs.append(doc)
      print(f"Doc {count}: {doc}")

    # try to embed each set of question answers
    try:
      # here the collection will use document_title as name. put `doc` in a list `[]`. document title is the business collection name
      print("list of docs: ", list_of_docs)
      embed_data_result = embed_data.vector_db_create(list_of_docs, business_document_title , CONNECTION_STRING, embeddings)
      if "success" in embed_data_result:
        print("embed data result: ", embed_data_result)
        response = json.dumps({"success": f"(x{count}) Data successfully embeded, ready for client user retrieval."})
        return HttpResponse(response, content_type="application/json", status=200)
    except Exception as e:
      '''
       Create logs for Devops/Security team
      '''
      print("e: ", e)
      response = json.dumps({"error": f"An error occured while trying to create embeddings: {e}"})
      return HttpResponse(response, content_type="application/json", status=400)

  response = json.dumps({"error": "Get request not accepted for this route."})
  '''
   Log this for Devops/ Security team
  '''
  return HttpResponse(response, content_type="application/json", status=405)











