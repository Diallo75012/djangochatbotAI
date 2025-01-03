#!/bin/bash

# make sure to call the python environment `venv`

# Variables
# Automatically find the root directory of the Django project
PROJECT_ROOT="$(dirname "$(realpath "$0")")"
# Path to the Python executable
PYTHON_PATH="$PROJECT_ROOT/venv/bin/python"
# Path to the Python script inside the common app
SCRIPT_PATH="$PROJECT_ROOT/common/log_agents_jobs.py"
# Schedule: 3:00 AM daily
CRON_TIME="0 3 * * *"

# Check if cronjob already exists for the script
if crontab -l 2>/dev/null | grep -q "$SCRIPT_PATH"; then
  echo "Cronjob already exists for the script."
else
  # Add the cronjob
  (crontab -l 2>/dev/null; echo "$CRON_TIME $PYTHON_PATH $SCRIPT_PATH") | crontab -
  echo "Cronjob added successfully."
fi
