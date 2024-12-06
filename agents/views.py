from django.shortcuts import render
from django.http import HttpResponse
from app_utils import (
  custom_chunk_and_embed_to_vectordb.py,
  is_path_or_text.py,
  process_query.py
)
from llms import llms
from prompts import prompts
from structured_output import structured_output
from dotenv import load_dotenv


load_dotenv()

def callLlmApi(request):
  return HttpResponse("calling API")

def embedData(request):
  return HttpResponse("Embedding DATA")

def retrieveData(request):
  return HttpResponse("Retrieving DATA")
