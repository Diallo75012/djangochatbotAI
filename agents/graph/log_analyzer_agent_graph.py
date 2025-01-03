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
from agents.app_utils.log_advice_report_creation import CONNECTION_STRING
from agents.app_utils.delete_log_analyzer_data import (
  delete_flagged_log_from_db_table,
  delete_all_files_in_dir(directory_path,
)
from agents.app_utils.log_copier import copy_logs
from agents.app_utils import (
  call_llm,
  prompt_creation,
  beautiful_graph_output,
  chunk_store_alalyze_logs,
  logs_advice_report_creation,
)
# Tools
from agents.tools.tools import (
  log_analyzer_notififier_tool,
  llm_with_log_analyzer_notififier_tool_choice,
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

# log folder from agents
LOG_AGENT_REPORTS_FOLDER = os.path.join(BASE_DIR, 'log_agent_reports')

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
  count_no_log_file_in_folder_tracker = 0
  django_and_rust_logs_fodler_names = [os.getenv("DJANGO_LOGS_FOLDER_NAMER"), os.getenv("RUST_LOGS_FOLDER_NAME")]
  for log_folder_name in  django_and_rust_logs_fodler_names:
    try:
      copy_logs_job_result = copy_logs(log_folder_name)
      if "success" in copy_logs_job_result:
        # success message sent with the log file names list so that we can open those in the next chunking/storing node
        return  {"messages": [{"role": "ai", "content": json.dumps({"success": log_file_list})}]}
      elif "nothing" in copy_logs_job_result:
        count_no_log_file_in_folder_tracker += 1
      elif "error" in copy_logs_job_result:
        return {"messages": [{"role": "ai", "content": json.dumps({"error": f"An error occured while trying to copy log file: {['error']}"})}]} 
    except Exception as e:
      return {"messages": [{"role": "ai", "content": json.dumps({"error": f"An exception occured while trying to copy log file {e}"})}]} 

  # here we check as we can have also issue with log folder empty
  if len(count_no_log_file_in_folder_tracker) == len(django_and_rust_logs_fodler_names):
    return {"messages": [{"role": "ai", "content": json.dumps({"empty": f"error as log folders are all empty, agent couldn't proceed to any analysis job."})}]} 

# CONDITIONAL EDGE
def copy_log_files_success_or_error(state: MessagesState):
  messages = state['messages']
  # should be 'success' or 'error'
  last_message = messages[-1].content

  if "empty" in last_message:
    # we don't need to run the graph nodes if the log folders are empty, we stop graph.
    return END
  elif 'success' in last_message:
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
    return "advice_agent_report_creator"
  return "error_handler"

# NODE
def advice_agent_report_creator(state: StateMessages):
  messages = state['messages']
  # contains success message
  last_message = messages[-1].content
  if "success" in json.dumps(last_message):
    # get the chunk from database and call llm to get advice on it
    # make a report on the fly for the error in a special `agents_logs_report` folder
    flags = json.laods(os.getenv("FLAGS")) # list of log levels
    # We get advice and report made, the for loop on the `FLAGS` will be done there
    try:
      # should return a dict with `success` or `error`
      advice_log_report_response = get_advice_on_logs(flags)
      if "error" in advice_log_report_response:
        return {"messages": [{"role": "ai", "content": json.dumps({"error": f"An error occured while trying to get advice log report: {advice_log_report_response['error']}"})}]}
      return  {"messages": [{"role": "ai", "content": json.dumps({"success": f"Successfully created log reports: {advice_log_report_response['success']}"})}]}
    except Exception as e:
      return {"messages": [{"role": "ai", "content": json.dumps({"error": f"An error occured while trying to produce advice report on logs: {e}"})}]}

# CONDITIONAL EDGE    
def advice_agent_report_creator_success_or_error(state: StateMessages):
  messages = state['messages']
  # should be 'success' or 'error'
  last_message = messages[-1].content

  if 'success' in last_message:
    return "tool_notifier_agent"
  return "error_handler"

def tool_notifier_agent(state: StateMessages):
    messages = state['messages']
    last_message = messages[-1].content
    # print("messages from call_model func: ", messages)
    query = prompt_creation(tool_notifier_agent_prompt["human"], folder_name_parameter=LOG_AGENT_REPORTS_FOLDER)
    response = llm_with_log_analyzer_notififier_tool_choice.invoke(json.dumps(query))

    return {"messages": [response]}

# CONDITIONAL EDGE    
def discord_notification_flow_success_or_error(state: StateMessages):
  messages = state['messages']
  # should be 'success' or 'error'
  last_message = json.loads(messages[-1].content)

  if 'success' in last_message:
    return "temporary_log_files_cleaner"
  return "error_handler"

# NODE
def temporary_log_files_cleaner(state: StateMessages):

  # here we will delete the databases entries and empty the agent `LogAnalyzer` model
  try:
    delete_flagged_logs_from_table_result = delete_flagged_log_from_db_table(connection: str = CONNECTION_STRING)
    if "error" in delete_flagged_logs_from_table_result:
      return {"messages": [{"role": "ai", "content": json.dumps({"error": f"An error occured while trying to delete logs from database: {delete_flagged_logs_from_table_result['error']}"})}]}
  except Exception as e:
    return {"messages": [{"role": "ai", "content": json.dumps({"error": f"An exception occured while trying to delete logs from database: {e}"})}]}

  # herewe will delete all copied log files from the agent workspace folder
  try:
    delete_initialy_copied_log_result = delete_all_files_in_dir()
    if "error" in delete_initialy_copied_log_result:
      return {"messages": [{"role": "ai", "content": json.dumps({"error": f"An error occured while trying to delete logs from agent log copy folder: {delete_initialy_copied_log_result['error']}"})}]}
  except Exception as e:
    return {"messages": [{"role": "ai", "content": json.dumps({"error": f"An exception occured while trying to delete logs from database: {e}"})}]}

  return  {"messages": [{"role": "ai", "content": json.dumps({"success": f"{delete_flagged_logs_from_table_result['success']}\ndeleted all temporary files for agent initially copied logs: {delete_initialy_copied_log_result ['success']}."})}]}

# error handling
def error_handler(state: MessagesState):
  messages = state['messages']

  # Log the graph errors in a file
  with open(os.path.join(BASE_DIR, 'log_agent_reports', 'logs_analyzer_agent_graph.log'), "a", encoding="utf-8") as conditional:
      json_error_message = messages[-1].content
      conditional.write(f"\n\n{json_error_message}\n\n")
  print(f"Error Handler: ", messages[-1].content)

  return {"messages": [{"role": "ai", "content": json.dumps({"error_handler": messages[-1].content})}]}

# CONDITIONAL EDGE    
def temporary_log_files_cleaner_success_or_error(state: StateMessages):
  messages = state['messages']
  # should be 'success' or 'error'
  last_message = json.loads(messages[-1].content)

  if 'success' in last_message:
    return END
  return "error_handler"

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
workflow.add_node("advice_agent_report_creator", advice_agent_report_creator)
worklfow.add_node("log_analyzer_notififier_tool_node", log_analyzer_notififier_tool_node)
worklfow.add_node("tool_notifier_agent", tool_notifier_agent)
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
workflow.add_conditional_edges(
  "advice_agent_report_creator",
  advice_agent_report_creator_success_or_error
)
workflow.add_edge("tool_notifier_agent", "log_analyzer_notififier_tool_node")
workflow.add_conditional_edges(
  "log_analyzer_notififier_tool_node",
  discord_notification_flow_success_or_error
)
workflow.add_conditional_edges(
  "temporary_log_files_cleaner",
  # if success the this will end here otherwise it will go to error_handler which will end the graph
  temporary_log_files_cleaner_success_or_error
)
# end
workflow.add_edge("error_handler", END)
# compile
checkpointer = MemorySaver()
log_analyzer_agent_processing_stage = workflow.compile(checkpointer=checkpointer)

###############################
## GRAPH CODE LOGIC ABOVE IT ##
###############################
def logs_agent_team(logs_folder_path):
  print("Logs Agents AI Team Startooooooo !!!")
  final_output = None

  count = 0
  for step in log_analyzer_agent_processing_stage.stream(
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
  graph_image = log_analyzer_agent_processing_stage.get_graph().draw_png()
  with open(os.path.join(BASE_DIR, 'log_agent_reports', 'logs_agent_team.png'), "wb") as f:
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
