import os
import ast
from dotenv import load_dotenv
from typing import Dict, List, Tuple, Any, Optional


# load env vars
load_dotenv(dotenv_path='.env', override=False)
load_dotenv(dotenv_path=".vars.env", override=True)

# function needed to get the STR dict representation returned by the query analyzer and be able to fetch values as a dict
# this help us to store in env vars a dictionary and here it will be converted to dict as env vars have `'<env var>'` str format
def string_to_dict(string: str) -> Dict[str, Any]:
  """
  Converts a string representation of a dictionary to an actual dictionary.

  Args:
  string (str): The string representation of a dictionary.

  Returns:
  Dict[str, Any]: The corresponding dictionary.
  """
  final_dict_key_lowercase = {}
  try:
    # Safely evaluate the string as a Python expression
    dictionary = ast.literal_eval(string)
    if isinstance(dictionary, dict):
      for k, v in dictionary.items():
        final_dict_key_lowercase[k.lower()] = v
        return final_dict_key_lowercase
      else:
        raise ValueError("The provided string does not represent a dictionary.")
  except (SyntaxError, ValueError) as e:
    raise ValueError(f"Error converting string to dictionary: {e}")

def personality_trait_formatting(trait_dict) -> dict:
  """
    This function will be return a dict with all fields of AI personality filled
    Here we check that fields are not empty, if those are we will provide defautl value
    an environment variable need to be set with default values: AI_PERSONALITY_DEFAULT

    Those are the fields of the AI Personamlity:
    ai_traits_dict = {
      "chatbot_name": chatbot_name,
      "chatbot_description": chatbot_description,
      "chatbot_age": chatbot_age,
      "chatbot_origin": chatbot_origin,
      "chatbot_dream": chatbot_dream,
      "chatbot_tone": chatbot_tone,
      "chatbot_expertise": chatbot_expertise,
    }
  """
  ai_personality_env_var = os.getenv("DEFAULT_AI_PERSONALITY_TRAIT")
  ai_personality_default = string_to_dict(ai_personality_env_var)
  # we made sure to have same key names for dafault and custom clintuser/businessuser defined AI personality trait
  for k, v in trait_dict.items():
    # we check if value is empty, so not set by clientuser/businessuser
    if v == "":
      # we update that the value of that empty field with default value that we have set in env vars
      trait_dict[k] = ai_personality_default[k]

  # `trait_dict` exists this function being sure to have all fields filled
  return trait_dict











