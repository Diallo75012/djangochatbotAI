import os
import json
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
from agents.app_utils import (
  call_llm,
  prompt_creation,
  beautiful_graph_output,
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
  groq_llm_llama3_8b_tool_use,
  groq_llm_llama3_70b,
  groq_llm_llama3_70b_tool_use,
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

def chunk_and_store_logs(state: StateMessages):
  continue

def classify_and_store_schematize_flagged_logs(state: StateMessages):
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
  with open("logs/logs_agent_graph.log", "a", encoding="utf-8") as conditional:
      json_error_message = messages[-1].content
      conditional.write(f"\n\n{json_error_message}\n\n")
  print(f"Error Handler: ", messages[-1].content)

  return {"messages": [{"role": "ai", "content": json.dumps({"error_handler": messages[-1].content})}]}


'''
LOG ANALYZER
- Copy log file
- chunk and store to SQLite
- Classify Logs : check chunks for error, alert, critical flags
- Provide Advice: Get from error, critical, alert flagged schemas
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

# edges
workflow.set_entry_point("analyse_user_query_safety")
'''
workflow.add_conditional_edges(
  "",
  ...
)
'''
# probably will be truned all in conditional edges
workflow.add_edge("copy_log_files", "chunk_and_store_logs")
workflow.add_edge("chunk_and_store_logs", "classify_and_store_schematize_flagged_logs")
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
