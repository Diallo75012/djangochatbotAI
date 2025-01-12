





import os
import json
import psycopg
from typing import List, Dict, Any
from dotenv import load_dotenv
from pathlib import Path
BASE_DIR = Path(__file__).resolve().parent.parent


load_dotenv(dotenv_path='../.env', override=False)
load_dotenv(dotenv_path='../vars.env', override=True)

# db connection vars
driver=os.getenv("DRIVER") # not psycopg2 as now it required psycopg3 (we install both: pip install psycopg2 psycopg)
host=os.getenv("DBHOST")
port=int(os.getenv("DBPORT"))
database=os.getenv("DBNAME")
user=os.getenv("DBUSER")
password=os.getenv("DBPASSWORD")
#CONNECTION_STRING = f"postgresql+{driver}://{user}:{password}@{host}:{port}/{database}"
CONNECTION_STRING = f"postgresql://{user}:{password}@{host}:{port}/{database}"

'''
 - need an extra function that will go through the logs per groups of flags and analyze each lines (be carefull rate limit, so do include retry logic and asynchronous)
'''
def detect_flagged_logs(flags: list, list_of_log_files: list) -> dict:
  """
    Gets a list of log files,
    reads those files,
    and adds flagged lines to a dictionary.
  """
  # Initialize the dictionary to hold flags and corresponding log lines
  flagged_logs_dict = {flag: [] for flag in flags}

  # Read through log files
  print("list_of_log_files: ", list_of_log_files)
  for log_file_name in list_of_log_files:
    print("log file name: ", log_file_name)
    log_path = os.path.join(BASE_DIR, f"agents/graph/logs_to_analyze/{log_file_name}")
    try:
      with open(log_path, 'r', encoding="utf-8") as log_file:
        # Iterate through each line in the log file
        for line in log_file:
          try:
            # Parse the line as JSON as it is json.dumps() to check level
            log_data = json.loads(line)
            log_level = log_data.get("level")

            # Check if the log level matches any of the flags
            if log_level in flags:
              flagged_logs_dict[log_level].append(line)
              print(f"flagged_dict plus lines: {flagged_logs_dict}")

          except json.JSONDecodeError as e:
            print(f"Malformed line in {log_file_name}: {line}. Error: {e}")
    except FileNotFoundError:
      print(f"File not found: {log_path}")

  # is a Dict[str, List[dict of log lines)]]
  '''
  {'WARNING': [
    {'time': '2024-12-26 21:39:50,143', 'level': 'WARNING', 'name': 'django.request', 'message': 'Not Found: /', 'user_id': 'anonymous'},
    {'time': '2024-12-26 21:39:51,153', 'level': 'WARNING', 'name': 'django.request', 'message': 'Not Found: /favicon.ico', 'user_id': 'anonymous'},
    {'time': '2024-12-28 23:19:25,553', 'level': 'WARNING', 'name': 'httpx', 'message': 'warn clientchat', 'user_id': 'anonymous'},
    {'time': '2024-12-28 23:16:25,553', 'level': 'WARNING', 'name': 'httpx', 'message': 'warn agent', 'user_id': 'anonymous'},
    {'time': '2024-12-28 23:17:25,553', 'level': 'WARNING', 'name': 'httpx', 'message': 'warn businessdata', 'user_id': 'anonymous'},
    {'time': '2024-12-28 23:29:25,553', 'level': 'WARNING', 'name': 'httpx', 'message': 'warn common', 'user_id': 'anonymous'}
    ],
    'ERROR': [],
    'CRITICAL': []
  }
  '''

  return flagged_logs_dict

def store_logs(log_level: str, lines: list, connection: str = CONNECTION_STRING) -> Dict:
  """
  Stores logs in the database with their log level.
  """
  try:
    # Open a database connection
    with psycopg.connect(connection) as conn:
      try:
        # Create a cursor to execute SQL commands
        with conn.cursor() as cur:
          for line in lines:
            print(f"Inserting log_level: {log_level}, line: {line}")
            cur.execute(
              "INSERT INTO agents_loganalyzer (chunk, log_level) VALUES (%s, %s)",
              (line, log_level)
            )
      except Exception as e:
        conn.rollback()
        print(f"Error during database operation: {e}")
        return {"error": f"An error occurred while storing logs: {e}"}
      else:
        conn.commit()
        print("Logs committed successfully.")
      return {"success": "All logs data has been stored successfully."}
  except Exception as e:
    print(f"Error connecting to the database: {e}")
    return {"error": f"An error occurred while trying to connect to the database: {e}"}

def chunk_store_logs(flags: list, list_of_log_files: list, connection: str = CONNECTION_STRING) -> Dict:
  """
  Reads through log files, detects flagged logs, and stores them in the database.
  """
  try:
    flagged_logs_dict = detect_flagged_logs(flags, list_of_log_files)
  except Exception as e:
    return {"error": f"An error occurred while detecting flagged logs: {e}"}

  # Iterate through flagged logs and store them
  for flag, log_lines_list_dumps in flagged_logs_dict.items():
    if not log_lines_list_dumps:
      print(f"No logs found for flag: {flag}")
      continue

    print(f"Storing logs for flag: {flag}, count: {len(log_lines_list_dumps)}")
    try:
      store_logs(flag, log_lines_list_dumps, connection)
    except Exception as e:
      print(f"Error while storing logs for flag {flag}: {e}")
      return {"error": f"An error occurred while storing logs: {e}"}

  return {"success": "All logs data has been stored successfully."}

