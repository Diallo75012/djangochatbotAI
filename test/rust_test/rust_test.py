import os
import json
from dotenv import load_dotenv

from rust_lib import (
  call_llm_api, # OK! From previous tests
  load_personality, # OK!
  delete_collection_py, # OK!
  load_env_variable_py, # OK!
  string_to_dict_py, # OK1
  collection_normalize_name_py, # OK!
  token_counter_py, # OK!
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
'''

'''
# load_env_variable_py: just a like a `os.getenv()` using rust's `dotenv` under the hood
# file path need to be pointing to the django root folder (../../<this kind of path> or absolute path as well)
env_file_absolute_path = "/home/creditizens/djangochatAI/chatbotAI/.vars.env"
env_file_dotted_path = "../../.vars.env"
env_var = "DOCUMENT_TITLE"

try:
  document_title = load_env_variable_py(env_file_absolute_path, env_var)
  print("doc title 1: ", document_title)
except Exception as e:
  print("doc title error: ", e)

try:
  document_title2 = load_env_variable_py(env_file_dotted_path, env_var)
  print("doc title 2: ", document_title2)
except Exception as e:
  print("doc title2 error: ", e)

# returns
Environment variables loaded from: "/home/creditizens/djangochatAI/chatbotAI/.vars.env"
doc title 1:  purikura-photo-booths-in-japan
Environment variables loaded from: "/home/creditizens/djangochatAI/chatbotAI/test/rust_test/../../.vars.env"
doc title 2:  purikura-photo-booths-in-japan
'''

'''
# string_to_dict_py
# this will work as we have single quote `''` surrounding double quotes `""` btu won't work the other way around
dict = '{"country": "Japan", "Wind": "Kamikaze"}' # works
# dict = "{'country': 'Japan', 'Wind': 'Kamikaze'}" # won't work

# better just use json dumps like here
dict2 = json.dumps({'country': 'Metaverse-Japan', 'City':'Kamakura'})

try:
  formatted_to_dict = string_to_dict_py(dict)
  print("formatted_to_dict: ", formatted_to_dict)
except Exception as e:
  print("error formatted dict1 string dict: ", e)

try:
  formatted_to_dict2 = string_to_dict_py(dict2)
  print("formatted_to_dict2: ", formatted_to_dict2)
except Exception as e:
  print("error formatted dict1 string dict: ", e)
'''


'''
# collection_normalize_name_py
collection_name = "Shibuya 109 Tower Shopping Center"
try:
  formatted_collection_name = collection_normalize_name_py(collection_name)
  print("Formatted collection name: ", formatted_collection_name)
except Eception as e:
  print("Error formatting collection name: ", e)
'''


'''
# token_counter_py
prompt_completion_string = """
overing the Warmth of Japan's Manga and Internet Cafe Culture
執筆者: Hideo Takahashi

|

2024年11月11日

|

読む時間 5 min

In the hustle and bustle of Japan's urban landscape, there's a unique sanctuary that stands out for lovers of comics, digital entertainment, and warm hospitality. Welcome to the world of 日本の漫画喫茶・ネットカフェ (Manga Kissa and Net Café culture). These spots aren’t just about escapism; they reflect the country's rich culture intertwined with the love for storytelling and technology.

The Rise of Manga Kissa and Net Cafes in Japan
Manga Kissa, or manga cafes, began in the late 1970s, evolving from simple places to read comics into comprehensive entertainment hubs. Net cafes joined the scene in the mid-1990s, offering internet access before it was commonplace in homes. Today, these cafes serve as both a cultural staple and a refuge for enthusiasts.
A Blend of Tradition and Technology
Manga cafes originally provided visitors with a library of manga to read. Over time, the fusion with Internet cafes turned these locations into multimedia centers. In a Manga Kissa, you can not only read comics but also enjoy internet browsing, gaming, and sometimes even movies.
The Cultural Significance
These cafes are more than venues; they hold cultural significance. For many, they are a retreat from the fast-paced life outside. They embody the Japanese values of hospitality and convenience, offering cozy environments where patrons can relax and recharge.
The Role in Urban Life
In crowded cities like Tokyo, where space is a luxury, Manga Kissa and Net Cafes provide an affordable alternative to hotels. They offer overnight stays with amenities, making them ideal for travelers on a budget or those who miss the last train home.
Exploring the Offerings of Manga and Net Cafes
The diverse offerings of these cafes cater to a wide audience, from readers and gamers to tourists looking for a unique experience. Let's go deeper into what makes these places so special.
A Haven for Manga Lovers
With walls lined with manga, these cafes allow patrons to immerse themselves in their favorite series. Some boast collections of thousands of titles, ensuring there’s something for every reader. The calm ambiance enhances the reading experience, making it the perfect escape for manga enthusiasts.
"""
try:
  token_count = token_counter_py(prompt_completion_string)
  print("Token Count Manga Kissa: ", token_count)
except Exception as e:
  print("error occured while trying to count token of manag kissa..: ", e)

# returned
Outputs: 491
- Tested using GPT4o&40-mini Openai Tokenizer(https://platform.openai.com/tokenizer) and got:
TOkens: 474, Characters: 2297


Very close i just use the base tokenizer so it is fine!
'''
