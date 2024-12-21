import os
import json
from dotenv import load_dotenv

from rust_lib import (
  call_llm_api,
  load_personality, # OK!
  delete_collection_py, # OK!
  load_env_variable_py,
  string_to_dict_py,
  collection_normalize_name_py,
  token_counter_py,
)


load_dotenv(dotenv_path='../../.env', override=False)
load_dotenv(dotenv_path="../../.vars", override=True)

'''
 STEPS:
 - check where the function is called in the code
 - check types and if the code is doing what is intented to do
 - debug, debug, debug, them, replace the python function helper
'''

'''
# load_personality
ai_traits_dict = {
  "chatbot_name": "",
  "chatbot_description": "nice test chatbot",
  "chatbot_age": "",
  "chatbot_origin": "Tokyo",
  "chatbot_dream": "",
  "chatbot_tone": "",
  "chatbot_expertise": "",
}
print("ai traits dict: ", ai_traits_dict, type(ai_traits_dict))
json_ai_traits = json.dumps(ai_traits_dict)
print("json_ai_traits: ", json_ai_traits, type(json_ai_traits))

ai_personality_traits = load_personality(json_ai_traits)
print("AI PERsonality traits: ", ai_personality_traits, type(ai_personality_traits))
'''


# delete_collection
# here need to start server use UI to create business data,
# therefore, run ollama, and after embedding is done like just one or two,
# come here to see if this deletes the collection and embeddings
driver=os.getenv("DRIVER")
host=os.getenv("DBHOST")
port=int(os.getenv("DBPORT"))
database=os.getenv("DBNAME")
user=os.getenv("DBUSER")
password=os.getenv("DBPASSWORD")
CONNECTION_STRING = f"postgresql+{driver}://{user}:{password}@{host}:{port}/{database}"
print("DB HOST just tocheck if env vars are pulled: ", host)


business_collection_name = "rust-test"

try:
  delete_collection = delete_collection_py(CONNECTION_STRING, business_collection_name)
  print("Delete collection: ", delete_collection)
except Exception as e:
  print("Error while calling trying to delete collection: ", e)
