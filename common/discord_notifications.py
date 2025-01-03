import os
from dotenv import load_dotenv
from discord_webhook import DiscordWebhook
from django.conf.settings import BASE_DIR


# load env vars
load_dotenv(dotenv_path='.env', override=False)
load_dotenv(dotenv_path=".vars.env", override=True)


DISCORD_WEBHOOK_ID = os.getenv("DISCORD_WEBHOOK_ID")
DISCORD_WEBHOOK_TOKEN = os.getenv("DISCORD_WEBHOOK_TOKEN")
DISCORD_WEBHOOK_URL = os.getenv("DISCORD_WEBHOOK_URL")
LOG_AGENT_REPORTS_FOLDER = os.path.join(BASE_DIR, 'log_agent_reports')

# max file size is 8MB dfor discord
def send_file_to_discord(file_path):
  """
  Helper function to send a single file to Discord.

  :param webhook_url: The Discord webhook URL.
  :param file_path: Path to the file to be sent.
  """
  webhook = DiscordWebhook(url=DISCORD_WEBHOOK_URL, content=f"📄 **Log Report Chunk**: {os.path.basename(file_path)}")
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
  Sends a large log file to a Discord channel using a webhook. If the file exceeds 8 MB, it splits the file into
  smaller chunks and sends each chunk separately.

  :param log_file_path: Path to the log file to be sent.
  """
  # Discord Webhook URL ressembles to this
  #"https://discord.com/api/webhooks/{DISCORD_WEBHOOK_ID}/{DISCORD_WEBHOOK_TOKEN}"

  # Define the maximum file size in bytes (8 MB) but will use smaller chunk
  #MAX_FILE_SIZE = 8 * 1024 * 1024
  MAX_FILE_SIZE = 6 * 1024 * 1024

  # loop through all files report present in the log agent report folder `log_to_analyze`
  for log_file in os.listdir(os.listdir(os.path.join(BASE_DIR, 'agents/graph/log_to_analyze'))):
    log_file_path = os.path.join(BASE_DIR, 'agents/graph/log_to_analyze', log_file)
    # if needed in later iterations; the level is critical/error/warning written at the beginning of each files in the report folder
    # log_file_level = log_file_path.split("/")[-1].split("_")[0]

    # Check if the file exists
    if not os.path.exists(log_file_path):
      print(f"Error: The file '{log_file_path}' does not exist.")
      return f"error: The file '{log_file_path}' does not exist."

    # Get the file size
    file_size = os.path.getsize(log_file_path)

    if file_size <= MAX_FILE_SIZE:
      # Send the file as-is if it's under the limit
      try:
        send_file_to_discord(log_file_path)
      except Exception as e:
        return f"error occured while trying to get file transmission result: {e}"
    else:
      # Split and send the file in chunks
      print(f"The file '{log_file_path}' exceeds 8 MB (size: {file_size / (1024 * 1024):.2f} MB). Splitting into chunks.")

      # Open the file in binary mode
      with open(log_file_path, "rb") as file:
        chunk_number = 1
        while True:
          # Read a chunk of MAX_FILE_SIZE bytes
          chunk = file.read(MAX_FILE_SIZE)
          if not chunk:
            break

          # Create a temporary chunk file
          chunk_filename = f"{log_file_path}_part{chunk_number}.log"
          with open(chunk_filename, "wb") as chunk_file:
            chunk_file.write(chunk)

            # Send the chunk to Discord
            print(f"Sending chunk {chunk_number}...")
            try:
              send_file_result = send_file_to_discord(chunk_filename)

              # Delete the temporary chunk file after sending
              os.remove(chunk_filename)
              chunk_number += 1
            except Exception as e:
              return f"error occured while trying to get file transmission result: {e}"

  print("All chunks have been sent successfully.")
  return "success all logs have been transmitted to Devops/Security team"
