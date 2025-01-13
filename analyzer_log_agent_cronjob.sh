#!/bin/bash

# Ensure the script is executable
# chmod +x analyzer_log_agent_cronjob.sh

# Variables
# Automatically find the root directory of the Django project
PROJECT_ROOT="$(dirname "$(realpath "$0")")"
# Path to the Python virtual environment
VENV_PATH="$PROJECT_ROOT/venv"
# Python executable within the virtual environment
PYTHON_PATH="$VENV_PATH/bin/python"
# Path to the Python script
SCRIPT_PATH="$PROJECT_ROOT/log_analysis_center/log_analyzer_graph.py"
# Directory to store cronjob logs
LOG_DIR="$PROJECT_ROOT/log_agent_reports"
# Log file for the cronjob
LOG_FILE="$LOG_DIR/cronjob.log"

# Cronjob schedule: 3:00 AM daily
CRON_TIME="0 1 * * *"

# Verify the virtual environment exists
if [ ! -d "$VENV_PATH" ]; then
  echo "Error: Virtual environment not found at $VENV_PATH. Please ensure it exists."
  exit 1
fi

# Verify the Python script exists
if [ ! -f "$SCRIPT_PATH" ]; then
  echo "Error: Script not found at $SCRIPT_PATH. Please check the path."
  exit 1
fi

# Generate the cronjob entry
CRON_JOB="$CRON_TIME cd $PROJECT_ROOT && source $VENV_PATH/bin/activate && $PYTHON_PATH $SCRIPT_PATH >> $LOG_FILE 2>&1"

# Check if the cronjob already exists
if crontab -l 2>/dev/null | grep -Fq "$SCRIPT_PATH"; then
  echo "Cronjob already exists for the script."
else
  # Add the cronjob
  (crontab -l 2>/dev/null; echo "$CRON_JOB") | crontab -
  echo "Cronjob added successfully."
fi
