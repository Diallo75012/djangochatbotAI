import os
import json
# for typing func parameters and outputs and states
from typing import Dict, List, Tuple, Any, Optional, Union
# structured output
from structured_output import (
  analyse_user_query_safety_schema,
  summarize_user_to_clear_question_schema,
  answer_to_user_schema,
  retrieve_answer_schema,
)
from json_dumps_manager import safe_json_dumps
from token_count_helper import token_counter
# prompts
from prompts import (
  analyse_user_query_safety_prompt,
  summarize_user_to_clear_question_prompt,
  retrieve_answer_prompt,
  answer_to_user_prompt,
  # only if needed custom answer prompt
  #answer_to_user_prompt_055,
  disclaimer,
)
# utils
import call_llm, prompt_creation, beautiful_graph_output
# Tools
from tools import (
  llm_with_retrieve_answer_tool_choice,
  tool_retrieve_answer_node,
)
# Retrieve Vector 
from retrieve_answer import retrieve_answer_action
# LLMs
from llms import (
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
load_dotenv(dotenv_path='../.env', override=False)
load_dotenv(dotenv_path="../.vars.env", override=True)

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
def analyse_user_query_safety(state: MessagesState):
  messages = state['messages']
  # this should be equal to os.getenv("USER_INITIAL_QUERY")
  last_message = messages[-1].content

  if last_message == os.getenv("USER_INITIAL_QUERY"):
    query = prompt_creation.prompt_creation(analyse_user_query_safety_prompt["human"], user_initial_query=last_message)
    print("query: ", query)
  else:
    return {"messages": [{"role": "ai", "content": json.dumps({"error": "User query to start graph different from environment variable set for user query."})}]}
  
  # get the answer as we want it using structured output schema directly injected in prompt
  try:
    decision = call_llm.call_llm(query, analyse_user_query_safety_prompt["system"]["template"], analyse_user_query_safety_schema, groq_llm_llama3_70b)
    if decision["safe"].lower() == "valid":
      return {"messages": [{"role": "ai", "content": json.dumps({"safe":"safe"})}]}
    return {"messages": [{"role": "ai", "content": json.dumps({"unsafe": "unsafe"})}]}
  except Exception as e:
    return {"messages": [{"role": "ai", "content": json.dumps({"error": f"An error occured while trying to analyze user input content: {e}"})}]}

# CONDITIONAL EDGE
def safe_or_not(state: MessagesState):
  messages = state['messages']
  last_message = json.loads(messages[-1].content)

  if "safe" in last_message:
    # go to question rephraser node
    return "summarize_user_to_clear_question"
  elif "unsafe" in last_message:
    # set env var for unsafe query and the Django view will take care of flagging user in the DB and creating log of that event for Devops/Security Team
    set_key(".var.env", "USER_QUERY_UNSAFE", "True")
    load_dotenv(dotenv_path=".vars.env", override=True)
    return END
  else:
    # it could be any other error, so we forward to error node
    return "error_handler"

# NODE
def summarize_user_to_clear_question(state: MessagesState):

  user_initial_query = os.getenv("USER_INITIAL_QUERY")
  query = prompt_creation.prompt_creation(summarize_user_to_clear_question_prompt["human"], user_initial_query=user_initial_query)

  # rephrase user intial query to a question
  try:
    clear_question = call_llm.call_llm(query, summarize_user_to_clear_question_prompt["system"]["template"], summarize_user_to_clear_question_schema, groq_llm_llama3_70b)
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
    #return "retrieve_answer_agent"
    return "retrieve_answer_action"
  return "error_handler"

# NODE
def retrieve_answer_agent(state: MessagesState):
  rephrased_user_query = os.getenv("REPHRASED_USER_QUERY")
  state_history = MessagesState()

  try:
    #response = tool_retrieve_answer_node.invoke(tool_schema)
    response = retrieve_answer_action(state_history)
    print("Retriever node response: ", response, type(response))
    # we return the response from the retriever which is already in the right format for state update
    return 
  except Exception as e:
    print(f"Error during tool node execution: {e}")
    return {"messages": [{"role": "ai", "content": json.dumps({"error": str(e)})}]}

  #return {"messages": [{"role": "ai", "content": json.dumps({"response": response})}]}

# CONDITIONAL EDGE
def retrieved_answer_or_not(state: MessagesState):
  '''
  Here we will capture the answer fromt he state which is success or error
  '''
  messages = state["messages"]
  print("Retrieved answer or not mssages: ", messages[-1].content)
  #last_message = json.loads(messages[-1].content[-1])
  last_message = json.loads(messages[-1].content)
  print("Last message in retrieved_answer_or_not: ", last_message, type(last_message))

  '''
  # first keys to check
  error_vector, answers, nothing
  # then for answers key
  top_n > 1
  'score_064_*'
  'score_055_*'
  top_n = 1
  'score_064'
  'score_055'
  '''
  if "error_vector" in last_message:
    return "error_handler"
  elif "nothing" in last_message:
    #ai_messages = AIMessage(content="nothing")
    state["messages"].append({"role": "ai", "content": "nothing"})
    return "answer_to_user"
  else:
    #ai_messages = AIMessage(content="answers")
    state["messages"].append({"role": "ai", "content": "answers"})
    return "answer_to_user"
      



# NODE
def answer_to_user(state: MessagesState):

  '''
    we check first the last message if equal to: answers or nothing
    Then we answer directly if nothing
    OR we need to fetch the answer from the previous message, so the `-2` message one.
  '''
  print("full state in answer to user: ", state)
  messages = state['messages']
  last_message = json.loads(messages[-1].content)
  print("Last message from answer to user: ", last_message, type(last_message))
  '''
    {"answers": {"score_063_1": "Tokyo for population density", "score_055_1": "what is the biggest capital city in Asia?"}}
  '''
  user_initial_query_rephrased = os.getenv("REPHRASED_USER_QUERY")
  
  ai_personality = "("
  ai_personality_traits = json.loads(os.getenv("AI_PERSONALITY_TRAITS"))
  print("ai_personality_traits: ", ai_personality_traits, type(ai_personality_traits))
  for k, v in ai_personality_traits.items():
    ai_personality += f"{k} is {v}, "
  ai_personality = ai_personality[:-1] + ")"
  print("Ai personality: ", ai_personality)
  
  query = prompt_creation.prompt_creation(answer_to_user_prompt["human"], user_initial_query_rephrased=user_initial_query_rephrased)
  answer_063 = ""
  question_055 = ""

  # inject ai_personality_traits in system prompt:
  answer_to_user_prompt_ai_personality_injected = answer_to_user_prompt["system"]["template"].format(ai_personality_traits=json.dumps(ai_personality), response_schema="{response_schema}", query="{query}")
  # if using customized prompt
  #answer_to_user_prompt_ai_personality_injected_055 = answer_to_user_prompt_055["system"]["template"].format(ai_personality_traits=json.dumps(ai_personality), response_schema="{response_schema}", query="{query}")
  #print("answer_to_user_prompt_ai_personality_injected_055: ", answer_to_user_prompt_ai_personality_injected_055)

  # FLOW ZERO ANSWER  
  if "nothing" in last_message:
    # answer accordingly! using AI or not

    disclaimer_nothing = disclaimer["nothing"].format(user_initial_question=user_initial_query_rephrased)
    # get schema and inject variables in schema
    schema_if_nothing = answer_to_user_schema["answer_if_nothing"]["response"].format(disclaimer=disclaimer_nothing)
    # call llm and then stop graph returning final answer to user
    try:
      final_answer_nothing = call_llm.call_llm(query, answer_to_user_prompt_ai_personality_injected, schema_if_nothing, groq_llm_llama3_70b)
      # get the 'response' from the schema
      response_nothing = final_answer_nothing["response"]
      return {"messages": [{"role": "ai", "content": json.dumps({"response_nothing": response_nothing})}]}
    except Exception as e:
      return {"messages": [{"role": "ai", "content": json.dumps({"error_response_nothing": e})}]}    

  # FLOW ANSWERS VALID OR PARTIAL EXAMPLES
  elif "answers" in last_message:
    answers_dict_of_dict = last_message
    print("Answers Dict of Dict in Answer_to_user node: ", answers_dict_of_dict)

    # now just check if answer come from the higher score band or the lower one to tailor the answer type
    # we loop through and check those keys: get all answers
    for k, v in answers_dict_of_dict["answers"].items():
      # this is our valid answers flow
      if "063" in k:
        # get answer
        answer_063 = answer_063 + v + ". "
      # this is our mitigated answer flow
      # we will just advice user by saying not found but we have this kind of questions answers 
      # and then show sample of those questions from retrieval result score 055
      elif "055" in k:
        # get answer
        question_055 = question_055 + v + ". "

    # FLOW ANSWERING USER WITH ANSWER FOUND: VALID
    # we want to send good answers if we have some in priority, if there is none, next conditional will be triggered
    # as we could have both 063 and 055 but if tehre is 063 we ignore here 055 and just answer with good answers
    # 055 is just a backup answer
    if answer_063 != "":
      print("answer_063: ", answer_063)
      disclaimer_answer_found_but_disclaim_accuracy = disclaimer["answer_found_but_disclaim_accuracy"].format(
        user_initial_question=user_initial_query_rephrased,
        answer_found_in_vector_db=answer_063,
      )
      schema_if_063 = answer_to_user_schema["answer_if_063"]["response"].format(
        answer_with_disclaimer=disclaimer_answer_found_but_disclaim_accuracy
      )
      try:
        final_answer_063 = call_llm.call_llm(query, answer_to_user_prompt_ai_personality_injected, schema_if_063, groq_llm_llama3_70b)
        print("final answer 063: ", final_answer_063)
        # get the 'response' from the schema
        # why ? i don't know but there is sometimes a key in response `text` so dict in dict and we need to extract it.
        if isinstance(final_answer_063.get("response"), dict) and "text" in final_answer_063["response"]:
          response_063 = final_answer_063["response"]["text"]
          return {"messages": [{"role": "ai", "content": json.dumps({"response": response_063})}]}
        else:
          response_063 = final_answer_063["response"]
          return {"messages": [{"role": "ai", "content": json.dumps({"response": response_063})}]}
      except Exception as e:
        return {"messages": [{"role": "ai", "content": json.dumps({"error": e})}]}

    # FLOW WITH SIMILAR QUESTION BUT NO ANSWER FOUND
    if question_055 != "" and answer_063 == "":
      print("question_055: ", question_055)
      disclaimer_only_this_type_of_questions_example_show_to_user = disclaimer["example_of_questions_having_answers"].format(
        user_initial_question=user_initial_query_rephrased,
        type_of_questions_example_show_to_user=question_055,
      )
      schema_if_055 = answer_to_user_schema["answer_if_055"]["response"].format(
        disclaimer=disclaimer_only_this_type_of_questions_example_show_to_user
      )
      try:
        final_answer_055 = call_llm.call_llm(query, answer_to_user_prompt_ai_personality_injected, schema_if_055, groq_llm_llama3_70b)
        # get the 'response' from the schema
        if isinstance(final_answer_055.get("response"), dict) and "text" in final_answer_055["response"]:
          response_055 = final_answer_055["response"]["text"]
          return {"messages": [{"role": "ai", "content": json.dumps({"response": response_055})}]}
        else:
          response_055 = final_answer_055["response"]
          return {"messages": [{"role": "ai", "content": json.dumps({"response": response_055})}]}
      except Exception as e:
        return {"messages": [{"role": "ai", "content": json.dumps({"error": e})}]} 

# error handling
def error_handler(state: MessagesState):
  messages = state['messages']
  
  # Log the graph errors in a file
  with open("../logs/retrieval_graph_logs.log", "a", encoding="utf-8") as conditional:
      json_error_message = messages[-1].content
      conditional.write(f"\n\n{json_error_message}\n\n")
  '''
    # we return in the state the message that is already in json.dumps form so that we can json.load in the views.py side
    # where we are going to filter to see what kind of error has been returned,
    # we might need to have a thread running for the graph running environment
    # all error types returned by graph: "error", "error_vector", "error_reponse_nothing", "error_reponse_063", "error_reponse_055"
  '''
  
  return {"messages": [{"role": "ai", "content": messages[-1].content}]}

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
                     Then provide retrieved question form retrieved data at 0.5 if any
                     get the questions to show user which kind of question we have and can answer as sample to inform user.
'''

# Initialize states
workflow = StateGraph(MessagesState)

# nodes
workflow.add_node("error_handler", error_handler)
workflow.add_node("analyse_user_query_safety", analyse_user_query_safety)
workflow.add_node("summarize_user_to_clear_question", summarize_user_to_clear_question)
# workflow.add_node("retrieve_answer_agent", retrieve_answer_agent)
workflow.add_node("retrieve_answer_action", retrieve_answer_action)
workflow.add_node("answer_to_user", answer_to_user)

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
workflow.add_conditional_edges(
  #"retrieve_answer_agent",
  "retrieve_answer_action",
  retrieved_answer_or_not
)

# end
workflow.add_edge("error_handler", END)
workflow.add_edge("answer_to_user", END)

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
def retrieval_agent_team(user_query):
  print("Retrieval Agents AI Team Startooooooo !!!")
  print(f"Query: '{user_query}'")
  final_output = None

  count = 0
  for step in user_query_processing_stage.stream(
    {"messages": [SystemMessage(content=user_query)]},
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
      except TypeError:
        final_output = safe_json_dumps(step)

  # subgraph drawing
  graph_image = user_query_processing_stage.get_graph().draw_png()
  with open("retrieval_agent_team.png", "wb") as f:
    f.write(graph_image)

  # Ensure final_output is JSON formatted for downstream consumption
  if isinstance(final_output, str):
    try:
      # Ensure valid JSON; if not, wrap in a standard error message
      json.loads(final_output)
    except json.JSONDecodeError:
      final_output = json.dumps({"error": "Invalid final output format"})

  return final_output



if __name__ == '__main__':
  import json
  load_dotenv()
  user_query = os.getenv("USER_INITIAL_QUERY")
  retrieval_agent_team(user_query)

