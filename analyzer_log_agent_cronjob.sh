#!/bin/bash

# Variables
PROJECT_ROOT="$(dirname "$(realpath "$0")")"
PYTHON_PATH="$PROJECT_ROOT/venv/bin/python"
SCRIPT_PATH="$PROJECT_ROOT/log_analysis_center/log_analyzer_graph.py"
LOG_FILE="$PROJECT_ROOT/log_agent_reports/cronjob.log"

# Verify files and directories
if [ ! -d "$PROJECT_ROOT/venv" ]; then
  echo "Error: Virtual environment not found" >> "$LOG_FILE"
  exit 1
fi

if [ ! -f "$SCRIPT_PATH" ]; then
  echo "Error: Script not found at $SCRIPT_PATH" >> "$LOG_FILE"
  exit 1
fi

# Add cronjob
CRON_TIME="00 20 * * *"
CRON_JOB="$CRON_TIME $PYTHON_PATH $SCRIPT_PATH >> $LOG_FILE 2>&1"

if crontab -l 2>/dev/null | grep -Fq "$SCRIPT_PATH"; then
  echo "Cronjob already exists" >> "$LOG_FILE"
else
  (crontab -l 2>/dev/null; echo "$CRON_JOB") | crontab -
  echo "Cronjob added successfully" >> "$LOG_FILE"
fi
