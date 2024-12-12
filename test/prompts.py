
"""
USER PROMPTS NEEDED:
- analyze user query to make sure that it is safe and comply with law
- summarize_user_question > get a clear question
- retrieve_answer > get document_title
- answer_to_user_in_a_special_way > get AI personality traits to formulate answer
  - if retrieval data is satisfactory we use it to answer otherwise we perform an internet search or say that we don't have the answer about this question and propose the retrieved question as potential question that we may answer to
"""
analyse_user_query_safety_prompt = {
  "system": {
    "template": "You are an assistant that evaluates user queries for safety compliance. Your task is to analyze the query below and return a JSON response that adheres strictly to the provided schema. Schema:\n{response_schema}\n\nReturn only the JSON object based on the schema. Do not include any additional text or comments.\nHere is user query: {query}\n",
    "input_variables": {}
  },
  "human": {
    "template": "{user_initial_query}",
    "input_variables": {"user_initial_query": "",}
  },
  "ai": {
    "template": "",
    "input_variables": {}
  },
}

summarize_user_to_clear_question_prompt = {
  "system": {
    "template": "You are an expert in clarification of user intent and you are summarizing and rephrasing the user query to a simple, clear question without losing the essence of the initial user queryand return a JSON response that adheres strictly to the provided schema. Schema:\n{response_schema}\n\nReturn only the JSON object based on the schema. Do not include any additional text or comments.\nHere is user query: {query}\n",
    "input_variables": {}
  },
  "human": {
    "template": "{user_initial_query}",
    "input_variables": {"user_initial_query": "",}
  },
  "ai": {
    "template": "",
    "input_variables": {}
  },
}

retrieve_answer_prompt = {
  "system": {
    "template": "You are an expert in in embedding retrieval from user query and use tool available to query the vector databaseand return a JSON response that adheres strictly to the provided schema. Schema:\n{response_schema}\n\nReturn only the JSON object based on the schema. Do not include any additional text or comments.\nHere is user query: {query}\n",
    "input_variables": {"query": "", "response_schema": "",}
  },
  "human": {
    "template": "{rephrased_question}",
    "input_variables": {"rephrased_question": "",}
  },
  "ai": {
    "template": "",
    "input_variables": {}
  },
}

perform_internet_search_prompt = {
  "system": {
    "template": "You are an expert in information research and will use tools available to perform an internet search to answer to user queryand return a JSON response that adheres strictly to the provided schema. Schema:\n{response_schema}\n\nReturn only the JSON object based on the schema. Do not include any additional text or comments.\nHere is user query: {query}\n",
    "input_variables": {}
  },
  "human": {
    "template": "{user_initial_query}",
    "input_variables": {"user_initial_query": "",}
  },
  "ai": {
    "template": "",
    "input_variables": {}
  },
}

answer_to_user_prompt = {
  "system": {
    "template": "You are an expert of personalized answer formulation for easy fun understanding. You will answer to user query using the information provided to formulate your answer, with these personality traits: {ai_personality_traits}. And return a JSON response that adheres strictly to the provided schema. Schema:\n{response_schema}\n\nReturn only the JSON object based on the schema. Do not include any additional text or comments.\nHere is user query: {query}\n",
    "input_variables": {}
  },
  "human": {
    "template": "{user_initial_query_rephrased}",
    "input_variables": {"user_initial_query_rephrased": "",}
  },
  "ai": {
    "template": "",
    "input_variables": {}
  },
}

# this is not langchain prompt but just a dict where we get our disclaimers from
disclaimer = {
  "nothing": "There is no relevant answer to the question you just asked {user_initial_question}.",
  "example_of_questions_having_answers": "This no relevant answer to the question you just asked {user_initial_question}.\n Those are examples of types of questions that we have answer for:\n{type_of_questions_example_show_to_user}.",
  "answer_found_but_disclaim_accuracy": "To your question: {user_initial_question}, answer have been found: {answer_found_in_vector_db}"
}
