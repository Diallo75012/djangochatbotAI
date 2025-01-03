import os
from typing import Dict


def copy_logs(fodler_name: str) -> Dict[str,str]: 
  """
    Copies logs from origin folder to log anamyzer agent workspace folder
  """
  
  # get all the logs files
  log_file_list = [log_file for log_file in os.listdir(os.path.join(BASE_DIR, folder_name)) else "nothing"]
  
  # check if the dir exist or make it anyways (dir where logs will be copied for dedicsted analysis job)
  try:
    os.makedirs(os.path.join(BASE_DIR, 'agents/graph/logs_to_analize'), exist_ok=True)
  except Exception as e:
    return {"error": f"An error occured while trying check if agent log dir exist and if not create it: {e}"}

  # loop through the file and copy each of those to the log analyzer folder
  try:
    if log_file_list[0] == "nothing":
      return {"nothing": "An error occured origin log folder is empty, log_file_list is equal to: {log_file_list}"}
    for elem in log_file_list:
      with open(os.path.join(BASE_DIR, folder_name, elem), 'r', encoding="utf-8") as original_log_file, with open(os.path.join(BASE_DIR, 'agents/graph/logs_to_analize', elem), 'w', encoding="utf-8") as log_file_copy_for_analysis:
        log_file_content = original_log_file.read()
        log_file_copy_for_analysis.write(log_file_content)
    return {"success": "all original log files copied to agent workspace folder"}
  except Exception as e:
    return {"error": "An exception occured while trying to copy logs to agent workspace folder: {e}"}
