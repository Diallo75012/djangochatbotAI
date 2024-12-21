import tiktoken
from rust_lib import token_counter_py


def token_counter(text_or_string_prompt):
  try:
    num_of_tokens = token_counter_py(text_or_string_prompt) # rust counterpart function called
    print("Num of tokens: ", num_of_tokens)
    return num_of_tokens
  execpt Exception as e:
    print("An error occured while trying to count tokens from rust helper: ", e)
    return f"An error occured while trying to count tokens from rust helper: {e} "


'''
# rust counterpart will replace it  
def token_counter(text_or_string_prompt):

  # Define a custom encoding (you need to provide vocabulary or rules)
  custom_encoding = tiktoken.get_encoding("cl100k_base")  # Use a base encoding scheme

  num_of_tokens = len(custom_encoding.encode(text_or_string_prompt))
  return num_of_tokens
'''
