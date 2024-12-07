
import os
import json
# for typing func parameters and outputs and states
from typing import Dict, List, Tuple, Any, Optional
# structured output
from structured_output.structured_output import (
  analyse_user_query_safety_schema,
  summarize_user_to_clear_question_schema,
  retrieve_answer_schema,
)
# prompts
from prompts.prompts import (
  analyse_user_query_safety_prompt,
  summarize_user_to_clear_question_prompt,
  retrieve_answer_prompt,
)
from typing import Dict, List, Any, Optional, Union
# utils
from app_utils import (
  call_llm,
  prompt_creation,
  answer_retriever,
)
# Tools
from app_tools.app_tools import (
  llm_with_retrieve_answer_tool_choice,
  tool_retrieve_answer_node,
)
# LLMs
from llms.llms import (
  groq_llm_mixtral_7b,
  groq_llm_llama3_8b,
  groq_llm_llama3_8b_tool_use,
  groq_llm_llama3_70b,
  groq_llm_llama3_70b_tool_use,
  groq_llm_gemma_7b,
)
# for graph creation and management
from langgraph.checkpoint import MemorySaver
from langgraph.graph import END, StateGraph, MessagesState
# display drawing of graph
from IPython.display import Image, display
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

# NODE FUNCTIONS
# api selection
def tool_api_choose_agent(state: MessagesState):
    messages = state['messages']
    last_message = messages[-1].content
    print("message state -1: ", messages[-1].content, "\nmessages state -2: ", messages[-2].content)
    # print("messages from call_model func: ", messages)
    user_initial_query = os.getenv("USER_INITIAL_QUERY")

    query = prompt_creation(tool_api_choose_agent_prompt["human"], user_initial_query=user_initial_query)
    response = llm_api_call_tool_choice.invoke(json.dumps(query))

    return {"messages": [response]}

# NODE AND CONDITIONAL EDGES FUNCTIONS
'''
EXAMPLE OF USER INPUT ANALYSIS FLOW
'''
# NODE
def analyse_user_query_safety(state: MessagesState, analyse_query_class = AnalyseUserInput):
  messages = state['messages']
  last_message = messages[-1].content
  set_key(".vars.env", "USER_INITIAL_QUERY", last_message)
  load_dotenv(dotenv_path=".vars.env", override=True)

  query = prompt_creation.prompt_creation(analyse_user_query_safety_prompt["human"], user_initial_query=last_message)
  
  # get the answer as we want it using structured output schema directly injected in prompt
  try:
    decision = call_llm.call_llm(query, analyse_user_query_safety_prompt["system"]["template"], schema, groq_llm_llama3_70b)
    if decision.safe.lower() == "true":
      return {"messages": [{"role": "ai", "content": "safe"}]}
    return {"messages": [{"role": "ai", "content": "unsafe"}]}
  except Exception as e:
    return {"messages": [{"role": "ai", "content": f"An error occured while trying to analyze user input content: {e}"}]}

# CONDITIONAL EDGE
def safe_or_not(state: MessagesState):
  messages = state['messages']
  last_message = messages[-1].content

  if last_message == "safe":
    # go to question rephraser node
    return "summarize_user_to_clear_question"
  elif last_message == "unsafe":
    # set env var for unsafe query and the Django view will take care of flagging user in the DB and creating log of that event for Devops/Security Team
    set_key(".var.env", "USER_QUERY_UNSAFE", "True")
    load_dotenv(dotenv_path=".vars.env", override=True)
    return END
  else:
    # it could be any other error, so we forward to error node
    return "error_handler"

# NODE
def summarize_user_to_clear_question(state: MessagesState):
  messages = state['messages']
  # should be 'safe' or 'unsafe'
  last_message = messages[-1].content
  user_initial_query = os.getenv("USER_INITIAL_QUERY")

  query = prompt_creation.prompt_creation(summarize_user_to_clear_question_prompt["human"], user_initial_query=user_initial_query)
  
  # rephrase user intial query to a question
  try:
    clear_question = call_llm.call_llm(query, summarize_user_to_clear_question_prompt["system"]["template"], schema, groq_llm_llama3_70b)
    if clear_question:
      question = clear_question["question"]
      set_key(".vars.env", "REPHRASED_USER_QUERY", question)
      load_dotenv(dotenv_path=".vars.env", override=True)
      return {"messages": [{"role": "ai", "content": json.dumps({"success": clear_question})}]}
    return {"messages": [{"role": "ai", "content": json.dumps({"error": f"no question key found in response: {e}"})}]}
  except Exception as e:
    return {"messages": [{"role": "ai", "content": json.dumps({"error": f"An error occured while trying to rephrase user query: {e}"})}]}

# CONDITIONAL EDGE
def question_rephrased_or_error(state: MessagesState):
  messages = state['messages']
  # should be 'success' or 'error'
  last_message = messages[-1].content

  if 'success' in last_message:
    return "retrieve_answer_agent"
  return "error_handler"

# NODE
def retrieve_answer_agent(state: MessagesState):
  rephrased_user_query = os.getenv("REPHRASED_USER_QUERY")
  prompt = prompt_creation.prompt_creation(retrieve_answer_prompt["system"], query=rephrased_user_query, response_schema=retrieve_answer_prompt_schema) 
  response = llm_with_retrieve_answer_tool_choice.invoke(json.dumps(prompt))
  # return response for the answer_retriever tool to be able to perform the retrieval task from this llm binded tool choice
  return {"messages": [response]}

