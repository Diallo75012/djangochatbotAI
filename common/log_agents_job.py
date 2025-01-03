import os
from agents.graph.log_analyzer_agent_graph import logs_agent_team
from django.conf.settings import BASE_DIR
from dotenv import load_dotenv

"""
 DO NOT FORGET TO MAKE IT EXECUTABLE WHEN WETTING UP SERVER OR CONTAINER
"""

# load env vars
load_dotenv(dotenv_path='.env', override=False)
load_dotenv(dotenv_path=".vars.env", override=True)

LOG_AGENT_REPORTS_FOLDER = os.path.join(BASE_DIR, 'log_agent_reports')

def log_analisys_job(logs_folder_path: str = LOG_AGENT_REPORTS_FOLDER):
  try:
    result_log_collection_job = logs_agent_team(logs_folder_path)
    return result_log_collection_job
  except Exception as e:
    print(f"Error running LangGraph agent: {str(e)}")
    return f"Error running LangGraph agent: {str(e)}"


if __name__ == "__main__":
  try:
    logs_analysis_result = log_analysis_job(LOG_AGENT_REPORTS_FOLDER)
    with open(os.path.join(BASE_DIR, 'log_agent_reports', 'agent_log_job_result.md'), "a", encoding="utf-8") as cronjob_issue_file:
      cronjob_issue_file.write(f"Successfully ran the log agent job with result: {log_analysis_result}")

  except Exception as e:
    with open(os.path.join(BASE_DIR, 'log_agent_reports', 'agent_log_job_result.md'), "a", encoding="utf-8") as cronjob_issue_file:
      cronjob_issue_file.write(f"An exception occured while trying to run the log agent job: {e}")
