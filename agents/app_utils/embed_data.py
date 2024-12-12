import os
import json
import psycopg2
from typing import List, Dict, Any
#from langchain_community.vectorstores.pgvector import PGVector, DistanceStrategy
#from langchain_postgres import PGVector
from langchain_postgres.vectorstores import PGVector, DistanceStrategy
from langchain.docstore.document import Document
from langchain_ollama import OllamaEmbeddings
from dotenv import load_dotenv


load_dotenv(dotenv_path='.env', override=False)
load_dotenv(dotenv_path=".vars", override=True)

embeddings = OllamaEmbeddings(model="mistral:7b") # temperature=float(os.getenv("EMBEDDINGS_TEMPERATURE")))

# db connection vars
driver=os.getenv("DRIVER") # not psycopg2 as now it required psycopg3 (we install both: pip install psycopg2 psycopg)
host=os.getenv("DBHOST")
port=int(os.getenv("DBPORT"))
database=os.getenv("DBNAME")
user=os.getenv("DBUSER")
password=os.getenv("DBPASSWORD")
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

def vector_db_create(docs: List[Document], collection: str = BUSINESS_COLLECTION_NAME, connection: str = CONNECTION_STRING, embeddings: OllamaEmbeddings = embeddings) -> PGVector|dict:

  print("Collection name fom the vector_db_create function: ", collection)
  print("Type docs: ", type(docs))
  try:
    """Create and store embeddings in PGVector."""
    db_create = PGVector(
      embeddings=embeddings,
      collection_name=collection,
      connection=connection,
      distance_strategy=DistanceStrategy.COSINE,
      #distance_strategy="cosine", # can be "eucledian", "hamming", "cosine"EUCLEDIAN, COSINE, HAMMING
      use_jsonb=True,
    )
    """
      See here what to return
    """
    # use this method to embed the list of documents, docs here comes already as list of documents
    db_create.add_documents(documents=docs, ids=[doc.metadata["id"] for doc in docs])
    return {"success": f"Data correctly embedded!"}
  except Exception as e:
    print(f"An error occurred while trying to embed in vector db -> {e}")
    return e