# CONDITIONAL EDGE
def retrieved_answer_or_not(state: MessagesState):
  '''
  Here we will capture the answer fromt he state which is success or error
  '''
  messages = state["messages"]
  last_message = messages[-1].content
  
  if "vector_responses" or "nothing" in last_message:
    # we will evaluate 055 vs 063 in "answer_user" node
    return "answer_to_user"
  elif "error_vector" in last_message:
    return "error_handler"

'''
EXAMPLE OF ERROR HANDLING IF THREE RESPONSE BACK EXIST LIKE AFTER API CALL
'''
# error handling
def error_handler(state: MessagesState):
  messages = state['messages']
  last_three_messages_json = json.dumps([
    {
      "Error": "Find here the last 3 messages of code execution graph",
      "message -3": messages[-3].content,
      "message -2": messages[-2].content,
      "message -1": messages[-1].content,
    }
  ])
  
  with open("./logs/conditional_edge_logs.log", "a", encoding="utf-8") as conditional:
      conditional.write(f"\n\nerror handler called: {last_three_messages_json}\n\n")

  return {"messages": [{"role": "ai", "content": f"An error occured, error message: {last_three_messages_json}"}]}

# NODE
def answer_to_user(state: MessagesState):
  messages = state['messages']
  last_message = message[-1].content
  # end the graph if it is unsafe and set env var that app will fetch
  document_title = os.getenv("DOCUMENT_TITLE")
  # no need to make it JSON or Dict, we just will inject it in prompt at the right place
  ai_personality_traits = os.getenv("AI_PERSONALITY_TRAITS")
  user_initial_query_rephrased = os.getenv("REPHRASED_USER_QUERY")
  query = prompt_creation.prompt_creation(summarize_user_to_clear_question_prompt["human"], user_initial_query_rephrased=user_initial_query_rephrased)
  
  '''
    Nedd here to add if statements to check last messsage what is the level of retrieval if any and call llm then to make the final answer
  '''
  try:
    answer = call_llm(query, answer_to_user_prompt, answer_to_user_schema, groq_llm_llama3_70b, partial_variables={"ai_personality_traits": ai_personality_traits})
  except Exception as e:
    return e
'''
RETRIEVAL
Client User Flow:
  - Retrieval Flow:
    -> user send a message >
         perform a safety check on user query and if comply with law >
           - if unsafe or not comply:
               send warning to user and flag user in database and create logs for Devops/Security team 
           - if safe, perform retrieval:
               get document name, AI personality traits needed to perform retrieval and answer user >
                  > x2 retrieval layers: at treshold 0.62 for valid answer and one more at 0.5 to have some other type of questions
                 - if no data retrieved:
                     tell user disclaimer that we didn't find answer in our business data
                     but this what an internet search info about it. Then provide retrieved question form retrieved data at 0.5 if any
                      get the questions to show user which kind of question we have and can answer as sample to inform user.
'''


# Initialize states
workflow = StateGraph(MessagesState)

# nodes
workflow.add_node("error_handler", error_handler)
workflow.add_node("analyse_user_query_safety", analyse_user_query_safety)
workflow.add_node("summarize_user_to_clear_question", summarize_user_to_clear_question)
workflow.add_node("retrieve_answer_agent")
workflow.add_node("tool_retrieve_answer_node", tool_retrieve_answer_node)
worklfow.add_node("answer_to_user", answer_to_user)

# edges
workflow.set_entry_point("analyse_user_query_safety")
workflow.add_conditional_edges(
  "analyse_user_query_safety",
  safe_or_not
)
workflow.add_conditional_edges(
  "summarize_user_to_clear_question",
  question_rephrased_or_error
)
workflow.add_edge("retrieve_answer_agent", "tool_retrieve_answer_node")
workflow.add__conditonal_edge(
  "tool_retrieve_answer_node", 
  retrieved_answer_or_not
)


# end
workflow.add_edge("error_handler", END)

# compile
checkpointer = MemorySaver()
user_query_processing_stage = workflow.compile(checkpointer=checkpointer)

###############################
## GRAPH CODE LOGIC ABOVE IT ##
###############################
'''
HERE WE COULD LOG THE GRAPH EXECUTION STEPS
TO GET MAYBE LATER SOMETHING LIKE VISUAL REPRESENTATION...
'''
def code_execution_graph(user_query):
  print("Code execution Graph")
  print(f"Query: '{user_query}'")
  count = 0
  for step in user_query_processing_stage.stream(
    {"messages": [SystemMessage(content=user_query)]},
    config={"configurable": {"thread_id": int(os.getenv("THREAD_ID"))}}):
    count += 1
    if "messages" in step:
      output = beautify_output(step['messages'][-1].content)
      print(f"Step {count}: {output}")
    else:
      output = beautify_output(step)
      print(f"Step {count}: {output}")
  
  # subgraph drawing
  graph_image = code_execution_graph.get_graph().draw_png()
  with open("code_execution_subgraph.png", "wb") as f:
    f.write(graph_image)

'''
if __name__ == '__main__':
  code_execution_graph(user_query)
'''
