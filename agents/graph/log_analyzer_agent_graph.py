import os
import json
from django.conf.settings import BASE_DIR
# for typing func parameters and outputs and states
from typing import Dict, List, Tuple, Any, Optional, Union
# structured output
from agents.structured_output.structured_output import (
)
# prompts
from agents.prompts.prompts import (
)
# utils
from agents.app_utils.json_dumps_manager import safe_json_dumps
from agents.app_utils.embed_data import CONNECTION_STRING
from agents.app_utils import (
  call_llm,
  prompt_creation,
  beautiful_graph_output,
  chunk_store_alalyze_logs,
)
# Tools
from agents.tools.tools import (
)
# Retrieve Vector
from agents.app_utils.retrieve_answer import retrieve_answer_action
# LLMs
from agents.llms.llms import (
  groq_llm_mixtral_7b,
  groq_llm_llama3_8b,
  groq_llm_llama3_70b,
  groq_llm_llama3_70b_versatile,
  groq_llm_gemma_7b,
)
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage, ToolMessage
# for graph creation and management
# this has changed with version upgrade of langgraph it is in langgraph.checkpoint.memory that we find MemorySaver
# from langgraph.checkpoint import MemorySaver
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import END, StateGraph, MessagesState
# env vars
from dotenv import load_dotenv, set_key


# load env vars
load_dotenv(dotenv_path='.env', override=False)
load_dotenv(dotenv_path=".vars.env", override=True)

# Helper functions
def message_to_dict(message):
    if isinstance(message, (AIMessage, HumanMessage, SystemMessage, ToolMessage)):
        return {
            "content": message.content,
            "additional_kwargs": message.additional_kwargs,
            "response_metadata": message.response_metadata if hasattr(message, 'response_metadata') else None,
            "tool_calls": message.tool_calls if hasattr(message, 'tool_calls') else None,
            "usage_metadata": message.usage_metadata if hasattr(message, 'usage_metadata') else None,
            "id": message.id,
            "role": getattr(message, 'role', None),
        }
    return message

def convert_to_serializable(data):
    if isinstance(data, list):
        return [convert_to_serializable(item) for item in data]
    elif isinstance(data, dict):
        return {k: convert_to_serializable(v) for k, v in data.items()}
    elif isinstance(data, (AIMessage, HumanMessage, SystemMessage, ToolMessage)):
        return message_to_dict(data)
    return data

def beautify_output(data):
    serializable_data = convert_to_serializable(data)
    return json.dumps(serializable_data, indent=4)

# NODES
def copy_log_files(state: StateMessages):
  '''
    Function that will copy file from the root directory to a folder special for log analysis
    The log analysis folder will hold temporary files that will be deleted at the end of the graph
  '''
  
  # get all the logs files
  log_file_list = [log_file for log_file in os.path.join(BASE_DIR, 'logs')]
  # check if the dir exist or make it anyways (dir where logs will be copied for dedicsted analysis job)
  try:
    os.makedirs(os.path.join(BASE_DIR, 'agents/graph/logs_to_analize'), exist_ok=True)
  except Exception as e:
    return f"An error occured while trying check if agent log dir exist and if not create it: {e}"

  # loop through the file and copy each of those to the log analyzer folder
  try:
    for elem in log_file_list:
      with open(os.path.join(BASE_DIR, 'logs', elem), 'r', encoding="utf-8") as original_log_file, with open(os.path.join(BASE_DIR, 'agents/graph/logs_to_analize', elem), 'w', encoding="utf-8") as log_file_copy_for_analysis:
        log_file_content = original_log_file.read()
        log_file_copy_for_analysis.write(log_file_content)
    # success message sent with the log file names list so that we can open those in the next chunking/storing node
    return  {"messages": [{"role": "ai", "content": json.dumps({"success": log_file_list})}]}    
  except Exception as e:
    return {"messages": [{"role": "ai", "content": json.dumps({"error": f"An error occured while trying to copy log file {e}"})}]} 

# CONDITIONAL EDGE
def copy_log_files_success_or_error(state: MessagesState):
  messages = state['messages']
  # should be 'success' or 'error'
  last_message = messages[-1].content

  if 'success' in last_message:
    return "chunk_and_store_logs"
  return "error_handler"

# NODE
def chunk_and_store_logs(state: StateMessages):
  messages = state['messages']
  # contains a list of the log file names
  last_message = messages[-1].content
  logs_file_names = json.loads(last_message)["success"]
  flags = os.getenv("FLAGS")
  # one chunk is one log line, therefore we get each line and will on the fly parse and store to database
  # only logs that we need to analyze (critical/error/warning)
  try:
    chunk_store_analyze_logs.chunk_store_logs(flags, logs_file_names, CONNECTION_STRING)
    return  {"messages": [{"role": "ai", "content": json.dumps({"success": "Logs chunks successfully selected and stored"})}]}
  except Exception as e:
    return {"messages": [{"role": "ai", "content": json.dumps({"error": f"An error occured while trying to chunk and store logs: {e}"})}]}

