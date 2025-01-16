import os
import json
# for typing func parameters and outputs and states
from typing import Dict, List, Tuple, Any, Optional
# one is @tool decorator and the other Tool class
from langchain_core.tools import tool, Tool
from langgraph.graph import MessagesState
from langgraph.prebuilt import ToolNode
from langchain_community.tools import (
  # Run vs Results: Results have more information
  DuckDuckGoSearchRun,
  DuckDuckGoSearchResults
)
from llms import (
  groq_llm_mixtral_7b,
  groq_llm_mixtral_larger,
  groq_llm_llama3_8b,
  groq_llm_llama3_70b,
  groq_llm_llama3_70b_versatile,
  groq_llm_llama3_vision_large,
  groq_llm_gemma_7b,
)
from discord_notifications import send_agent_log_report_to_discord
from dotenv import load_dotenv
#from django.conf import settings # can't import from setting or set env var to do that while running standalone script so we just build the BASE_DIR from here
#BASE_DIR = settings.BASE_DIR
from pathlib import Path
BASE_DIR = Path(__file__).resolve().parent

# load env vars
load_dotenv(dotenv_path='../.env', override=False)
load_dotenv(dotenv_path="../.vars.env", override=True)
#load_dotenv(dotenv_path='.env', override=False)
#load_dotenv(dotenv_path=".vars.env", override=True)


# TOOLS

# will use notify devops/security team in discord
@tool
def notify_devops_security(state: MessagesState = MessagesState()):
    """
    Sends Discord notification to DevOps/Security team.

    Parameters:
    None

    Returns:
    A dictionary with success or error messages.
    """
    agent_report_folder_path = os.path.join(BASE_DIR, 'log_agent_reports')
    try:
        notification_result = send_agent_log_report_to_discord(agent_report_folder_path)
        if "success" in notification_result:
            return {"messages": [{"role": "ai", "content": json.dumps({"success": notification_result})}]}
        return {"messages": [{"role": "ai", "content": json.dumps({"error": notification_result})}]}
    except Exception as e:
        return {"messages": [{"role": "ai", "content": json.dumps({"error": f"An exception occurred while trying to notify on discord: {e}"})}]}


####################################
### THIS TO BE USED AND EXPORTED ###
####################################

# log analyzer notifier tool
llm_with_log_analyzer_notififier_tool_choice = groq_llm_llama3_70b_versatile.bind_tools([notify_devops_security])
log_analyzer_notififier_tool_node = ToolNode([notify_devops_security])

