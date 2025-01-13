import tiktoken

def token_counter(text_or_string_prompt):

  # Define a custom encoding (you need to provide vocabulary or rules)
  custom_encoding = tiktoken.get_encoding("cl100k_base")  # Use a base encoding scheme

  num_of_tokens = len(custom_encoding.encode(text_or_string_prompt))
  return num_of_tokens
