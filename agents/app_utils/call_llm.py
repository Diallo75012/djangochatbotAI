import os
import json
# for typing func parameters and outputs and states
from typing import Dict, List, Tuple, Any, Optional
# for llm call with func or tool and prompts formatting
from langchain_groq import ChatGroq
from langchain_core.messages import (
  AIMessage,
  HumanMessage,
  SystemMessage,
  ToolMessage
)
from langchain.prompts import (
  PromptTemplate,
  ChatPromptTemplate,
  SystemMessagePromptTemplate,
  HumanMessagePromptTemplate,
  AIMessagePromptTemplate
)
# replaced by rust countrerpart `string_to_dict_py`
#from agents.app_utils.formatters import string_to_dict
from rust_lib import string_to_dict_py
# to run next graphs
from agents.llms.llms import (
  groq_llm_mixtral_7b,
  groq_llm_llama3_8b,
  groq_llm_llama3_70b,
  groq_llm_llama3_70b_versatile,
  groq_llm_gemma_7b,
)
# for env. vars
from dotenv import load_dotenv, set_key


# load env vars
load_dotenv(dotenv_path='.env', override=False)
load_dotenv(dotenv_path=".vars", override=True)

# creation of prompts
def prompt_creation(target_prompt_human_system_or_ai: Dict[str, Any], **kwargs: Any) -> str: #-> PromptTemplate:
    """
      formatitng a prompt using two parts: the base of the prompt with the expected input variables
      and the kwargs to which are input variables to inject in the prompt
    """
    input_variables = target_prompt_human_system_or_ai.get("input_variables", [])

    prompt = PromptTemplate(
        template=target_prompt_human_system_or_ai["template"],
        input_variables=input_variables
    )

    formatted_template = prompt.format(**kwargs) if input_variables else target_prompt_human_system_or_ai["template"]
    print("formatted_template: ", formatted_template)
    return formatted_template
    #return PromptTemplate(
    #    template=formatted_template,
    #    input_variables=[]
    #)

def call_llm(query: str, prompt_template_part: str, schema: str, llm: ChatGroq, partial_variables={}) -> Dict:


  prompt = PromptTemplate(
    template=prompt_template_part,
    input_variables=["query", "response_schema"],
    # this has to be a dict
    partial_variables=partial_variables,
  )
  print("Prompt before call structured output: ", prompt)

  # And a query intended to prompt a language model to populate the data structure. groq_llm_llama3_70b as many code sent so long context
  try:
    prompt_and_model = prompt | groq_llm_mixtral_7b
    response = prompt_and_model.invoke({"query": query, "response_schema": schema})
    print("RESPONSE: ", response.content)
    # parse content from dict
    if "```markdown" in response.content:
      print(" '```markdown' in response")
      # parse response and clean it to limit errors of not valid json error when transforming to dictionary
      response_parsed = response.content.split("```")[1].strip("markdown").strip().replace("`", "")

      # 1. Replace escaped underscores first to avoid double-replacing backslashes.
      response_parsed = response_parsed.replace("\\_", "_")
      print("Parsed response underscores: ", response_parsed)

    else:
      if "```python" in response.content:
        print(" '```python' in response")
        # parse response and clean it to limit errors of not valid json error when transforming to dictionary
        response_parsed = response.content.split("```")[1].strip("python").strip().replace("`", "")
        response_parsed = response_parsed.replace("\\_", "_")
        print("Parsed response underscores: ", response_parsed)
      elif "```json" in response.content:
        print(" '```json' in response")
        # parse response and clean it to limit errors of not valid json error when transforming to dictionary
        response_parsed = response.content.split("```")[1].strip("json").strip().replace("`", "")
        response_parsed = response_parsed.replace("\\_", "_")
        print("Parsed response underscores: ", response_parsed)
      else:
        print(" '```' not in response")
        response_parsed = response.content
    # transform to dict
    # replaced by rust counterpart string_to_dict_py
    # response_content_to_dict = string_to_dict(response_parsed)
    response_content_to_dict = string_to_dict_py(response_parsed) #using rust coutnerpart string_to_dict_py
    print("Response content dict: ", response_content_to_dict)
    return response_content_to_dict

  except Exception as e:
    raise Exception(f"An error occured while calling llm: {str(e)}")
