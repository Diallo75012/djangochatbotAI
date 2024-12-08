from django.shortcuts import render
from django.http import HttpResponse
from agents.app_utils import (
  custom_chunk_and_embed_to_vectordb,
  is_path_or_text,
  process_query,
  retrieve_answer,
)
from agents.graph import retrieval_agent_graph
from dotenv import load_dotenv

# load env vars
load_dotenv(dotenv_path='.env', override=False)
load_dotenv(dotenv_path=".vars.env", override=True)

def callLlmApi(request):
  return HttpResponse("calling API")

def embedData(request):
  return HttpResponse("Embedding DATA")

'''
 no need to parametrize user query in url, we will just use env var and fetch it from here
'''
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




