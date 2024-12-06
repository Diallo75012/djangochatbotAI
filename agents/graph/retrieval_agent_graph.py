
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
)
# Tools
from app_tools.app_tools import (
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

  query = prompt_creation.prompt_creation(analyse_user_query_safety_prompt["human"], user_initial_query=user_initial_query)
  
  # get the answer as we want it using structured output schema directly injected in prompt
  try:
    decision = call_llm.call_llm(query, analyse_user_query_safety_prompt["system"]["template"], schema, groq_llm_llama3_70b)
    if decision.safe.lower() == "true":
      return {"messages": [{"role": "ai", "content": "safe"}]}
    return {"messages": [{"role": "ai", "content": "unsafe"}]}
  except Exception as e:
    return {"messages": [{"role": "ai", "content": f"An error occured while trying to analyze user input content: {e}"}]}

# CONDITIONAL EDGE
def safe_or_not(state: MessageState):
  message = state['messages']
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
def summarize_user_to_clear_question(state: MessageState):
  message = state['messages']
  # should be 'safe' or 'unsafe'
  last_message = messages[-1].content
  user_initial_query = os.getenv("USER_INITIAL_QUERY")

  query = prompt_creation.prompt_creation(summarize_user_to_clear_question_prompt["human"], user_initial_query=user_initial_query)
  
  # rephrase user intial query to a question
  try:
    clear_question = call_llm.call_llm(query, summarize_user_to_clear_question_prompt["system"]["template"], schema, groq_llm_llama3_70b)
    return {"messages": [{"role": "ai", "content": json.dumps({"success": clear_question.question})}]}
  except Exception as e:
    return {"messages": [{"role": "ai", "content": json.dumps({"error": f"An error occured while trying to rephrase user query: {e}"})}]}

# CONDITIONAL EDGE
def question_rephrased_or_error(state: MessageState):
  message = state['messages']
  # should be 'success' or 'error'
  last_message = messages[-1].content

  if 'success' in last_message:
    return "retrieve_answer"
  return "error_handler"

# NODE
def retrieve_answer(state: MessageState):
  set_key(".vars.env", "USER_INITIAL_QUERY", last_message)
  load_dotenv(dotenv_path=".vars.env", override=True)

   # vars
    messages = state['messages']
    last_message = messages[-1].content
    table_name: str = os.getenv("TABLE_NAME")
    query: str = last_message
    score: float = float(os.getenv("SCORE"))
    top_n: int = int(os.getenv("TOP_N"))

      try:
        # returns List[Dict]
        cached_response = fetch_cached_response_by_hash(query)
        if cached_response:
          #return {"exact_match_search_response_from_cache": cached_response}
          return {"messages": [{"role": "ai", "content": f"success_hash: {cached_response}"}]}
      except Exception as e:
        print(f"An error occured while trying to fetch cached response by hash: {e}")
        return {"messages": [{"role": "ai", "content": f"error_hash: An error occured while trying to fetch cached response by hash: {e}"}]}



      # Perform vector search with score if semantic search is not relevant
      try:
          response = answer_retriever(table_name, query, score, top_n)
  print("JSON RESPONSE: ", json.dumps(response, indent=4))

        print("Cache had nothing, therefore, performing vectordb search, response: ", vector_response)
        if vector_response:
            # Cache the new response with TTL
            try:
              """
              HERE CACHE THE RESPONSE WITH THE QUESTION IN THE USER INDEX OF THE CACHE
              """
              return {"messages": [{"role": "ai", "content": f"success_vector_retrieved_and_cached: {vector_response}"}]}
            except Exception as e:
              return {"messages": [{"role": "ai", "content": f"error_vector_retrieved_and_cached: An error occured while trying to cache the vector search response: {e}"}]}
            #return {"vector_search_response_after_cache_failed_to_find": vector_response}
      except Exception as e:
        print(f"An error occured while trying to perform vectordb search query {e}")
        return {"messages": [{"role": "ai", "content": f"error_vector: An error occured while trying to perform vectordb search query: {e}"}]}
    
    # If no relevant result found, return a default response, and perform maybe after that an internet search and cache the query and the response
    return {"messages": [{"role": "ai", "content": f"nothing_in_cache_nor_vectordb: {query}."}]}



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


'''
EXAMPLE FUNCTION CALLING WITH SCHEMA
'''
# judging documentation created agent
def documentation_steps_evaluator_and_doc_judge(state: MessagesState, apis = apis, code_doc_eval_class = CodeDocumentationEvaluation):
  """
    Will judge the documentation and return 'rewrite' to rewrite the documentation or 'generate' to start generating the script
  """
  # documentation written by agent
  messages = state["messages"]
  documentation = messages[-1].content
  # user inital query
  user_initial_query = os.getenv("USER_INITIAL_QUERY")
  # api chosen to satisfy query
  api_choice = os.getenv("API_CHOICE")
  # links for api calls for each apis existing in our choices of apis
  apis_links = apis
  
  # we need to fill this template with the input variables to create the query form 'human' side of the rpompt template
  query = prompt_creation(rewrite_or_create_api_code_script_prompt["human"], documentation=documentation, user_initial_query=user_initial_query, api_choice=api_choice, apis_links=apis_links)
  # get the answer as we want it using structured output
  try:

    decision = call_llm(query, rewrite_or_create_api_code_script_prompt["system"]["template"], schema, groq_llm_llama3_70b)

    if decision["decision"] == "rewrite":
      print("DECISION: rewrite")
      return {"messages": [{"role": "ai", "content": json.dumps({"disagree":decision})}]} # use spliting technique to get what is wanted 
    elif decision["decision"] == "generate":
      print("DECISION: generate")
      return {"messages": [{"role": "ai", "content": json.dumps({"success":"generate"})}]}
    else:
      print("DECISION: error")
      return {"messages": [{"role": "ai", "content": json.dumps({"error":decision})}]}
  except Exception as e:
    print("Exception Triggered")
    return {"messages": [{"role": "ai", "content": json.dumps({"error":e})}]} 


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
                     perform internet search and tell user disclaimer that we didn't find answer in our business data
                     but this what an internet search info about it. Then provide retrieved question form retrieved data at 0.5 if any
                      get the questions to show user which kind of question we have and can answer as sample to inform user.
'''
    # end the graph if it is unsafe and set env var that app will fetch
    document_title = os.getenv("DOCUMENT_TITLE")
    # no need to make it JSON or Dict, we just will inject it in prompt at the right place
    ai_personality_trait = os.getenv("AI_PERSONALITY_TRAIT")

# Initialize states
workflow = StateGraph(MessagesState)

# nodes
workflow.add_node("error_handler", error_handler)
workflow.add_node("analyse_user_query_safety", analyse_user_query_safety)
workflow.add_node("summarize_user_to_clear_question", summarize_user_to_clear_question)
workflow.add_node("retrieve_answer")

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


# tool edges
workflow.add_edge("tool_api_choose_agent", "tool_agent_decide_which_api_node")
# edges
workflow.add_edge("tool_agent_decide_which_api_node", "find_documentation_online_agent")
workflow.add_edge("find_documentation_online_agent", "tool_search_node")
workflow.add_edge("tool_search_node", "documentation_writer")
workflow.add_conditional_edges(
  "documentation_writer",
  evaluate_doc_or_error
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
