import os
import json
import requests
from django.shortcuts import render
from django.http import HttpResponse
from agents.app_utils import (
  custom_chunk_and_embed_to_vectordb,
  is_path_or_text,
  process_query,
  retrieve_answer,
  embed_data,
  delete_embeddings,
  formatters,
)
# retrieval agent
from agents.graph.retrieval_agent_graph import retrieval_agent_team
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
# check if user is client and use this in decorator to it test
def is_client_user(user):
  return user.groups.filter(name='client').exists()

def callLlmApi(request):
  return HttpResponse("calling API")

'''
 no need to parametrize user query in url, we will just use env var and fetch it from here
'''

@csrf_exempt
@login_required(login_url='users:loginclientuser')
@user_passes_test(is_client_user, login_url='users:loginclientuser')
def retrieveData(request):
  user_query = os.getenv("USER_INITIAL_QUERY")
  try:
    # retrieval response while like: `{"messages": [{"role": "ai", "content": json.dumps({"response": response_055})}]}`
    retrieval_response = retrieval_agent_team(user_query)
    print("Retrieval Response RAW from agents to django view: ", json.loads(retrieval_response), type(json.loads(retrieval_response)))
    # here we target the content of the dict returned and json.load it (deserialize): json.dumps({"response": response_055})}
    retrieval_response_json = json.loads(retrieval_response)
    retrieval_message_content_json = json.loads(retrieval_response_json['answer_to_user']['messages'][-1]['content'])
    # we should here get the dictionary like (could be an `error` as well): {"response": response_055} 
    print("retrieval_message_content_json: ", retrieval_message_content_json, type(retrieval_message_content_json), "retrieval_message_content_json Keys(): ", retrieval_message_content_json.keys())

    '''
      make sure to send either 'error': <response error> OR 'answer': <response answer> in dict and json.dumps() that is what is the `clientchat` is waiting for
    '''

    for k, v in retrieval_message_content_json.items():
      if k == "response_nothing":
        response_transmit = {"answer": v}
        print(f"Found Response: {response_transmit}")
        return HttpResponse(json.dumps(response_transmit), content_type='application/json', status=200)
      elif k == "response":
        response_transmit = {"answer": v}
        print(f"Found Response: {response_transmit}")
        return HttpResponse(json.dumps(response_transmit), content_type='application/json', status=200)
      else:
        response_transmit = {"error": v}
        print(f"Response Error: {response_transmit}")
        return HttpResponse(json.dumps(response_transmit), content_type='application/json', status=400)

  except requests.exceptions.RequestException as e:
    # log also here for Devops/Security 
    error_message = {"error": f"An error occured while trying to retrieveData: {e}"}
    print(error_message)
    return HttpResponse(json.dumps(error_message), content_type="applicatiion/json", status=500)
  except Exception as e:
    # log also here for Devops/Security 
    error_message = {"error": f"An exception error occured while trying to retrievedata: {e}"}
    print(error_message)
    return HttpResponse(json.dumps(error_message), content_type="applicatiion/json", status=400)


# we need this decorator for internal API calls to not require any CSRF token
# decorators are read from next to function to out
# here is the correct order, we check the test if user is business, if user is logged in, and examplt csrf token for internal API call
@csrf_exempt
@login_required(login_url='users:loginbusinessuser')
@user_passes_test(is_business_user, login_url='users:loginbusinessuser')
def embedData(request, pk):

  # fetch required data from databaase to prepare documents to be embedded
  business_document = get_object_or_404(BusinessUserData, pk=pk, user=request.user)
  business_document_title = business_document.document_title
  business_document_question_answer = business_document.question_answer_data
  print("business question answers: ", business_document_question_answer, type(business_document_question_answer))
  # will count the number of documents embeded
  count = 0

  if request.method == 'POST':

    # set env var for business collection name which will have document_title as name for if we need it in the helper function side
    formatted_business_doc_title = formatters.collection_normalize_name(business_document_title)
    set_key(".vars.env", "BUSINESS_COLLECTION_NAME", str(formatted_business_doc_title))

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
          "id": count,
        }
      )
      print(f"Doc {count}: {doc}")

      # try to embed each set of question answers
      try:
        # here the collection will use document_title as name. put `doc` in a list `[]`. document title is the business collection name
        embed_data_result = embed_data.vector_db_create([doc], business_document_title , CONNECTION_STRING, embeddings)
        if "success" in embed_data_result:
          print("embed data result: ", embed_data_result)
          response = json.dumps({"success": f"(x{count}) Data successfully embeded, ready for client user retrieval."})
          return HttpResponse(response, content_type="application/json", status=200)
      except Exception as e:
        '''
         Create logs for Devops/Security team
        '''
        print("error trying to embed data: ", e)
        response = json.dumps({"error": f"An error occured while trying to create embeddings: {e}"})
        return HttpResponse(response, content_type="application/json", status=400)

  response = json.dumps({"error": "Get request not accepted for this route."})
  '''
   Log this for Devops/ Security team
  '''
  return HttpResponse(response, content_type="application/json", status=405)

@csrf_exempt
@login_required(login_url='users:loginbusinessuser')
@user_passes_test(is_business_user, login_url='users:loginbusinessuser')
def deleteEmbeddingCollection(request, pk):

  # get the document name using the document id sent through the request to delete embeddings
  business_document = get_object_or_404(BusinessUserData, pk=pk, user=request.user)
  business_document_title = business_document.document_title

  if request.method == 'POST':
    try:
      # conenction string is defined at the top of this fine Global scope so we can access to it
      delete_collection = delete_embeddings.delete_embedding_collection(CONNECTION_STRING, business_document_title)
      # delete_collection is a string
      if "success" in delete_collection:
        response = json.dumps({"success": f"Collesciton {business_document_title} deleted successfully."})
        return HttpResponse(response, content_type="application/json", status=200)
      else:
        # we return delete_collection variable as it has the error message str
        response = json.dumps({"error": f"An error received while trying to delete collection {business_document_title}: {delete_collection}"})
        return HttpResponse(response, content_type="application/json", status=400)
    except Exception as e:
      '''
       Create logs for Devops/Security team
      '''
      print("error trying delete embeddings: ", e)
      response = json.dumps({"error": f"An error occured while trying to delete embedding collection {business_document_title}: {e}"})
      return HttpResponse(response, content_type="application/json", status=400)





