import os
import json
import psycopg
from typing import List, Dict, Any
from dotenv import load_dotenv
from agents.app_utils.log_advice_report_creation import CONNECTION_STRING


load_dotenv(dotenv_path='.env', override=False)
load_dotenv(dotenv_path='vars.env', override=True)


def delete_flagged_log_from_db_table(connection: str = CONNECTION_STRING) -> Dict[str, str]:
  '''
    empty/delete database table `LogAnalyzer` ready for next job
  '''
  try: 
    # we open a database connection to do all operations
    with psycopg.connect(CONNECTION_STRING) as conn:
      try:
        # create a cursor to use SQL commands
        with conn.cursor() as cur:
          # store the values
          cur.execute(
            "DELETE FROM agents_loganalyzer"
          )
      except BaseException:
        # rollback if issue
        conn.rollback()
        return {"error": f"Error while trying to delete data from agents_loganalyzer db, connection rollback: {e}"}
      else:
        # commit if all good
        conn.commit()
      finally:
        # close connection
        conn.close()
      return {"success": "Successfully deleted all flagged logs fron agents_loganalyzer table."}}

    except Exception as e:
      return {"error": f"An error occured while trying to fetch logs: {e}"}

def delete_all_files_in_dir(directory_path):
  """
  Deletes all files in the given directory but keeps the directory itself.

  :param directory_path: Path to the directory
  """
  if not os.path.exists(directory_path):
    print(f"The directory '{directory_path}' does not exist.")
    return

  try:
    for item in os.listdir(directory_path):
      item_path = os.path.join(directory_path, item)
      # Check if it's a file and delete it
      if os.path.isfile(item_path):
        os.remove(item_path)
        print(f"Deleted file: {item_path}")
      else:
        print(f"Skipped: {item_path} (not a file)")
    return {"success": "Successfully deleted all agent copies log files. Folder graph/logz_to_analyze is empty."}}
  except Exception as e:
    return {"error": f"An error occured while trying to delete files from agent copied log folder graph/logz_to_analyze: {e}"}
