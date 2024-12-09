import os
import json
import psycopg2
from typing import List, Dict, Any
from langchain_community.vectorstores.pgvector import PGVector, DistanceStrategy
from langchain.docstore.document import Document
from langchain_ollama import OllamaEmbeddings
from dotenv import load_dotenv


load_dotenv(dotenv_path='.env', override=False)
load_dotenv(dotenv_path=".vars", override=True)

embeddings = OllamaEmbeddings(model="mistral:7b") # temperature=float(os.getenv("EMBEDDINGS_TEMPERATURE")))

CONNECTION_STRING = PGVector.connection_string_from_db_params(
    driver=os.getenv("DRIVER"), # psycopg2
    host=os.getenv("DBHOST"),
    port=int(os.getenv("DBPORT")),
    database=os.getenv("DBNAME"),
    user=os.getenv("DBUSER"),
    password=os.getenv("DBPASSWORD"),

BUSINESS_COLLECTION_NAME = os.getenv("BUSINESS_COLLECTION_NAME")

def vector_db_create(doc: List[Document], collection: str = BUSINESS_COLLECTION_NAME, connection: str = CONNECTION_STRING, embeddings: OllamaEmbeddings = embeddings) -> PGVector|dict:
  try:
    """Create and store embeddings in PGVector."""
    db_create = PGVector.from_documents(
        embedding=embeddings,
        documents=doc,
        collection_name=collection,
        connection_string=connection,
        distance_strategy=DistanceStrategy.COSINE,
        #distance_strategy="cosine", # can be "eucledian", "hamming", "cosine"EUCLEDIAN, COSINE, HAMMING
    )
    """
      See here what to return
    """
    return db_create
  except Exception as e:
    print(f"An error occurred while trying to embed in vector db -> {e}")
    return {"error": f"An error occurred while trying to embed in vector db -> {e}"}
