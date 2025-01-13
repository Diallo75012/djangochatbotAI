import os
import json
import psycopg
import time
from datetime import datetime
from typing import List, Dict, Any
from dotenv import load_dotenv
import call_llm, prompt_creation
from structured_output import advice_agent_report_creator_schema
from prompts import advice_agent_report_creator_prompt
# LLMs
from llms import (
  groq_llm_mixtral_7b,
  groq_llm_llama3_8b,
  groq_llm_llama3_70b,
  groq_llm_llama3_70b_versatile,
  groq_llm_gemma_7b,
)
# from django.conf import settings # can't import from setting or set env var to do that while running standalone script so we just build the BASE_DIR from here
from pathlib import Path
BASE_DIR = Path(__file__).resolve().parent.parent


load_dotenv(dotenv_path='../.env', override=False)
load_dotenv(dotenv_path="../.vars.env", override=True)

# db connection vars
driver=os.getenv("DRIVER") # not psycopg2 as now it required psycopg3 (we install both: pip install psycopg2 psycopg)
host=os.getenv("DBHOST")
port=int(os.getenv("DBPORT"))
database=os.getenv("DBNAME")
user=os.getenv("DBUSER")
password=os.getenv("DBPASSWORD")
#CONNECTION_STRING = f"postgresql+{driver}://{user}:{password}@{host}:{port}/{database}"
CONNECTION_STRING = f"postgresql://{user}:{password}@{host}:{port}/{database}"


def get_database_flagged_logs(log_level: str, connection: str = CONNECTION_STRING) -> Dict[str, str]:
    """
    Fetch logs from the database by log level.
    """
    log_level_group_logs = {log_level: []}

    try:
        # Debugging connection
        print(f"Connecting to database with: {connection}")

        with psycopg.connect(connection) as conn:
            try:
                print(f"Log level before database fetch: {log_level}")
                with conn.cursor() as cur:
                    # Executing the query
                    query = "SELECT chunk FROM agents_loganalyzer WHERE log_level = %s"
                    print(f"Executing query: {query}")
                    cur.execute(query, (log_level,))
                    results = cur.fetchall()

                    # Process results
                    for log in results:
                        log_level_group_logs[log_level].append(log[0])  # Assuming `chunk` is in the first column
            except Exception as e:
                conn.rollback()
                print(f"Database query error: {e}")
                raise
            finally:
                conn.commit()
        return {"success": json.dumps(log_level_group_logs)}

    except Exception as e:
        print(f"Database connection or query failed: {e}")
        return {"error": f"An error occurred while trying to fetch logs: {e}"}


def get_advice_on_logs(log_levels: list) -> Dict[str, str]:
    """
    Analyze logs from the database for each log level and generate advice.
    """
    log_analyzer_advice_to_send_to_discord_folder = os.getenv("LOG_ANALYZER_ADVICE_TO_SEND_DISCORD_FOLDER")
    for flag in log_levels:
        try:
            fetched_logs_response = get_database_flagged_logs(flag, CONNECTION_STRING)
            print("Fetched logs response: ", fetched_logs_response)

            if "success" not in fetched_logs_response:
                return {"error": f"Failed to fetch logs for flag: {flag}"}

            fetched_flag, list_logs = next(iter(json.loads(fetched_logs_response["success"]).items()))
            print("Fetched flag: ", fetched_flag, "Logs: ", list_logs)

            if not list_logs:
                print(f"No logs found for flag: {flag}")
                continue

            for log_line in list_logs:
                query = prompt_creation.prompt_creation(
                    advice_agent_report_creator_prompt["human"],
                    user_query=f"I found this log of record {fetched_flag}:{log_line};\n and want you to help me troubleshoot and provide advice. It is a Python Django application."
                )
                print("Query for LLM: ", query)

                try:
                    report = call_llm.call_llm_for_logs(
                        query,
                        advice_agent_report_creator_prompt["system"]["template"],
                        advice_agent_report_creator_schema,
                        groq_llm_llama3_70b
                    )
                    print("LLM Response: ", report)

                    current_date = datetime.now().strftime("%Y_%m_%d")
                    report_file_name = os.getenv(f"LOGS_REPORT_{fetched_flag}_FILE_NAME")
                    report_path = os.path.join(BASE_DIR, log_analyzer_advice_to_send_to_discord_folder, f"{current_date}_{report_file_name}")
                    print("Writing to report path: ", report_path)

                    json_response = {
                        "log_time": json.loads(log_line).get("time"),
                        "log_advice": report["response"]
                    }
                    with open(report_path, 'a', encoding="utf-8") as report_file:
                        report_file.write(json.dumps(json_response) + "\n")
                except Exception as e:
                    print(f"Error during LLM call or writing: {e}")
                    return {"error": f"An error occurred: {e}"}
        except Exception as e:
            print(f"Error fetching or processing logs for flag {flag}: {e}")
            return {"error": f"An error occurred while fetching or processing logs: {e}"}

    return {"success": f"All flagged logs have been analyzed. Reports saved in: {os.path.join(BASE_DIR, 'agents/graph/agents_logs_reports')}"}



