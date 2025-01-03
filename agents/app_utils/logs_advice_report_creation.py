import os
import json
import psycopg
import time
from datetime import datetimes
from typing import List, Dict, Any
from dotenv import load_dotenv
from app_utils import (
  call_llm,
  prompt_creation,
)
from structured_output.structured_output import advice_agent_report_creator_schema
from prompts import advice_agent_report_creator_prompt
# LLMs
from agents.llms.llms import (
  groq_llm_mixtral_7b,
  groq_llm_llama3_8b,
  groq_llm_llama3_70b,
  groq_llm_llama3_70b_versatile,
  groq_llm_gemma_7b,
)


load_dotenv(dotenv_path='.env', override=False)
load_dotenv(dotenv_path='vars.env', override=True)

# db connection vars
driver=os.getenv("DRIVER") # not psycopg2 as now it required psycopg3 (we install both: pip install psycopg2 psycopg)
host=os.getenv("DBHOST")
port=int(os.getenv("DBPORT"))
database=os.getenv("DBNAME")
user=os.getenv("DBUSER")
password=os.getenv("DBPASSWORD")
CONNECTION_STRING = f"postgresql+{driver}://{user}:{password}@{host}:{port}/{database}"

def get_database_flagged_logs(log_level: str, connection: str = CONNECTION_STRING) -> Dict[str, str]: # second `str` is a `json.dumps()`
  '''
    fetch from database all logs having the same flag
  '''
  # will have all the 
  log_level_group_logs = {log_level: []}
  # STORE
  try: 
    # we open a database connection to do all operations
    with psycopg.connect(CONNECTION_STRING) as conn:
      try:
        # create a cursor to use SQL commands
        with conn.cursor() as cur:
          # store the values
          cur.execute(
            "SELECT * FROM agents_loganalyzer WHERE log_level = %s",
            (log_level)
          )
        results = cursor.fetchall()
        for log in results:
          # update the Dict[str, List]
          log_level_group_logs[log_level] += [log]
      except BaseException:
        # rollback if issue
        conn.rollback()
      else:
        # commit if all good
        conn.commit()
      finally:
        # close connection
        conn.close()
      # return the dict {log_level: [log, log2..., logN]}
      return {"success": json.dumps{log_level_group_logs}}
    Except Exception as e:
      return {"error": f"An error occured while trying to fetch logs: {e}"}


def get_advice_on_logs(log_levels: list) -> Dict[str, str]: # it is a Dict[str, str(meaning here of a list)]

  for flag in log_levels:
    # FETCH LOGS FROM DB
    try:
      # fetch all data from database of that log level: we get a `Dict[str,str]` and first `str` is `success` and second a `Dict[str, List]`
      fetched_logs_response = get_database_flagged_logs(flag, CONNECTION_STRING)
    except Exception as e:
      return {"error": f"An error occured while trying to fetch logs to get advice: {e}"} 

  # UNPACK RESPONSE
  # can unpach with `,` after the tuple and access variables `fetched_flag` and `list_logs`
  (fetched_flag, list_logs), = json.loads(fetched_logs_response["success"]).items()
  # OR use this to unpack the dict:
  #fetched_flag = list(fetched_logs_response.keys())[0]
  #list_logs = list(fetched_logs_response.values())[0]
    
  for log_line in list_logs:

    # INJECT IN QUERY AND MAKE API CALL
    query = prompt_creation.prompt_creation(advice_agent_report_creator_prompt["human"], user_query=f"I found this log of record {fetched_flag}:{log_line};\n and want you to help me troubleshoot and provide advise. it is a Python Django application.")
    print("query: ", query)
  
    # get report made, might need to truncate logs or to send batch of certain size and keep writing in the same report file
    # or just do for loop and make call for each log line taking care of retry and rate limits
    try:
      report = call_llm.call_llm(query, advice_agent_report_creator_prompt_prompt["system"]["template"], advice_agent_report_creator_prompt_schema, groq_llm_llama3_70b)
    except Exception as e:
      return {"error": f"An error occured while trying to analyze user input content: {e}"}

    # WRITE TO FILE
    # write to a file the line in fomat json.dumps({"time": get the time from the fetched parsed ... log_line so that we can relate this advice to a specific log having same time, "response": the llm advice and reponse in how to fix the issue}). also set date for the file. 'a' option will create file if it doesn't exist and will append new lines
    current_date = datetime.now()
    formatted_date = current_date.strftime("%Y_%m_%d")

    # `a` Append to log file
    if fetched_flag == "CRITICAL":
      with open(os.path.join(BASE_DIR, "log_agent_reports", f"{os.getenv('LOGS_REPORT_CRITICAL_FILE_NAME')}_{formatted_date}", 'a', encoding="utf-8") as report_file:
        report_file.write({"log_time": log_line["time"], "log_advice": report["response"]})
        # we sleep a bit to not get rate limited
      time.sleep(0.5)
    elif fetched_flag == "ERROR":
      with open(os.path.join(BASE_DIR, "log_agent_reports", f"{os.getenv('LOGS_REPORT_ERROR_FILE_NAME')}_{formatted_date}", 'a', encoding="utf-8") as report_file:
        report_file.write({"log_time": log_line["time"], "log_advice": report["response"]})
      time.sleep(0.5)
    elif fetched_flag == "WARNING":
      with open(os.path.join(BASE_DIR, "log_agent_reports", f"{os.getenv('LOGS_REPORT_WARNING_FILE_NAME')}_{formatted_date}", 'a', encoding="utf-8") as report_file:
        report_file.write({"log_time": log_line["time"], "log_advice": report["response"]})
      time.sleep(0.5)
    else:
      return {"error": f"No fetched flag detected. Therefore, no log file written for this entry: {log_line}"}

  return {"success": f"all flagged logs have been analyzed by agent. Please find reports at: {os.path.join(BASE_DIR, 'agents/graph/agents_logs_reports')"}




