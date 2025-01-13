#!/bin/bash


# Set execute permission for the main script
chmod +x log_analysis_center/log_analyzer_graph.py

# Set execute permission for the shell script
chmod +x analyzer_log_agent_cronjob.sh

# Ensure helper files are not executable (optional, but good practice)
# chmod -x log_analysis_center/*.py

# Ensure directories are traversable
chmod 755 log_analysis_center
chmod 755 agents/graph
