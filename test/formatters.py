import json
from typing import Dict, Any
# For str to dict
import ast
# this to print to stderr
import sys


def eprint(*args, **kwargs):
  print(*args, file=sys.stderr, **kwargs)

# function needed to get the STR dict representation returned by the query analyzer and be able to fetch values as a dict
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
    print("string: ", string, type(string))
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

string = '```json { "safe": true, "unsafe": false}```'
if "```json" in string:
  print(" '```json' in response")
  # parse response and clean it to limit errors of not valid json error when transforming to dictionary
  response_parsed = string.split("```")[1].strip("json").strip().replace("`", "")

  # 1. Replace escaped underscores first to avoid double-replacing backslashes.
  #response_parsed = response_parsed.replace("\\_", "_")
  #print("Parsed response underscores: ", response_parsed)
  # 2. Normalize multiple newlines into single ones.
  #response_parsed = response_parsed.replace("\n\n", "\n")
  #print("Parsed response double line return: ", response_parsed)
  # 3. Escape single newlines for JSON representation (this ensures newlines are preserved as literal `\n`).
  #response_parsed = response_parsed.replace("\n", "\\n")
  #print("Parsed response escape slash of line return: ", response_parsed)
  # 4. Finally, escape backslashes. This is done last to ensure we don't affect earlier replacements.
  #response_parsed = response_parsed.replace("\\", "\\\\")
  #print("Parsed response replace double backslashes: ", response_parsed)
  response_parsed = string_to_dict(json.dumps(response_parsed))
  print("response parsed is dict or not: ", type(response_parsed), response_parsed)

elif "```markdown" in string:
    print(" '```markdown' in response")
    # parse response and clean it to limit errors of not valid json error when transforming to dictionary
    response_parsed = string.split("```")[1].strip("markdown").strip().replace("`", "")
    response_parsed = response_parsed.replace("\\_", "_")
    print("Parsed response underscores: ", response_parsed)  

else:
  print(" '```' in not response")
  if "```python" in string:
    print(" '```python' in response")
    # parse response and clean it to limit errors of not valid json error when transforming to dictionary
    response_parsed = string.split("```")[1].strip("python").strip().replace("`", "")
    response_parsed = response_parsed.replace("\\_", "_")
    print("Parsed response underscores: ", response_parsed)
  else:
    response_parsed = string
    print("response parse raw no transformation (no json/python/markdown): ", response_parsed)


