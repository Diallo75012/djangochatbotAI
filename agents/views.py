from django.shortcuts import render
from django.http import HttpResponse
from app_utils import (
  custom_chunk_and_embed_to_vectordb.py,
  is_path_or_text.py,
  process_query.py
)
from graph import retrieval_agent_graph
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
  retrieval_agent_graph(user_query)
  # all error types returned by graph: "error", "error_vector", "error_reponse_nothing", "error_reponse_063", "error_reponse_055"
  return HttpResponse("Retrieving DATA")
