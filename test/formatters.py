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
  try:
    # Directly use JSON parsing
    dictionary = json.loads(string)
    print("dictionary converted: ", dictionary)
    return {k.lower(): v for k, v in dictionary.items()}
  except json.JSONDecodeError as e:
    raise ValueError(f"Error converting string to dictionary: {e}")

"""
string = '{"safe": "valid", "unsafe": "invalid"}'
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

print("RESPONSE PARSED RAW (no stirng to dict): ", response_parsed)
string_to_dict_response = string_to_dict(response_parsed)
print("RESPONSE PARSED string_to_dict: ", string_to_dict_response, type(string_to_dict_response))

"""








