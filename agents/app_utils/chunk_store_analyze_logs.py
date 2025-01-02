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
 - need an extra function that will go through the logs per groups of flags and analyze each lines (be carefull rate limit, so do include retry logic and asynchronous)
'''
def detect_flagged_logs(flags: list, list_of_log_files: list) -> dict:
  '''
    gets a list of log files
    reads those files
    add to a dictionary the flagged lines
  '''

  # CHUNK
  # dict[list] that will hold for each flag key a list value of log lines
  flagged_logs_dict = {}
  # here we prepare the dictionary to have flags as key (`flags` is a env var to be set)
  for flag in flags:
    flagges_logs_dict[flag] = []

  # read through log files lines and detect any of the flags
  for log_file_name in list_of_log_files:
    with open(log_file_name, 'r', encoding="utf-8") as log_file:

      # now read through lines of the log_file and detect the flag. when detected store it in db
      for flag in flags:
        for line in loge_file:

          # we check if the level is one of the flag ones and add it to return dictionary
          if json.loads(line)["level"] == flag:

            # add to the flag list of the dict flagged_logs_dict
            flagged_logs_dict[flag] += [line]

  # is a Dict[str, List[json.dumps(log lines)]]
  return flagged_logs_dict

def store_logs(log_level: str, line:str, connection: str = CONNECTION_STRING) -> Dict:
  '''
    Stores logs in database with their log level
  '''
  # STORE
  try: 
    # we open a database connection to do all operations
    with psycopg.connect(CONNECTION_STRING) as conn:
      try:
        # create a cursor to use SQL commands
        with conn.cursor() as cur:
          # store the values
          cur.execute(
            "INSERT INTO agents_loganalyzer (chunk, log_level, advice) VALUES (%s, %s, %s)",
            (line, log_level, "")
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
      return {"error": f"An error occured while trying to store logs: {e}"}


def chunk_store_logs(flags: list, list_of_log_files: list, connection: str = CONNECTION_STRING) -> Dict:
  '''
    reads through logs files and detects flagged logs that need to be stored in database for AI analysis and store those
  '''
  # here flagged_logs_dict is a Dict[str, List[json.dumps(log lines)]]
  flagged_logs_dict = detect_flagged_logs(flags, list_of_log_files)

  # we store logs loopping through the dict
  for flag, log_lines_list_dumps in flagged_logs_dict.items():
    for log_line in log_lines_list_dumps:
 
      # Now we can store in db
      try:
        store_logs(flag, log_line, connection: str = CONNECTION_STRING)
      except Eception as e:
        return {"error": "An error occured while storing logs: {e}"}
 
  return {"success": "All logs data has been stored successfully."}