# CONDITIONAL EDGE
def chunk_and_store_logs_success_or_error(state: MessagesState):
  messages = state['messages']
  # should be 'success' or 'error'
  last_message = messages[-1].content

  if 'success' in last_message:
    return "classify_and_store_schematize_flagged_logs"
  return "error_handler"

def classify_and_store_schematize_flagged_logs(state: StateMessages):
  # this one might be combined with the node storing logs as we can classify just bay splitting the log line which is already formatted and detect critial/error/warning
  continue

def advice_agent_report_creator(state: StateMessages):
  continue

def notifier_agent(state: StateMessages):
  continue

def temporary_log_files_cleaner(state: StateMessages):
  continue



# CONDITIONAL EDGE
def question_rephrased_or_error(state: MessagesState):
  messages = state['messages']
  # should be 'success' or 'error'
  last_message = messages[-1].content

  if 'success' in last_message:
    return "retrieve_answer_action"
  return "error_handler"

# error handling
def error_handler(state: MessagesState):
  messages = state['messages']

  # Log the graph errors in a file
  with open("logs/logs_analyzer_agent_graph.log", "a", encoding="utf-8") as conditional:
      json_error_message = messages[-1].content
      conditional.write(f"\n\n{json_error_message}\n\n")
  print(f"Error Handler: ", messages[-1].content)

  return {"messages": [{"role": "ai", "content": json.dumps({"error_handler": messages[-1].content})}]}


'''
LOG ANALYZER
- Copy log file
- chunk and store to SQLite
- Classify Logs : check chunks for error, warning, critical flags
- Provide Advice: Get from error, critical, warning flagged schemas
- Notify Devops/Security (email, discord, slack.....)
'''

# Initialize states
workflow = StateGraph(MessagesState)

# nodes
workflow.add_node("copy_log_files", copy_log_files)
workflow.add_node("chunk_and_store_logs", chunk_and_store_logs )
workflow.add_node("classify_and_store_schematize_flagged_logs", classify_and_store_schematize_flagged_logs)
workflow.add_node("advice_agent_report_creator", advice_agent_report_creator)
worklfow.add_node("notifier_agent", notifier_agent)
workflow.add_node("temporary_log_files_cleaner", temporary_log_files_cleaner)

# start
workflow.set_entry_point("copy_log_files")

# edges
workflow.add_conditional_edges(
  "copy_log_files",
  copy_log_files_success_or_error
)
workflow.add_conditional_edges(
  "chunk_and_store_logs",
  chunk_and_store_logs_success_or_error
)

# probably will be truned all in conditional edges
workflow.add_edge("classify_and_store_schematize_flagged_logs", "advice_agent_report_creator")
workflow.add_edge("advice_agent_report_creator", "notifier_agent")
workflow.add_edge("notifier_agent", "temporary_log_files_cleaner")

# end
workflow.add_edge("error_handler", END)
workflow.add_edge("temporary_log_files_cleaner", END)

# compile
checkpointer = MemorySaver()
user_query_processing_stage = workflow.compile(checkpointer=checkpointer)

###############################
## GRAPH CODE LOGIC ABOVE IT ##
###############################
def logs_agent_team(logs_folder_path):
  print("Logs Agents AI Team Startooooooo !!!")
  final_output = None

  count = 0
  for step in user_query_processing_stage.stream(
    {"messages": [SystemMessage(content=logs_folder_path)]},
    config={"configurable": {"thread_id": int(os.getenv("THREAD_ID"))}}):
    count += 1

    if "messages" in step:
      final_output = step['messages'][-1].content
      output = beautiful_graph_output.beautify_output(step['messages'][-1].content)
      print(f"Step {count}: {output}")
    else:
      output = beautiful_graph_output.beautify_output(step)
      print(f"Step {count}: {output}")
      try:
        final_output = safe_json_dumps(step)
      except TypeError as e:
        final_output = json.dumps({"error": f"Invalid final output format: {e}"})

  # subgraph drawing
  graph_image = user_query_processing_stage.get_graph().draw_png()
  with open("logs_agent_team.png", "wb") as f:
    f.write(graph_image)

  # Ensure final_output is JSON formatted for downstream consumption
  if isinstance(final_output, str):
    try:
      # Ensure valid JSON; if not, wrap in a standard error message
      json.loads(final_output)
    except json.JSONDecodeError:
      final_output = json.dumps({"error": "Invalid final output format"})

  # final_output_agent content should be of type json.dumps() as we json.dumped all transmitted messages
  #final_output_agent = final_output["messages"][-1]["content"]
  '''
    write final out to a file for debugging
  '''
  with open("logs/logs_agent_final_output.log", "w", encoding="utf-8") as final_output_log:
    final_output_log.write(json.dumps({"final_output": final_output}))
  return final_output


"""
if __name__ == '__main__':
  import json
  load_dotenv()
  logs_agent_team(user_query)
"""
