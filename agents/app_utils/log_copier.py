import os
import json
from typing import Dict
from django.conf import settings


def copy_logs(folder_name: str) -> Dict[str,str]: 
  """
    Copies logs from origin folder to log anamyzer agent workspace folder
  """
  
  # get all the logs files
  log_file_list = [log_file for log_file in os.listdir(os.path.join(settings.BASE_DIR, folder_name))] or ["nothing"]
  
  # check if the dir exist or make it anyways (dir where logs will be copied for dedicsted analysis job)
  try:
    os.makedirs(os.path.join(settings.BASE_DIR, 'agents/graph/logs_to_analyze'), exist_ok=True)
  except Exception as e:
    return {"error": f"An error occured while trying check if agent log dir exist and if not create it: {e}"}

  # loop through the file and copy each of those to the log analyzer folder
  try:
    if log_file_list[0] == "nothing":
      return {"nothing": "An error occured origin log folder is empty, log_file_list is equal to: {log_file_list}"}
    for elem in log_file_list:
      source_path = os.path.join(settings.BASE_DIR, folder_name, elem)
      destination_path = os.path.join(settings.BASE_DIR, 'agents/graph/logs_to_analyze', elem)
      # Read from the source and write to the destination
      with open(source_path, 'r', encoding="utf-8") as original_log_file:
        with open(destination_path, 'w', encoding="utf-8") as log_file_copy_for_analysis:
          log_file_content = original_log_file.read()
          log_file_copy_for_analysis.write(log_file_content)
    print("Success logs have been copied")
    return {"success": json.dumps(log_file_list)}
  except Exception as e:
    print("Exception while copying logs in copy_logs")
    return {"error": "An exception occured while trying to copy logs to agent workspace folder: {e}"}
