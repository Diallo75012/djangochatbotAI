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


# this will normalize the collection names to have those lowercases and no space in between words but a dash `"-"`
def collection_normalize_name(collection_name: str):
  return collection_name.replace(" ", "-").strip().lower()

