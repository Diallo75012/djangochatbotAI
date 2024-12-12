import os
import json
# for typing func parameters and outputs and states
from typing import Dict, List, Tuple, Any, Optional
# For str to dict
import ast
import re

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
        print("string: ", eprint(string))
        print("string: ", string)
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

