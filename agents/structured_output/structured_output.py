"""
  Here we will list all the different schema for structured output
  using the `in-prompt`(desired structured output injection in prompts) technique.
"""
schema_example={
  "requirements": "A requirements.txt content corresponding to new Python script only if needed. Or a correction of the previous requirements.txt if error comes from it. answer just a str as it should be on the requirements.txt file, if there is more than one line make sure to format the str with \\n to return at the next line for next required package to install.",
  "script": "New Python script that addresses the error or the previous script if the error wasn't coming from the code but from the requirements.txt content. Make sure it is well formatted, with good indentation and line returns. use str to answer.",
  "needed": "Answer 'YES' or 'NO' depending on if the code requires a requirements.txt file."
}

analyse_user_query_safety_schema = {
  "safe": "can only take the value 'true' or 'false'. set to 'true' if the user query is considered as being safe."
  "unsafe": "can only take the value 'true' or 'false'. set to 'false' if the user query is considered as being unsafe."
}

summarize_user_to_clear_question_schema = {
  "question": "user question is rephrased to a clear question and only one question."
}
