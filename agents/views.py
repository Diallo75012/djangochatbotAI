from django.shortcuts import render
from django.http import HttpResponse
from agents.app_utils import (
  custom_chunk_and_embed_to_vectordb,
  is_path_or_text,
  process_query,
  retrieve_answer,
  embed_data,
)
from langchain.docstore.document import Document
from agents.graph import retrieval_agent_graph
from businessdata.models import BusinessUserData
from dotenv import load_dotenv, set_key

# load env vars
load_dotenv(dotenv_path='.env', override=False)
load_dotenv(dotenv_path=".vars.env", override=True)

embeddings = OllamaEmbeddings(model="mistral:7b") # temperature=float(os.getenv("EMBEDDINGS_TEMPERATURE")))

CONNECTION_STRING = PGVector.connection_string_from_db_params(
    driver=os.getenv("DRIVER"), # psycopg2
    host=os.getenv("DBHOST"),
    port=int(os.getenv("DBPORT")),
    database=os.getenv("DBNAME"),
    user=os.getenv("DBUSER"),
    password=os.getenv("DBPASSWORD"),

BUSINESS_COLLECTION_NAME = os.getenv("BUSINESS_COLLECTION_NAME")

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


def embedData(request):

  if request.method == 'POST':

    try:
      # Parse the JSON payload
      # dict[k/v, [k/v]]
      payload = json.loads(request.body.decode('utf-8'))

      # Extract the document_title and question_answer_data
      # dict key/value
      document_title = payload.get("document_title")
      # list[dict key/value, dict key/value, ...]
      question_answer_data = payload.get("question_answer")
    except json.JSONDecodeError:
      response = json.dumps({"error": "Invalid JSON payload"})
      return HttpResponse(response, content_type="application/json", status=400)

    document_title = business_document.document_title
    # set env var for business collection name which will have document_title as name
    sek_key(".vars.env", "BUSINESS_COLLECTION_NAME", document_title)

    count = 0
    # loop through the list
    for question_answer in question_answer_data:
      # loop through each dict key value pairs
      for question, answer in question_answer.items():
        # format the document to be embedded using langchain `Document`
        doc = Document[
          page_content=f"{question} {answer}",
          metadata= {
            "document_title": document_title,
            "question": question,
            "answer": answer,
          }
        )
        # try to embed each set of question answers
        try:
          # here the collection will use document_title as name
          embed_data.vector_db_create([doc], document_title , CONNECTION_STRING, embeddings)
          count += 1
        except Exception as e:
          '''
           Create logs for Devops/Security team
          '''
          response = json.dumps({"error": f"An error occured while trying to create embeddings: {e}"})
          return HttpResponse(response, content_type="application/json", 400)

      response = json.dumps({"success": f"(x{count}) Data successfully embeded, ready for client user retrieval."})
      return HttpResponse(reponse, content_type="application/json" ,200)

  response = json.dumps({"error": "Get request not accepted for this route."})
  '''
   Log this for Devops/ Security team
  '''
  return HttpResponse(response, content_type="application/json" ,405)











