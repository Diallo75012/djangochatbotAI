import os
import json
import logging
import psycopg
from typing import List, Dict, Any, Tuple
from django.conf import settings
from dotenv import load_dotenv


# logger
agents_app_logger = logging.getLogger('common')

load_dotenv(dotenv_path='.env', override=False)
load_dotenv(dotenv_path='vars.env', override=True)

# db connection vars
driver=os.getenv("DRIVER") # not psycopg2 as now it required psycopg3 (we install both: pip install psycopg2 psycopg)
host=os.getenv("DBHOST")
port=int(os.getenv("DBPORT"))
database=os.getenv("DBNAME")
user=os.getenv("DBUSER")
password=os.getenv("DBPASSWORD")
# `psycopg.connect()` doesn't expect a `{driver}` line `SQLALquemy` would therefore we drop ot for this `psycopg3` like connection
#CONNECTION_STRING = f"postgresql+{driver}://{user}:{password}@{host}:{port}/{database}"
CONNECTION_STRING = f"postgresql://{user}:{password}@{host}:{port}/{database}"

def db_recorder(record_query: str, *args: Tuple[str, ...], connection: str = CONNECTION_STRING) -> Dict:
  '''
    Record data to database
  '''
  # STORE
  try:
    # we open a database connection to do all operations
    with psycopg.connect(CONNECTION_STRING) as conn:
      try:
        # create a cursor to use SQL commands
        with conn.cursor() as cur:
          # store the values
          cur.execute(f"{record_query}",args)

      except BaseException:

        agents_app_logger.error(f"Log Analyzer Agent creating cursor (db_recorder): Exception -> {e}")

        # rollback if issue
        conn.rollback()
      else:
        # commit if all good
        conn.commit()
      finally:
        # close connection
        conn.close()
      return {"success": "data recorded"}
  except Exception as e:

    agents_app_logger.error(f"Log Analyzer Agent storing record in db (db_recorder): Exception -> {e}")

    return {"error": f"An exception occured when recorded data to database: {e}"}
