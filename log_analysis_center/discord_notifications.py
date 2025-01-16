import os
import json
from dotenv import load_dotenv
from discord_webhook import DiscordWebhook
#from django.conf import settings # can't import from setting or set env var to do that while running standalone script so we just build the BASE_DIR from here
#BASE_DIR = settings.BASE_DIR
from pathlib import Path # this to be used when running as standalone
BASE_DIR = Path(__file__).resolve().parent.parent


# load env vars
load_dotenv(dotenv_path='../.env', override=False)
load_dotenv(dotenv_path="../.vars.env", override=True)
#load_dotenv(dotenv_path='.env', override=False)
#load_dotenv(dotenv_path=".vars.env", override=True)

DISCORD_WEBHOOK_ID = os.getenv("DISCORD_WEBHOOK_ID")
DISCORD_WEBHOOK_TOKEN = os.getenv("DISCORD_WEBHOOK_TOKEN")
DISCORD_WEBHOOK_URL = os.getenv("DISCORD_WEBHOOK_URL")
log_agent_final_report_folder = os.getenv("LOG_AGENT_REPORTS_FOLDER")
LOG_AGENT_REPORTS_FOLDER = os.path.join(BASE_DIR, log_agent_final_report_folder)

# max file size is 8MB dfor discord
def send_file_to_discord(file_path):
  """
  Helper function to send a single file to Discord.

  :param webhook_url: The Discord webhook URL.
  :param file_path: Path to the file to be sent.
  """
  webhook = DiscordWebhook(url=f"{DISCORD_WEBHOOK_URL}/{DISCORD_WEBHOOK_ID}/{DISCORD_WEBHOOK_TOKEN}", content=f"📄 **Log Report Chunk**: {os.path.basename(file_path)}")
  try:
    with open(file_path, "rb") as file:
      # max file size is 8MB
      webhook.add_file(file=file.read(), filename=os.path.basename(file_path))

    response = webhook.execute()

    if response.status_code == 200:
      print(f"Chunk {os.path.basename(file_path)} sent successfully.")
      return "success"
    else:
      print(f"Failed to send chunk {os.path.basename(file_path)}. HTTP Status Code: {response.status_code}")
      print(response.content)
      raise Exception(f"failed: HTTP status code was {response.status_code}")
  except Exception as e:
    print(f"An unexpected error occurred while sending {file_path}: {e}")
    return f"error while trying to send file to discord: {e}"

def send_agent_log_report_to_discord(log_report_folder_path: str = LOG_AGENT_REPORTS_FOLDER):
  """
    Sends log files to a Discord channel using a webhook. Handles files exceeding Discord's file size limit
    by splitting them into smaller chunks.

    :param log_report_folder_path: Path to the folder containing log files to send.
  """
  MAX_FILE_SIZE = 6 * 1024 * 1024  # 6 MB
  log_analyzer_advice_to_send_to_discord_folder = os.getenv("LOG_ANALYZER_ADVICE_TO_SEND_DISCORD_FOLDER")
  
  if not log_analyzer_advice_to_send_to_discord_folder:
    return {"status": "error", "message": "Environment variable COPY_LOGS_DESTINATION_FOLDER is not set."}

  error_messages = []  # Track errors for reporting

  print("log_analyzer_advice_to_send_to_discord_folder: ", log_analyzer_advice_to_send_to_discord_folder)
  print("os.listdir(os.path.join(BASE_DIR, log_analyzer_advice_to_send_to_discord_folder)): ", 
        os.listdir(os.path.join(BASE_DIR, log_analyzer_advice_to_send_to_discord_folder)))

  for log_file in os.listdir(os.path.join(BASE_DIR, log_analyzer_advice_to_send_to_discord_folder)):
    print("log_file: ", log_file)
    log_file_path = os.path.join(BASE_DIR, log_analyzer_advice_to_send_to_discord_folder, log_file)
    print("log_file_path: ", log_file_path)

    # Check if the file exists
    if not os.path.exists(log_file_path):
      error_message = f"Error: The file '{log_file_path}' does not exist."
      print(error_message)
      error_messages.append(error_message)
      continue

    file_size = os.path.getsize(log_file_path)

    # If the file is small enough, send directly
    if file_size <= MAX_FILE_SIZE:
      try:
        send_result = send_file_to_discord(log_file_path)
        if send_result != "success":
          error_messages.append(f"Failed to send {log_file_path}: {send_result}")
      except Exception as e:
        error_message = f"Error while sending {log_file_path}: {e}"
        print(error_message)
        error_messages.append(error_message)
    else:
      # If the file exceeds the size limit, split and send in chunks
      print(f"The file '{log_file_path}' exceeds 6 MB (size: {file_size / (1024 * 1024):.2f} MB). Splitting into chunks.")
      try:
        with open(log_file_path, "rb") as file:
          chunk_number = 1
          while True:
            chunk = file.read(MAX_FILE_SIZE)
            if not chunk:
              break

            chunk_filename = f"{log_file_path}_part{chunk_number}.log"
            with open(chunk_filename, "wb") as chunk_file:
              chunk_file.write(chunk)

            try:
              send_result = send_file_to_discord(chunk_filename)
              if send_result != "success":
                error_messages.append(f"Failed to send chunk {chunk_filename}: {send_result}")
            except Exception as e:
              error_message = f"Error while sending chunk {chunk_filename}: {e}"
              print(error_message)
              error_messages.append(error_message)
            finally:
              os.remove(chunk_filename)  # Cleanup temporary chunk files
              chunk_number += 1
      except Exception as e:
        error_message = f"Error while processing chunks for {log_file_path}: {e}"
        print(error_message)
        error_messages.append(error_message)

  # Final status determination
  if error_messages:
    print("Errors occurred during the process:")
    for error in error_messages:
      print(error)
    return {"error": error_messages}
    
  print("All chunks have been sent successfully.")
  return {"success": "All logs have been transmitted to DevOps/Security team."}


