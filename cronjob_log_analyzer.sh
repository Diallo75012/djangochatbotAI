#!/usr/bin/bash
chmod +x /home/creditizens/djangochatAI/chatbotAI/log_analysis_center/log_analyzer_graph.py && cd /home/creditizens/djangochatAI/chatbotAI/log_analysis_center && /home/creditizens/djangochatAI/djangochatbotAI_venv/bin/python3 /home/creditizens/djangochatAI/chatbotAI/log_analysis_center/log_analyzer_graph.py  >> /home/creditizens/djangochatAI/chatbotAI/log_agent_reports/cronjob.log || echo "Cronjob failed at $(date)" >> /home/creditizens/djangochatAI/chatbotAI/log_agent_reports//cronjob.log

