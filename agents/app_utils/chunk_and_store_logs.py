import os
import json
import psycopg
from typing import List, Dict, Any
from dotenv import load_dotenv
from agents.app_utils import formatters


load_dotenv(dotenv_path='.env', override=False)

# db connection vars
driver=os.getenv("DRIVER") # not psycopg2 as now it required psycopg3 (we install both: pip install psycopg2 psycopg)
host=os.getenv("DBHOST")
port=int(os.getenv("DBPORT"))
database=os.getenv("DBNAME")
user=os.getenv("DBUSER")
password=os.getenv("DBPASSWORD")
CONNECTION_STRING = f"postgresql+{driver}://{user}:{password}@{host}:{port}/{database}"

'''
- need one function that will store chunks to postgresql in the chunk columns
- need a second function that will go through the existing columns and evaluate with llms
  and create schema that will be saved in the corresponding row schema column (only flagged logs will have this schema)
  maybe even not use llm for this but just split the log line and use if statement to classify log as alert/error/critical (so might be done in one go)
- need also funciton that will store advice when calling llm (so along the way we need to keep those row ids for ease of fetching from database)
'''

def chunk_store_logs(logs_file_names_list : List, connection: str = CONNECTION_STRING) -> Dict:
  
  try: 
    # we open a database connection to do all operations
    with psycopg.connect(CONNECTION_STRING) as conn:
      try:
        # create a cursor to use SQL commands
        with conn.cursor() as cur:
          # store the values
          cur.execute(
            "INSERT INTO agents_loganalyzer (chunk, schema, advice) VALUES (%s, %s, %s)",
            (chunk, "", "")
          )
      
      '''
        I put `conn.close()` but this could be avoided by just doing ``cur.execute(<SQL query>)` 
        and then commit `conn.commit()`, `conn` is closed when exiting the with statement
        that is why is cool to use with as it closes files/connections 
       '''
      except BaseException:
        # rollback if issue
        conn.rollback()
      else:
        # commit if all good
        conn.commit()
      finally:
        # close connection
        conn.close()
      return {"success": "All logs data has been stored successfully."}
    Except Exception as e:
      return {"error": "An error occured while trying to store logs"}


