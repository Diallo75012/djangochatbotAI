# install python3.12
```bash
sudo apt install software-properties-common -y
sudo add-apt-repository ppa:deadsnakes/ppa -y
sudo apt update -y
sudo apt install python3.12 -y
# pip installation
sudo apt install curl -y
sudo apt install python3-pip
curl -sS https://bootstrap.pypa.io/get-pip.py | python3.12
```
# create alternatives to switch to using python3.12
sudo cp /usr/bin/python3.12 /usr/local/bin/python3.12
sudo update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.10 1
sudo update-alternatives --install /usr/bin/python3 python3 /usr/local/bin/python3.12 2
# now check that the `*` (star) is in front of `python3.12` or make it move the python version you want to use but should be fine
sudo update-alternatives --config python3
# then make this fix
## check with the command the file name for next command to be used to create a simlink
ls /usr/lib/python3/dist-packages/apt_pkg*.so
/usr/lib/python3/dist-packages/apt_pkg.cpython-310-x86_64-linux-gnu.so
# now cd to the folder and use the filename to create the simlink
cd /usr/lib/python3/dist-packages/
sudo ln -s apt_pkg.cpython-310-x86_64-linux-gnu.so apt_pkg.so
## then update and reinstall python3-apt
sudo apt-get update
sudo apt-get install --reinstall python3-apt
sudo apt update

# install venv for python3.12
sudo apt install python3.12-venv

### **But be careful with Ubuntu22 Python3.10 is installed by default so don't change it and prefer creating the virtual environment using `python3.12 -m venv <name_of_env>` | otherwise the terminal might not open when rebooting computer, if issue happen use: `ctrl + alt + f3` to have access to headless terminal and do the correct changes then reboot**


# postgresql installation
# we purge to have a fresh install
sudo apt purge postgresql* -y
sudo apt autoremove --purge -y
sudo rm -rf /etc/postgresql /var/lib/postgresql /var/log/postgresql
# remove any repo
sudo rm -f /etc/apt/sources.list.d/pgdg.list
# add the repo
echo "deb [arch=amd64] http://apt.postgresql.org/pub/repos/apt $(lsb_release -cs)-pgdg main" | sudo tee /etc/apt/sources.list.d/pgdg.list
# import repo
wget -qO - https://www.postgresql.org/media/keys/ACCC4CF8.asc | sudo apt-key add -
# update
sudo apt update
# install postgresql 17
sudo apt install postgresql-17 postgresql-contrib -y
# check
psql --version
# enable it
sudo systemctl start postgresql
sudo systemctl enable postgresql

# Restart virtuenv and install psycopg2
## make sure that you put the python version when installing `python3.x-dev` like `python3.12-dev`
sudo apt install -y build-essential python3.12-dev libpq-dev
pip install psycopg2-binary
pip install psycopg2

# install django rest framework
pip install djangorestframework
pip install markdown
pip install django-filter


# run tests
```bash
# install
pip install pytest pytest-django coverage
```
```bash
coverage run --source='.' -m pytest --ds=chatbotAI.settings
# then get the report either ways
coverage report
coverage html
```

# Next
**Finish the unit tests and maque sure to have an 80% coverage**
Total Estimated Test Functions to Add or Update:
- Views: 8-12 new tests.
- URLs: 2-3 new tests.
- Forms: 2-3 additional tests.
- Mixins: 2-3 additional tests.
- Template Tags: 1-2 new tests.
- Models: 1-2 additional tests.


# Github Action
if you dan't want to run CI at every push just add this to your commit message:
- **`[skip ci]` or `[ci skip]`**

# curl notes

- GET and POST (Option `-X`)
```bash
# Option `-X` for `--request`
curl -X GET URL
curl -X POST URL
```
- header in URL
```bash
-H header_key: header_value
```
- json data in URL.
```bash
# `-d` for data
-d json format data.
```
- Option to check the response in terminal
```bash
-v
```
- Example of command
```bash
curl -v -X POST https://<your_url> -H "Content-Type: application/json" -H "Authorization: bearer junkotokenshibuyamangakissafdkjfjdre" -d '{"identifier": "value", "events": "value", "use case": "value"}' 
```
- `?` at the end of URL
```bash
# here to have query parameter that limits results to `7` for example
curl -X GET YOU_URL/?limit=7
```

# diagram v1: Higher level view
[Diagram V1: high level view of app](https://excalidraw.com/#json=13cims8czPh4dJf0H06YF,avcPyjTq6wk_9r3-E0tu1Q)

# Next
- we won't use REACT but just Full Django HTML/JS/CSS/JINJA and chatgpt for improvements of UI with screenshots after having done boilerplate
- therefore we are going to use django routes normal ones for forms and everything and if needed to show data easily we can use the DjangoRestFramework ViewSets just to show the data from database to user

# Prometheus Python Client
- [Documentation Prometheus Python](https://prometheus.github.io/client_python/)

# render image from database using Jinja
```python
{% for img in your_object %}
    <img src="{{ img.image.url }}" >
{% endfor %}
```

# ForeignKey 
**on_delete options**
- CASCADE
- PROTECT
- SET_NULL
- SET_DEFAULT
- SET()
- DO_NOTHING

# Memcache for question answers instead of redis
- install memcached on ubuntu
```bash
sudo apt update
sudo apt install memcached
# systemctl start
sudo systemctl start memcached
# manual start 
memcached -d -m 64 -l 127.0.0.1 -p 11211
-d:		Run as a daemon.
-m 64:		Use 64MB of memory.
-l 127.0.0.1:	Listen only on localhost.
-p 11211:	Use port 11211 (default Memcached port).
```
- source: https://medium.com/@netfluff/memcached-for-django-ecedcb74a06d
```python
# python client to interact with memcached server
pip install python-memcached
```

# settings.pyCACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
        'LOCATION': '127.0.0.1:11211',
    }
}

# views.py

from django.core.cache import cachedef my_view(request):
    cache_key = 'my_unique_key' # needs to be unique (uuid probably)
    cache_time = 86400 # time in seconds for cache to be valid
    data = cache.get(cache_key) # returns None if no key-value pair    if not data:
        my_service = Service()
        data = service.get_data()
    
    cache.set(cache_key, data, cache_time)return JsonResponse(data, safe=False)```


# django foreinkey access to other model fields
- `.select_related()`: use .select_related('chat_bot') for example to get access to all fields in the view.py
- `__`: use .values('chat_bot__name') for example to access one specific field
- `jinj`: use dot notation if using `.select_related()` method or directly here `chat_bot__name`


# Next
-[x] make the user client routes, templates, forms, views, models..
-[x] fix issue with picture upload and see if is saved at location, then test deletion and see if function override works and actually delete the file and also make the field picture upload unique
-[x] prepare user using the diagram to know how UI would look like and make logic for User Client/Buisiness Registration
-[not for mvp no need] Have a set of numbers in a list that is like a number representing the business legal registration number, 
  , we could have also a system here that uses governmental API to check if business exist and other flags,
  here we are just making it simple to simulate only verified businesses registration allowed.
- [not for mvp no need do not overcomplicate]Add this number to business model as field that cannot change and will be used also in the bot model so add a field to get that number set for the chatbot getting it from the business user field.

# Django use of Lazy reference instead of import models from apps to other apps
instead of using `import` in the top of the top of the page we can use lazy referencing.
like:
```python
...
    chat_bot = models.OneToOneField(
        'chatbotsettings.ChatBotSettings',  # Lazy reference
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
...
``` 

This is more flexible as it prevent to get the circular import error.

# decision about chat
- there will be a sidebar with ChatBot Details
- we will use python-memcached or django session to save messages
- use javascript to have the webui keep the sate of the messages even if user reloads page or goes in another page and comes back
- clear everything when user logout
- use TTL is using cache (1h): it is for workplace so just asking to get answer from business knowledge and then use that information to continue working so after 1hour it can be deleted from cache

# Notes:
I have pivoted a bit my idea in how the user will be able to select chatbots:
- user will be able to select document_titles only
- if the document_title is associated with a chatbotsetting done by the business user, client user will have details about that chatbot and will have no other choice but use that one
- if no chatbotsettings are associated to that document_title, user will be presented a form with all fields of th echatbotsettings but his record won't be saved but used ont he fly by LLM agents to fill prompts and code logic.
- later maybe we would provide option for user to use default setting or to use his own chatbot customization.

# Next
- [x] need to fix the logic and get those document_titles showing in the drop down as for the time being they are not
- [x] need to go step by step, after that, need to have the chatbotsetting so information being displayed on the sidebar or if no chatbotsettings associated with the document_title have an empty form for user to customize chatbot, if user sends message without customization, we need to handle that in the backend with default value for chatbot more neutral
- [x] need to have user message visible in the webui with picture next to it
- [x] need to have response answer just under it with chatbot avatar if any or a default one that will be stored in static files just in case
- then need to do all the unit tests
- [x] then need to start pluggin in AI
- [x] then make those agents to interact with user
- then add logging in the codebase
- then create the other asynchrone workflow with agents analyzing logs
- [x] then replace caching with memecache isntead of native django cache or have that as fallback
- then create a report or email stream for Devops/SRE team to have reports on the app logs
- then dockerrize the app
- have docker compose first and see if all works fine
- then add nginx
- then use https self-signed
- then buy real domain and get letencrypt https
- then use dockerhub or other to have the image of the app in a container repo
- then create the terraform to have infrastructure for app in AWS
- then use ansible playbook to setup the server at distance
- then create a repository only for terraform so that we can start preparing the GitOps, organize ansible to be part of it, have github links to repository to get those dockerfiles or dockerhub image
- then do a nice CI with code quality (Sonarqube), Gate (Sonarqube), image scanning (Trivy)
- then have CD using ArgoCD server and the CI when good will update the listening repo image tags which will trigger ArgoCD to deploy new version of app. use githubaction if possible for CI..or have a jenkins server and jenkinsfiles in a repo for the flow.


# javascript making custom data available
```code
# HTML side
<span id="user-avatar" data-avatar-url="{{ user_avatar }}" hidden></span>
# javascript side
const userAvatarUrl = document.getElementById('user-avatar').dataset.avatarUrl;
```
The `data-avatar-url` attribute is a custom data attribute,
and JavaScript allows you to access this attribute using the `.dataset` property.

### How `.dataset.avatarUrl` Works:
- When an HTML element has an attribute like `data-avatar-url`, 
- JavaScript will make it available through the .dataset property of that element.
- `data-` attributes are automatically **converted to camelCase** format in JavaScript.

# javascript get sidebar elements to send with form data
# for form
Use `.value` to get forms fields data
```code
# eg. using Expertise field:
document.getElementById('chatbotExpertise').value;
```
# for HTML text in tags
Use `.innerHtml` to get already populated html text field
```code
# eg. using Expertise field:
document.getElementById('chatbotExpertise').innerText;
```

# install rust side library that will be used by Django
- here we trying to create a module that will be used by Python
to enjoy using Rust for long lasting tasks and enjoy Rust performances

```bash
# 1) install Rust
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh
# 2) check version
rustc --version
# 2') update it (optional or if int he future need to update Rust)
rustup update
# 3) install maturin (will help setup Rust to be Python friendly)
pip install maturin
# 4) create a rust project
maturin new --bindings pyo3 rust_lib
cd rust_lib
# 5) install rust extension-module to PyO3
cargo add pyo3 --features "extension-module"
# 6) open pyproject.toml and update it a bit adding:
- in `[project]`:
version = "<put version , i used same as in cargo.toml 0.1.0>"
description = "<put a description here>"
authors = [{name = "<name>", email = "<email>"}]
- in `[tool.maturin]`:
bindings = "pyo3"
# 7) open Cargo.toml and add dependencies that will be needed like reqwest and more for llm calls
# for HTTP requests to Groq or Ollama APIs...
# for HTTP requests to Groq or Ollama APIs...
reqwest = { "0.11", features = ["blocking"] }
serde = { version = "1.0", feautres = ["derive"] }
serde_json = "1.0"
# 8) open src/lib_rs and put code there for Rust functions to be exportable from Rust and importable from Python
do not forget the decorator: #[pyfunction] for any function defined and #[pymodule] for the bigger exporter wrapper
# 9) install pkg-config and libssl-dev as openssl special version won't be found and it is better so that no need to set the env var everytime
sudo apt-get install pkg-config libssl-dev
sudo apt update
**close terminal if any issue and run net command**
# 10) need to build the rust module
maturin develop
# 11) then we can import the module using the name of the folder like
import rust_lib 
OR from rust_lib import <function name>
# 12) the rust_lib should built and have a bigger size now:
du -hs rust_lib
623M	rust_lib
```
# during development clean up rust built to keep just one
```rust
cargo clean
maturin develop
```

# Rust Code Structure
- Note 1:
When creating a struct to parse the response from API response, we need to match the schema of the response and those fields
eg. response from `Groq`:
```json
{
  "id": "chatcmpl-123",
  "object": "chat.completion",
  "created": 123456789,
  "model": "gpt-3.5-turbo",
  "choices": [
    {
      "index": 0,
      "message": {
        "role": "assistant",
        "content": "The biggest capital city in Asia is Beijing, China."
      },
      "finish_reason": "stop"
    }
  ]
}
```
eg.:
```rust
#[derive(Serialize, Deserialize, Debug)]
struct ApiResponse {
    // The fields that Groq API returns
    choices: Vec<Choice>,
    // If the response has more fields, we need to include them here
    // Optional fields can use `Option<T>` to indicate they may or may not be present.
    #[serde(default)]
    id: Option<String>,
    #[serde(default)]
    created: Option<u64>,
    #[serde(default)]
    model: Option<String>,
}
```
- Note 2:
When calling API make sure to take into consideration `Rust's lifetimes` as the variable sent would outlive the function `lifetime`
if we send an `&` of the variable.
Therefore, **variable sent need to be OWNED** to respect `Rust Lifetime`.
eg: using `.to_string()`, `.to_vec()`...

- Note3:
as the code is compile and used by Pyo# we can't see the `println!'s` instead we can use `eprintln!` which prints to `stderr`
**OR** maybe the best write to a filem this will be handy for our future llm agent that would analyze logs.

# Next
- [x] then need to create new app for agents or have it in the `common` app as central point that all other apps can get agents from
- [x] then implement embedding for business data when recorded by business user (Use Rust and LangGraph)
- [x] then implement retrieval when user sends a message (Use Rust and LangGraph)
- then need to do all the unit tests (I want to cry! hihihihihiiii, ChatGPT Agent Will work with me to streamline this quicker/more productive)
- [x] then make those agents to interact with user
- [x] then add logging in the codebase
- then create the other asynchrone workflow with agents analyzing logs
- then create a report or email stream for Devops/SRE team to have reports on the app logs
- then dockerrize the app
- have docker compose first and see if all works fine
- then add nginx
- then use https self-signed
- then buy real domain and get letencrypt https
- then use dockerhub or other to have the image of the app in a container repo
- then create the terraform to have infrastructure for app in AWS
- then use ansible playbook to setup the server at distance
- then create a repository only for terraform so that we can start preparing the GitOps, organize ansible to be part of it, have github links to repository to get those dockerfiles or dockerhub image
- then do a nice CI with code quality (Sonarqube), Gate (Sonarqube), image scanning (Trivy)
- then have CD using ArgoCD server and the CI when good will update the listening repo image tags which will trigger ArgoCD to deploy new version of app. use githubaction if possible for CI..or have a jenkins server and jenkinsfiles in a repo for the flow.

# Value Proposition of this project:

**Provide business-specific responses by retrieval.**
**Unlike traditional methods that train an LLM on domain-specific data,**
**my rely on the general knowledge of an LLM and supplement it with domain-specific answers.**
**This can indeed significantly reduce complexity and costs while providing high-quality, accurate responses.**

# Embedding and Retrieval flows

**RETRIEVAL**
- Client User Flow:
  - Retrieval Flow:
    -> user send a message >
         perform a safety check on user query and if comply with law >
           - if unsafe or not comply:
               send warning to user and flag user in database and create logs for Devops/Security team 
           - if safe, perform retrieval:
               get document name, AI personality traits needed to perform retrieval and answer user >
                  > x2 retrieval layers: at treshold 0.62 for valid answer and one more at 0.5 to have some other type of questions
                 - if no data retrieved:
                     tell user disclaimer that we didn't find answer in our business data
                     but this what an internet search info about it. Then provide retrieved question form retrieved data at 0.5 if any
                      get the questions to show user which kind of question we have and can answer as sample to inform user.


**EMBEDDING**
- Business User Flow:
  - Embedding Flow:
    -> enters data >
         - data is store in database
         - embedding document creation from database rows >
               - document_title is embedding document name 
                 so "Collection name" {Question:Answer; metadata:document_title}
               - answer is embedded with question to have more context for retrieval
                 and this will be one doc. This is why it is not need to Chunk, just get dataframe rows

We will use python first until the workflow is dont and works fine and then, `We Rust it!`

Decision here initally was to perform internet search if we don't find andswer, but it goes against the purpose of the app which is just to get the answer from business data recorded otherwise get nothing. I have decided to not deliver `nothing` to client user but to provide a disclaimer that we haven't found an answer and that's we have answers to some other questions like ... and here I have decided to show one question or two which were clothe to be selected as valid answers but did fail the relevant score test. I will just just use a lower relevant socre to reveal some question that look like the one that user have asked for as example for user.
So not internet search! (for this version/ for the moment...etc..)

# Embeddings and retrieval
We will use the `document titles` to create the `collections` of data embedded:
- Business user will be storing data and `embedding` it with that `document title` as `collection`
- Client user will be selecting on the webui the `document_title` from side bar dropdown and this will be the targeted `collection` to perform `retrieval` 

# Ollama issues and embeddings
```bash
# install command
curl -fsSL https://ollama.com/install.sh | sh
```
- `OllamaEmbeddings` class deprecated if imported from langchain community:
  - need to install: `pip install -U langchain-ollama` and use `from langchain-ollama import OllamaEmbeddings`
  - The new place of import is now `from langchain-ollama` and not langchain community
  - the class `OllamaEmbeddings` have changed and not supporting temperature as parameter, so i got rid of it (was at 0.1)

# to be able to draw agent workflow
```bash
sudo apt-get update
sudo apt-get install graphviz graphviz-dev
pip install pygraphviz
```
- And, make sure that the `get_graph()` method is called on the object created holding the workflow (`workflow.compile(checkpointer=checkpointer)`)
 

# Next:
- make the full workflow of embedding data when business user enter new records (create/update) and also to delete embedding collection when business user deletes data

# test command for embedding route
Try to send data to embedding route to check if it works fine.
```bash
curl -X POST http://127.0.0.1:8000/agents/embed-data/ \
-H "Content-Type: application/json" \
-d '{
  "document_title": "Business Strategies 2024",
  "question_answer_data": [
    {"question": "What is the vision for 2024?", "answer": "To expand globally."},
    {"question": "What are the key goals?", "answer": "Increase market share by 25%."}
  ]
}'

```

# Next
- need to debug by running server
- then need to test curl command above sending data to be embedded to see if it works
- then need to implement to business data creation/update flow
- then need to have data in vector related to docuemnt deleted when business user deletes the data


# Issues:
- langchain PGVector have changed, it is now using `psycogp3` [see latest doc at ->](https://python.langchain.com/docs/integrations/vectorstores/pgvector/) : 
  - install both psycopg2 and psycopg3: `pip install psycopg2 psycopg`
  - use this psycogp3 connection uri: CONNECTION_STRING = "postgresql+psycopg://user:password@host:port/dbname"

- langchain PGVector has a `use_jsonb=True` which is going to take care of converting metadata to jsonb format. json is going to be deprecated
- langchain PGVector document embedding now have to use `add_documents(documents=list_of_documents)` to call on the PGVector() created object
- Therefore no more `documents=` when creating the PGVector object
- **we had before:**
```python
"""Create and store embeddings in PGVector."""
db_create = PGVector.from_documents(
  embedding=embeddings,
  documents=doc,
  collection_name=collection,
  connection_string=connection,
  distance_strategy=DistanceStrategy.COSINE,
  #distance_strategy="cosine", # can be "eucledian", "hamming", "cosine"EUCLEDIAN, COSINE, HAMMING
)
```
- **we have now:**
```python
"""Create and store embeddings in PGVector."""
db_create = PGVector.from_documents(
  embedding=embeddings,
  collection_name=collection,
  connection=connection,
  distance_strategy=DistanceStrategy.COSINE,
  #distance_strategy="cosine", # can be "eucledian", "hamming", "cosine"EUCLEDIAN, COSINE, HAMMING
  use_jsonb=True,
)

add_documents(documents=list_of_documents)
```
- worked fine when following documentation
- this is curl command to test but need to disable decorator for login required and user test and also when getting data from database get rid of request user:
```python
# disable decorator and get rid of user check when getting info from db
@csrf_exempt
#@login_required(login_url='users:loginbusinessuser')
#@user_passes_test(is_business_user, login_url='users:loginbusinessuser')
def embedData(request, pk):

  # fetch required data from databaase to prepare documents to be embedded
  business_document = get_object_or_404(BusinessUserData, pk=pk) #user=request.user)
```
```bash
# curl command to test from terminal
curl -X POST http://127.0.0.1:8000/agents/embed-data/11/ -H "Content-Type: application/json"**
```

# requirements packaging in a more concise way using pip-chill
```bash
# install
pip install pip-chill
# use
pip-chill > requriements.txt
```


# Prompts length calculation using TikToken
```bash
# install
pip install tiktoken
```
- for Openai based models:
```bash
import tiktoken

def count_tokens(text: str, model: str = "gpt-3.5-turbo") -> int:
    """
    Count the number of tokens in a given text for a specified model.

    Args:
        text (str): The input string to be tokenized.
        model (str): The model's tokenizer to use (default: "gpt-3.5-turbo").

    Returns:
        int: The number of tokens.
    """
    try:
        # Get the tokenizer for the model
        encoding = tiktoken.encoding_for_model(model)
    except KeyError:
        # Fallback to a default encoding if the model is not recognized
        encoding = tiktoken.get_encoding("cl100k_base")
    
    # Tokenize the input text and count tokens
    num_tokens = len(encoding.encode(text))
    return num_tokens

# Example usage
text = "This is an example text to count tokens."
model_name = "gpt-3.5-turbo"
print(f"Number of tokens: {count_tokens(text, model_name)}")

```
- for other models, you need to have informartion about how they tokenize and probably use this custom script
```bash
import tiktoken

# Define a custom encoding (you need to provide vocabulary or rules)
custom_encoding = tiktoken.get_encoding("cl100k_base")  # Use a base encoding scheme

text = "Example text for tokenization."
num_tokens = len(custom_encoding.encode(text))
print(f"Number of tokens: {num_tokens}")
```

# issue calling llm with tools
Groq return that context is too long so i can't use the tool like in the past, i can call the tool node directly using the right schema.
Also when using super context very long one llm, it couldn't format the schema properly making errors. I used llama3 vision as context is super huge but not made for tool call. very `not clever`.... It was actualy puting the function in content mixed with the query in arguments... and not selecting tool in `tool_call` 
- full schema example but not needed full to call tool:
```json
{
  "messages": [
    {
      "content": {
        "function": "retrieve_answer_action",
        "arguments": {
          "query": "Which is the largest capital city in Asia?"
        }
      },
      "additional_kwargs": {},
      "response_metadata": {
        "token_usage": {
          "completion_tokens": 21,
          "prompt_tokens": 5130,
          "total_tokens": 5151,
          "completion_time": 0.028,
          "prompt_time": 1.429650192,
          "queue_time": 0.0011769999999999836,
          "total_time": 1.457650192
        },
        "model_name": "llama-3.2-11b-vision-preview",
        "system_fingerprint": "fp_9cb648b966",
        "finish_reason": "stop",
        "logprobs": null
      },
      "tool_calls": [
        {
          "name": "retrieve_answer_action",
          "args": {
            "query": "Which is the largest capital city in Asia?"
          }
        }
      ],
      "usage_metadata": {
        "input_tokens": 5130,
        "output_tokens": 21,
        "total_tokens": 5151
      },
      "id": "run-d0758597-5e2b-4a0a-8eda-4ea53d398522-0",
      "role": null
    }
  ]
}

```


- instead just call the .run() with the parameter in it on the Toolnode:
```python
...
rephrased_user_query = os.getenv("REPHRASED_USER_QUERY")
# Prepare the schema for the tool call
tool_schema = {
  "query": rephrased_user_query
}
print("Retrieve Answer Tool Schema: ", tool_schema)
# Directly invoke the ToolNode
try:
  response = tool_retrieve_answer_node.invoke(tool_schema, state=state)
...
```

```code
what is the biggest capital city in Asia?
0.4 <class 'str'>
Type docs_and_similarity_score:  <class 'list'> 
Content:  [(Document(id='2', metadata={'id': 2, 'answer': 'Tokyo for population density', 'question': 'what is the biggest capital city in Asia?', 'document_title': 'tokyo'}, page_content='what is the biggest capital city in Asia? Tokyo for population density'), 0.423141683527101), (Document(id='1', metadata={'id': 1, 'answer': 'Edo city', 'question': 'what was the previous name of Tokyo?', 'document_title': 'tokyo'}, page_content='what was the previous name of Tokyo? Edo city'), nan)]
An error occured while trying to perform vectordb search query Expecting value: line 1 column 1 (char 0)
Expecting value: line 1 column 1 (char 0)

[
  (Document(
     id='2', 
     metadata={
       'id': 2, 
       'answer': 'Tokyo for population density', 
       'question': 'what is the biggest capital city in Asia?', 
       'document_title': 'tokyo'
     }, 
     page_content='what is the biggest capital city in Asia? Tokyo for population density'), 
     0.423141683527101
  ), 
  (Document(
     id='1', 
     metadata={
       'id': 1, 
       'answer': 'Edo city', 
       'question': 'what was the previous name of Tokyo?', 
       'document_title': 'tokyo'
     }, 
     page_content='what was the previous name of Tokyo? Edo city'), 
     nan
  )
]

# now get this from running retriever alone:
Type docs_and_similarity_score:  <class 'list'> 
Content:  [(Document(id='2', metadata={'id': 2, 'answer': 'Tokyo for population density', 'question': 'what is the biggest capital city in Asia?', 'document_title': 'tokyo'}, page_content='what is the biggest capital city in Asia? Tokyo for population density'), 0.423141683527101), (Document(id='1', metadata={'id': 1, 'answer': 'Edo city', 'question': 'what was the previous name of Tokyo?', 'document_title': 'tokyo'}, page_content='what was the previous name of Tokyo? Edo city'), nan)]
Score:  0.423141683527101
Error parsing page_content for document 2: Expecting value: line 1 column 1 (char 0)
Skipping document with NaN score: {'id': 1, 'answer': 'Edo city', 'question': 'what was the previous name of Tokyo?', 'document_title': 'tokyo'}
Results from retrieve_relevant_vectors:  []
Type relevant_vectors:  <class 'list'> 
Content:  []
JSON RESPONSE 063:  []
Type docs_and_similarity_score:  <class 'list'> 
Content:  [(Document(id='2', metadata={'id': 2, 'answer': 'Tokyo for population density', 'question': 'what is the biggest capital city in Asia?', 'document_title': 'tokyo'}, page_content='what is the biggest capital city in Asia? Tokyo for population density'), 0.423141683527101), (Document(id='1', metadata={'id': 1, 'answer': 'Edo city', 'question': 'what was the previous name of Tokyo?', 'document_title': 'tokyo'}, page_content='what was the previous name of Tokyo? Edo city'), nan)]
Score:  0.423141683527101
Error parsing page_content for document 2: Expecting value: line 1 column 1 (char 0)
Skipping document with NaN score: {'id': 1, 'answer': 'Edo city', 'question': 'what was the previous name of Tokyo?', 'document_title': 'tokyo'}
Results from retrieve_relevant_vectors:  []
Type relevant_vectors:  <class 'list'> 
Content:  []
JSON RESPONSE 055:  []
nothingu

```

# Next
- Will need to fix the logic in the function to get the answer from the metadata and not from the document content which is here just for similarity and have more context...
- I have decided that the metadata will contain the response and we might actually only embed the question to increase the relevance score as user will just send a question and we searching against that...
- Need to improve function logic and catch errors gracefully 
- Need to implement only question embedding in document content and in the retrieval get the answer from the metadata answer

#### All keys that need to be checked in agent retriever node:
```code
error_vector, answers, nothing
top_n > 1
'score_064_*'
'score_055_*'
top_n = 1
vector_responses["score_063"]
'score_064'
'score_055'
```

# all error types returned by graph: "error", "error_vector", "error_reponse_nothing", "error_reponse_063", "error_reponse_055"
```python
list_errors = ["error", "error_vector", "error_response_nothing", "error_response_063", "error_response_055"]
list_answers = ["response_nothing", "response_063", "response_055"]
```

#### all keys to check in agent app views after retrieval agents are done:
```code
'response_nothing'
'error_response_nothing'
```
```code
[{
  'answer': answer['answer'],
  'score': answer['score'],
  'question': answer['question']
}]
```

# Where are we at:
- [x] ok now the retrieval works for the different scenarios, answer yes, answer questions only, answer no.
- [x] Need to create the AI_PERSONALITY_TRAITS en var or find where we do set those.
- [x] **set AI_PERSONALITY_TRAITS as i don't find it set anywhere** : found this, it set at the normal place in `clientchat` views and using `agents.app_utils.ai_personality` module to create the dictionary and format it and in `view.py` of `clientchat` we are saving the `AI_PERSONALITY_TRAITS`  env var
- [x] we have to embed only the questions in the content part of the document
- [x] we can start plugging in the retrieval graph by moving the functions to the agent app from the test folder and start server and try the flow from user request to UI answer reception: start raw answer and then improve it.




# Next

- need to test webui as the flow goes but not sure why but we are not able to retrieve even with very low score.
- need to handle the error when default bot doesn't exist for selected document
- need to review the connection between bot settings and the business data, as it is too restrictive, we should be able to create several bot settings independently but just linked to a business user in one to one but not one to one to business data

# Issues with collection names
**Can't retrieve even if score close to 0.01 or collection empty of embeddings**
- some collections had double quote `""` and some other no.
- the collections names were case sensitive apparently
- I have created a helper function to normalize the collection names to lowercase strings `.lower()` and if space `" "` there will be a dash `"-"` to replace it: `.replace(" ", "-").lower()`
- I have deleted all collections `delete frm langchain_collection;`
- then retested embedding and retrieval and it worked fine thanks to [langchain documentation on Pgvector psycopg3](https://python.langchain.com/docs/integrations/vectorstores/pgvector/)

# Next
- need to incorporate those fixed issues which are all located in the test folder still and move those to respective locations


# some data created with chatgpt:
```json
"Tokyo Manga Kissa Guide": {
 "What is a manga kissa?": "A manga kissa is a Japanese café where you can read manga, relax, and sometimes use private booths.",
"Can I stay overnight at a manga kissa?": "Yes, many manga kissa offer overnight plans with reclining seats or private booths.",
"Do manga kissa have internet?": "Yes, manga kissa typically provide high-speed internet and computers for browsing.",
"What snacks are available at manga kissa?": "Snacks include instant noodles, drinks, and sometimes free soft drinks or coffee.",
"Are manga kissa expensive?": "Rates are affordable, starting around 400-600 yen per hour. Overnight packages may cost 1,500-2,000 yen.",
"Can foreigners visit manga kissa?": "Yes, manga kissa are open to everyone, though some may have limited English support.",
"What facilities do manga kissa offer?": "Facilities include manga collections, private booths, internet access, showers, and reclining seats.",
"Are manga kissa suitable for families?": "Some manga kissa are family-friendly, but others cater more to solo travelers or adults.",
"What is the atmosphere of a manga kissa?": "It is quiet and cozy, designed for relaxation and reading manga.",
"Where can I find manga kissa in Tokyo?": "You can find manga kissa in Akihabara, Shinjuku, and Ikebukuro, among other areas in Tokyo."
}

"Shibuya Fashion Trends": {
"What is Shibuya fashion?": "Shibuya fashion is a mix of urban, trendy, and youth-driven styles popularized by the district.",
"What is gyaru style?": "Gyaru is a flashy, glamorous fashion style with heavy makeup, bleached hair, and bold outfits.",
"What is streetwear in Shibuya?": "Streetwear includes oversized hoodies, sneakers, and urban designs influenced by skate and hip-hop culture.",
"What is the latest Shibuya fashion trend?": "Currently, oversized outerwear and monochromatic layering are trending in Shibuya.",
"What is 'Harajuku' vs 'Shibuya' style?": "Harajuku is playful and experimental, while Shibuya is urban and polished.",
Where to shop for Shibuya styles?": "109 Shibuya, Parco, and boutique shops in the area are hotspots for trendy fashion.",
"Is Shibuya fashion affordable?": "It depends; streetwear can be affordable, but designer brands can be expensive.",
"Who influences Shibuya fashion?": "Young influencers, models, and pop culture icons drive Shibuya fashion trends.",
"How do locals describe Shibuya style?": "Locals describe it as edgy, expressive, and reflective of youth culture.",
"What is the connection between Shibuya and music?": "Shibuya's fashion is influenced by music scenes like J-pop, hip-hop, and EDM."
}

"Purikura Photo Booths in Japan": {
"What is a purikura?": "A purikura is a Japanese photo booth that lets you take and decorate photos with effects.",
"Where can I find purikura booths?": "Purikura booths are common in malls, arcades, and entertainment areas across Japan.",
"How much does a purikura session cost?": "A purikura session typically costs around 400-600 yen.",
"Can I customize my purikura photos?": "Yes, you can add stickers, text, and effects using touch screens after taking photos.",
"How do purikura booths enhance photos?": "They enhance photos by smoothing skin, enlarging eyes, and adding fun effects.",
"Can I print purikura photos?": "Yes, purikura photos are printed as stickers or small sheets immediately after the session.",
"Can I save purikura photos digitally?": "Many modern purikura booths allow you to save photos digitally via QR codes or apps.",
"Are purikura popular with tourists?": "Yes, tourists love purikura for its fun experience and unique photo designs.",
"What are some tips for taking good purikura?": "Wear bright clothes, use poses, and experiment with effects for the best results.",
"What makes purikura unique?": "Purikura stands out for its customization, group fun, and kawaii (cute) effects."
}

```

# issue with embeddings being stores accross different colleciton
I wonder if it is because in the metadata ids are not unique?
**Godd guess: ChatGPT answer**
```gpt
Yes, your suspicion is correct. If documents from different collections share the same id (even though they belong to different collections), and the backend implementation for storing embeddings in PostgreSQL does not properly differentiate between collections when updating or replacing records, the embeddings could inadvertently overwrite each other.
```
- [x] So here we will use uuids to be sure to have unique ids in embedded document metadata, the businessdata when stored have already a field uuid, I will use that uuid and format it in a string that will get the `count` variable appended at the end, so when we create a list of docs from one collection they share same unique document uuid and different count so that it can't overlap with other documents ids (which will also be like `{businessdata.uuid}-[count]`) 

# result of issue resolution
```psql
chatbotaidb=> select * from langchain_pg_collection;
                 uuid                 |               name               | cmetadata 
--------------------------------------+----------------------------------+-----------
 c8aa8090-931c-419a-b750-41eedd1cc98f | purikura-photo-booths-in-japan   | null
 8a9b880c-a67e-4f64-9bbb-fbfa11c28416 | "purikura-photo-booths-in-japan" | null
 d0c89574-7fa2-4e93-8a11-15fd8814980c | shibuya-fashion-trends           | null
 e09e202a-8ea7-4552-adc1-445e2decd6f8 | tokyo-manga-kissa-guide          | null
(4 rows)

chatbotaidb=> delete from langchain_pg_collection where uuid='8a9b880c-a67e-4f64-9bbb-fbfa11c28416';
DELETE 1
chatbotaidb=> select * from langchain_pg_collection;
                 uuid                 |              name              | cmetadata 
--------------------------------------+--------------------------------+-----------
 c8aa8090-931c-419a-b750-41eedd1cc98f | purikura-photo-booths-in-japan | null
 d0c89574-7fa2-4e93-8a11-15fd8814980c | shibuya-fashion-trends         | null
 e09e202a-8ea7-4552-adc1-445e2decd6f8 | tokyo-manga-kissa-guide        | null
(3 rows)

chatbotaidb=> select count(*) from langchain_pg_embedding where collection_id='c8aa8090-931c-419a-b750-41eedd1cc98f';
 count 
-------
    10
(1 row)

chatbotaidb=> select count(*) from langchain_pg_embedding where collection_id='d0c89574-7fa2-4e93-8a11-15fd8814980c';
 count 
-------
    10
(1 row)

chatbotaidb=> select count(*) from langchain_pg_embedding where collection_id='e09e202a-8ea7-4552-adc1-445e2decd6f8';
 count 
-------
    10
(1 row)

chatbotaidb=> select document from langchain_pg_embedding where collection_id='e09e202a-8ea7-4552-adc1-445e2decd6f8';
                                                                  document                                                                  
--------------------------------------------------------------------------------------------------------------------------------------------
 Do manga kissa have internet? Yes, manga kissa typically provide high-speed internet and computers for browsing.
 Can foreigners visit manga kissa? Yes, manga kissa are open to everyone, though some may have limited English support.
 What facilities do manga kissa offer? Facilities include manga collections, private booths, internet access, showers, and reclining seats.
 What is a manga kissa? A manga kissa is a Japanese café where you can read manga, relax, and sometimes use private booths.
 Are manga kissa expensive? Rates are affordable, starting around 400-600 yen per hour. Overnight packages may cost 1,500-2,000 yen.
 Are manga kissa suitable for families? Some manga kissa are family-friendly, but others cater more to solo travelers or adults.
 Can I stay overnight at a manga kissa? Yes, many manga kissa offer overnight plans with reclining seats or private booths.
 Where can I find manga kissa in Tokyo? You can find manga kissa in Akihabara, Shinjuku, and Ikebukuro, among other areas in Tokyo.
 What is the atmosphere of a manga kissa? It is quiet and cozy, designed for relaxation and reading manga.
 What snacks are available at manga kissa? Snacks include instant noodles, drinks, and sometimes free soft drinks or coffee.
(10 rows)

chatbotaidb=> select document from langchain_pg_embedding where collection_id='d0c89574-7fa2-4e93-8a11-15fd8814980c';
                                                                  document                                                                  
--------------------------------------------------------------------------------------------------------------------------------------------
 What is gyaru style? Gyaru is a flashy, glamorous fashion style with heavy makeup, bleached hair, and bold outfits.
 What is Shibuya fashion? Shibuya fashion is a mix of urban, trendy, and youth-driven styles popularized by the district.
 Is Shibuya fashion affordable? It depends; streetwear can be affordable, but designer brands can be expensive.
 What is streetwear in Shibuya? Streetwear includes oversized hoodies, sneakers, and urban designs influenced by skate and hip-hop culture.
 Who influences Shibuya fashion? Young influencers, models, and pop culture icons drive Shibuya fashion trends.
 Where to shop for Shibuya styles? 109 Shibuya, Parco, and boutique shops in the area are hotspots for trendy fashion.
 How do locals describe Shibuya style? Locals describe it as edgy, expressive, and reflective of youth culture.
 What is 'Harajuku' vs 'Shibuya' style? Harajuku is playful and experimental, while Shibuya is urban and polished.
 What is the latest Shibuya fashion trend? Currently, oversized outerwear and monochromatic layering are trending in Shibuya.
 What is the connection between Shibuya and music? Shibuya's fashion is influenced by music scenes like J-pop, hip-hop, and EDM.
(10 rows)

chatbotaidb=> select document from langchain_pg_embedding where collection_id='c8aa8090-931c-419a-b750-41eedd1cc98f';
                                                            document                                                            
--------------------------------------------------------------------------------------------------------------------------------
 How do purikura booths enhance photos? They enhance photos by smoothing skin, enlarging eyes, and adding fun effects.
 How much does a purikura session cost? A purikura session typically costs around 400-600 yen.
 What are some tips for taking good purikura? Wear bright clothes, use poses, and experiment with effects for the best results.
 What is a purikura? A purikura is a Japanese photo booth that lets you take and decorate photos with effects.
 What makes purikura unique? Purikura stands out for its customization, group fun, and kawaii (cute) effects.
 Can I print purikura photos? Yes, purikura photos are printed as stickers or small sheets immediately after the session.
 Where can I find purikura booths? Purikura booths are common in malls, arcades, and entertainment areas across Japan.
 Are purikura popular with tourists? Yes, tourists love purikura for its fun experience and unique photo designs.
 Can I customize my purikura photos? Yes, you can add stickers, text, and effects using touch screens after taking photos.
 Can I save purikura photos digitally? Many modern purikura booths allow you to save photos digitally via QR codes or apps.
(10 rows)

```

# issues with updating business data and embeddings
Had the issue of having the same data being embedded even if i had updated the database.
After investigating I have noticed that the data need to be saved to database first as the agent embedding route is getting information from database to create new embeddings.

- needed to embed data only if question answer is updated: did create a state variable of previous question answer data and compared the string lenght using json.dumps() against the data updated, and embedding woudl only be started if it differs in length.
- then commited the changes to database and start embedding
- if error in embeddings we keep the data by just reverting back to the state of previous question answer that we save int he database to recover it back.
- the route agents embedding is fetching from database in our logic so if user only updates document name and chatbot settings, update business data will just perform normal updates of database.

Also I got the confirmation that embedding data using same colleciton name overrrides and not increment what has been set their previously
# Next:
- [x] Need to fix the chatbotsettings and be able to create as many as I want as business user
- [x] Need to make the update business data adding the embedding route to it with the logic of create embedding which will override what is there by reembedding all data (more or truncated depends on update)

# Next:
- can start working on replacing AI agent helper functions by rust functions

# Nice To Have
- adding an internal non censored llm (LMStudio or Ollama) that will check if
 `document_name` and `question_answer_data` are safe or not, to refuse recording to database if it is not

# Replacing some `app_utils` function to `Rust` helpers
- create a folder that will have all `app_utils` functions needed to be managed by `Rust` and then import those as module to the `lib.rs` `PyO3` transitioner
```rust
/* Example */
// folder having all helper modules imported as `mod`
mod app_utils;
// access to files inside the folder to import functions needed
use app_utils::ai_personality;
// OR import the funciton directly
use app_utils::ai_personality::personality_trait_formatting
```

- install dotenv like in Python and now we need to find the way from the app_utils modules have access to Django root project .env file to not have it twice as Rust expect it to be in the root directory of the rust project folder or in the directory same as the file calling it or a parent still in rust folder.
From [documentation](https://docs.rs/dotenv/0.15.0/dotenv/fn.from_path.html) of Rust's `dotenv` i have found this way to provide absolute path:
```rust
pub fn from_path<P: AsRef<Path>>(path: P) -> Result<()>
Loads the file at the specified absolute path.

Examples

use dotenv;
use std::env;
use std::path::{Path};

let my_path = env::home_dir().and_then(|a| Some(a.join("/.env"))).unwrap();
dotenv::from_path(my_path.as_path());
```
- so in `app_utils` folder we add a `mod.rs` where we make the modules available and import easier for other files in the directory or other directories:
```rust
pub mod ai_personality;
pub mod load_envs;

```
- import in files in the same dir and use it:
```rust
// when importing from within a module, refer to the parent as crate (app_utils) so the path is from (app_utils)
use crate::app_utils::load_envs::load_env_relative;

pub fn some_function() {
    if let Err(e) = load_env_relative() {
        eprintln!("Failed to load .env in ai_personality.rs: {}", e);
    }
    // Other logic...
}
```
- import in `lib.rs` parent dir"
```rust
mod app_utils;
// here no need to use the word `crate` as it is a child module that we have imported we can use it as defined in mod.rs child file as module

# use app_utils::load_envs::load_env_relative;
use app_utils::ai_personality::load_env_variable;

pub fn main() {
    let env_file_path = "../../.env";
    let env_var_name = "TEST_ENV_VAR";

    match load_env_variable(env_file_path, env_var_name) {
        Ok(value) => println!("Loaded value for '{}': {}", env_var_name, value),
        Err(error) => eprintln!("Error: {}", error),
    }
}
```
- imports `use <module>::<file>::<function>` or `use crate::<module>::<file>::<function>`
```markdown
# When to Use Each
- Use crate:: when you're in a nested module and want to explicitly reference a path starting from the crate root.
- Use the bare module name (e.g., app_utils) when you're already at the crate root or directly importing a sibling module.

# Key Rule of Thumb
- Nested Module (ai_personality.rs): Use crate:: to ensure you're referring to the root-level module.
- Root Module (lib.rs): Use the module name directly, since everything under lib.rs is already in the crate's namespace.

```

# Decision making
I feel like i want to implement to much for the first release and time is running and no release, therefore:
- i have decided to go easy on Rust module and just do some implementation to learn, easy ones. Use agent app utils that are not too complicated and make rust running those so that I can learn some concepts lioke postgresql connection with rust using tokio and env var management, modular rust use of different files and folders etc...
- easy wizzy pizzy !
- then I will start implementing logging which is the next big step, decide on log format to be able to be consummed easily for me (custom), ELK, Prometheus and all their friends as well...
- then after the logging files are determined and centralized, we can start pluggin in the new AI agent team which will work on those logs only and create reports and will notify using email/ordiscord/ or I need to decide this as well.
- After that we need to create the server Nginx and make sure it works with it.
- Then we need to use gunicorn for the moment behind nginx for simplicity as we have done this before, but using 'Rust' could be cool, but i still have in mind that django has its ownspeed limit so no need to have a flash speed magnum in front of it as it won't be able to handle it anyways, so just to learn maybe... for the moment gunicorn and its script.
- then create the containers for the app
- when all that is done we can open our test kubeadm cluster and use terraform to deploy the application...Ansible with it? an ansible server inside kubvernetes? i don't know will talk with ChatGPT...
- I don't like to do it but need to do the unit tests using ChatGPT and the github action as well to run tests.
- HAVE TO MOVE A BIT QUICKER FROM NOW ON AN MAKE THIS APP HAPPEN! DOMAIN NAME AND AWS HOSTED!

# Rust `Tokio` for `Postgreql` connection
source: [documentation](https://docs.rs/tokio-postgres/0.7.12/tokio_postgres/#example) 

- OR update `project.toml` file with
```toml
[dependencies]
tokio = { version = "1.0", features = ["full"] }
dotenv = "0.15"
tokio-postgres = "0.7"
```
- Or use terminal: Add with cargo
```bash
cargo add tokio --features full
cargo add dotenv
cargo add tokio-postgres
```
- Then
```bash
maturin develop
```

- ChatGPT step explanation
```bash
# Add a Rust dependency
cargo add tokio --features full
```
```bash
# Develop the Python module
maturin develop
```
```bash
# Test the installed module in Python
python -c "import your_module; print(your_module.some_function())"
```
```markdown
- When to Use maturin develop vs maturin build

   - Use maturin develop: During active development for faster iteration and testing in your Python environment.
   - Use maturin build: When preparing your project for distribution (e.g., creating .whl files for publishing to PyPI).
```

# Tiktoken.rs different encoding schemes to choose from
- I just choose the base one
| Encoding name	| OpenAI models |
|---------------|---------------|
| o200k_base	| GPT-4o models, o1 models|
| cl100k_base	| ChatGPT models, text-embedding-ada-002|
| p50k_base	| Code models, text-davinci-002, text-davinci-003|
| p50k_edit	| Use for edit models like text-davinci-edit-001, code-davinci-edit-001|
| r50k_base (or gpt2)	| GPT-3 models like davinci|


# Rust From GPT To fix 
- ChatGPT helps but there were some errors and here are the fix

| Aspect Original Code | Fixed Code |
|----------------------|------------|
| Encoding Function get_encoding (non-existent) | cl100k_base (correct function) |
| Dependency (lazy_static) Missing | Added to Cargo.toml |
| ENCODER_CACHE Definition Error due to missing lazy_static | Correctly initialized with lazy_static |
| Python Wrapper Type Mismatch String errors returned directly | Mapped String to PyErr for Python |

# how to test functions implemented in rust after compilation `maturin develop`
- Example:
```python
from rust_lib import safe_json_dumps_py

data = {"key": "value", "nested": {"inner_key": 123}}
print(safe_json_dumps_py(data))  # Outputs formatted JSON
print(safe_json_dumps_py(12345))  # Outputs "12345"
```

# List of function being processed by rust and their story
- [x] `ai_personality` file have been handed to rust and replaced by `load_personality`: the only place where we need this is in `clientchat/views/clientuserchat function`, where we set the environment variable `AI_PERSONALITY_TRAITS` which will be pulled by retriever agent in the `answer_to_user` node.
- [x] `delete_embeddings` file has also been handed to rust and replaced by `delete_collection_py` which will connect to the database and get rid of the collection passed in the function. The route `deleteBusinessData` is the one calling the internal API, in `agents` app which has a `deleteEmbeddings` route that deletes the coleciton therefore the embeddings stored in that collection. so this function handed to rust is used only in `agents views` 

```bash
chatbotaidb=> select * from langchain_pg_collection ;
                 uuid                 |              name              | cmetadata 
--------------------------------------+--------------------------------+-----------
 c8aa8090-931c-419a-b750-41eedd1cc98f | purikura-photo-booths-in-japan | null
 d0c89574-7fa2-4e93-8a11-15fd8814980c | shibuya-fashion-trends         | null
 e09e202a-8ea7-4552-adc1-445e2decd6f8 | tokyo-manga-kissa-guide        | null
 21799745-b3c8-4ed2-a0de-4af9418780c4 | rust-test                      | null
(4 rows)

chatbotaidb=> select * from langchain_pg_collection ;
                 uuid                 |              name              | cmetadata 
--------------------------------------+--------------------------------+-----------
 c8aa8090-931c-419a-b750-41eedd1cc98f | purikura-photo-booths-in-japan | null
 d0c89574-7fa2-4e93-8a11-15fd8814980c | shibuya-fashion-trends         | null
 e09e202a-8ea7-4552-adc1-445e2decd6f8 | tokyo-manga-kissa-guide        | null
(3 rows)
```
- [x] `string_to_dict_py1` works fine it is a helper function that we can use to replace the occurances where it is used:  we use it in the `agents/app_utils/formatters` and in `agents/app_utils/call_llm`. Have swapped but for `agents/app_utils/call_llm` might be using the rust counterpart if needed. this is just a small change to learn rust and improve our understanding of rust interactions with python
```python
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

```
- [x] `collection_normalize_name_py` has worked fine but for this one as it is used in many places instead of going to there i will just replace the helper module and use same function name but put this rust helper inside of it. (I probably should do same for the previous ones to have just a single point to change...) `DONE!`
- [x]  `token_counter_py` did work fine so i can use it if needed, for the time being it is not implemented nowhere, nice to have!
```python
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
```
```python
# returned
Outputs: 491
```
Tested using GPT4o&40-mini [Openai Tokenizer](https://platform.openai.com/tokenizer) and got:
```bash
TOkens: 474, Characters: 2297
```
Very close i just use the base tokenizer so it is fine!

- [x] Done with our first easy round of Rust helper implementation, let's keep learning!

# Issue with ChatGPT code **`WARNING`**
The code was executing a command to drop the table entirely!!!!
We need just a little command to delete only one collection....
**Therefore, be careful and never trust LLMs!!!**
- delete embedding collection from terminal
```psql
delete from langchain_pg_collection where name='Shibuya Fashion Trends';
```
- but in the `SQL` query we need to put the name in double quotes `"colection name"` to not get error for `-` character that would be missinterpreted by `psql` therefore,
  need to escape with backslashes but here we don't need because the `$1` will be making sure that the name is well formatted and `-` character won't be an issue anymore.
```rust
  let delete_collection_query = "DELETE FROM langchain_pg_collection WHERE name = $1;";
    client
      .execute(delete_collection_query, &[&collection_name])
      .await
      .map(|_| "Collection deleted successfully".to_string())
      .map_err(|e| format!("Error executing query: {}", e))
```


# Next
- [x] need to keep going on the rsut functions testing and replacement of their python counterparts
- [x] need to to run app and test collection creation and deletion from business user UI interface to validate that it works as we need probably to improve the returned value from rust. No it is fine, i have checked the original function also just returns a string saying "success". **ISSUE**:  Error making the request: Expecting value: line 3 column 1 (char 2)  `This form trying to delete from the webui, we will stop for today and come back tomorrow to it to have fresh mind`


# issue with deletion of embedding when integrating rust counterpart
 **ISSUE**:  Error making the request: Expecting value: line 3 column 1 (char 2)  `This form trying to delete from the webui, we will stop for today and come back tomorrow to it to have fresh mind`
- **Troubleshooting:**
  - had some redirects for the internal API call to agents route that deletes the embeddings
  - had wrong authentication setup in the `@login_required()` decorator which was set to `clientuser` who is not permitted to access to `businessuser` routes
  - had also not sent the authentication data for the route using cookies

- **Solution:**
  - have changed the `@login_required()` decorator to authorize only `businessuser` for the deletion route
  - have integrated the authentication data in the cookies passed to the internal API route. 
```python
# PREVIOUSLY
delete_embed_data_url = reverse("agents:delete-embedding-collection", kwargs={"pk": document_title_id})
# Construct the full URL using the request's base URI
full_url = request.build_absolute_uri(delete_embed_data_url)
try:
  # call the route using post request for the moment if we need to add data to payload (which is empty in this code version)
  response = requests.post(full_url, headers={"Content-Type": "application/json"})

# FIX
delete_embed_data_url = reverse("agents:delete-embedding-collection", kwargs={"pk": document_title_id})
# Construct the full URL using the request's base URI
full_url = request.build_absolute_uri(delete_embed_data_url)
session = requests.Session()
try:
  # call the route using post request for the moment if we need to add data to payload (which is empty in this code version)
  response = session.post(full_url, headers={"Content-Type": "application/json"}, cookies=request.COOKIES)
```


# Next 
- [x]  start implementing logging which is the next big step, decide on log format to be able to be consummed easily for me (custom), ELK, Prometheus and all their friends as well...


# Issue github push
```bash
warning: refname 'HEAD' is ambiguous.
warning: refname 'HEAD' is ambiguous.
warning: refname 'HEAD' is ambiguous.
```
deleted: `rm .git/refs/HEAD` being a double file pointing to HEAD
at the end just deleted `.git`, did a `git clone` and copier the `.git` to the project folder.


# LOGGING

- eg.:
  - # we have the choice to use either of those two to have logs rotation: `RotatingFileHandler`, `TimedRotatingFileHandler`

```python
import os
# we use this one in the code example: `TimedRotatingFileHandler`
from logging.handlers import RotatingFileHandler, TimedRotatingFileHandler

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'standard': {
            'format': '%(asctime)s [%(levelname)s] %(name)s: %(message)s'
        },
        # JSON better for Prometheus and ELK
        'json': {  # Better for Prometheus, Loki, or ELK stacks
            'format': '{"time": "%(asctime)s", "level": "%(levelname)s", "name": "%(name)s", "message": "%(message)s"}'
        },
    },
    'handlers': {
        'file_debug': {
            'level': 'DEBUG',
            # this for logs rotation
            'class': 'logging.handlers.TimedRotatingFileHandler',
            # log file location
            'filename': os.path.join(BASE_DIR, 'logs/debug.log'),
            'when': 'midnight',
            # Keep logs for 7 days
            'backupCount': 7,
            # Choose this formatter JSON better for Prometheus and ELK
            'formatter': 'json',
        },
        'file_info': {
            'level': 'INFO',
            'class': 'logging.handlers.TimedRotatingFileHandler',
            'filename': os.path.join(BASE_DIR, 'logs/info.log'),
            'when': 'midnight',
            'backupCount': 7,
            'formatter': 'json',
        },
        'file_warning': {
            'level': 'WARNING',
            'class': 'logging.handlers.TimedRotatingFileHandler',
            'filename': os.path.join(BASE_DIR, 'logs/warning.log'),
            'when': 'midnight',
            'backupCount': 7,
            'formatter': 'json',
        },
        'file_error': {
            'level': 'ERROR',
            'class': 'logging.handlers.TimedRotatingFileHandler',
            'filename': os.path.join(BASE_DIR, 'logs/error.log'),
            'when': 'midnight',
            'backupCount': 7,
            'formatter': 'json',
        },
        'file_critical': {
            'level': 'CRITICAL',
            'class': 'logging.handlers.TimedRotatingFileHandler',
            'filename': os.path.join(BASE_DIR, 'logs/critical.log'),
            'when': 'midnight',
            'backupCount': 7,
            'formatter': 'json',
        },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'standard',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file_debug', 'file_info', 'file_warning', 'file_error', 'file_critical', 'console'],
            'level': 'DEBUG',
            'propagate': True,
        },
        'myapp': {
            'handlers': ['file_debug', 'file_info', 'file_warning', 'file_error', 'file_critical', 'console'],
            'level': 'DEBUG',
            'propagate': False,
        },
    },
}

- eg. of use in code :
import logging
# here is where you can set the name of the loggers to match the name of the one in settings.py
# better to have those same as the application name so we know where it is coming from directly
logger = logging.getLogger('myapp')
logger.debug("This is a debug message.")

```


- think at logging to file instead of printing everywhere:
```python
import logging

# this for timestamps
logging.basicConfig(format='%(asctime)s %(message)s')
# this for the logginf message with the level of logging
logging.warning('is when this event was logged.') 

# need to do the configs better in settings.py
We have commented out advance logging settings and need to work on it
```
- extras:
**Fetching Logs with Prometheus or Other Tools**
- Prometheus with Loki: Use Loki as a log aggregation tool. It works seamlessly with Prometheus.
  - Install promtail, a log collector, and point it to your log files.
  - Configure promtail to scrape the JSON logs from your Django project.

- ElasticSearch (ELK Stack):
  - Use Filebeat or Logstash to ship logs to ElasticSearch.
  - Parse the JSON logs for advanced search and filtering.

- AWS CloudWatch or GCP Logging:
  - Use SDKs or agents to push logs from your Django server to these managed log services.

- ChatGPT suggestions to improve how I log files:
  1. in `setting.py`
```python
# settings.py
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'json': {
            'format': (
                '{"time": "%(asctime)s",'
                ' "level": "%(levelname)s",'
                ' "name": "%(name)s",'
                ' "message": "%(message)s",'
                ' "user_id": "%(user_id)s"}'
            )
        },
        'standard': {
            'format': '%(asctime)s [%(levelname)s] %(name)s: %(message)s'
        },
    },
    'handlers': {
        'master_file': {
            'level': 'DEBUG',
            'class': 'logging.handlers.TimedRotatingFileHandler',
            'filename': os.path.join(BASE_DIR, 'logs', 'master.log'),
            'when': 'midnight',
            'backupCount': 7,
            'formatter': 'json',
        },
        'agents_file': {
            'level': 'DEBUG',
            'class': 'logging.handlers.TimedRotatingFileHandler',
            'filename': os.path.join(BASE_DIR, 'logs', 'agents.log'),
            'when': 'midnight',
            'backupCount': 7,
            'formatter': 'json',
        },
        # similarly for 'businessdata_file', 'rust_file', etc.
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'standard'
        },
    },
    'loggers': {
        '': {  # Root logger
            'handlers': ['master_file', 'console'],
            'level': 'DEBUG',
        },
        'agents': {
            'handlers': ['agents_file', 'master_file', 'console'],
            'level': 'DEBUG',
            'propagate': False,
        },
        'businessdata': {
            'handlers': ['businessdata_file', 'master_file', 'console'],
            'level': 'DEBUG',
            'propagate': False,
        },
        # etc.
    }
}
```

  2. create a custom filter in a file to be able to add custom fields in the logging data. I have requested for `GDPR` anonymized `user` using the `user_id`

```python
# create a .py file living in an app (i will use the app that i called `common` that i have created on purpose for centralized stuff)
class UserIDFilter(logging.Filter):
    def filter(self, record):
        # If you have something like a thread-local or a context local
        # that stores the user, you can retrieve it here.
        # Or you can set it in your view code before logging.
        user_id = getattr(record, 'user_id', 'anonymous')
        record.user_id = user_id
        return True
```
    -  in `settings.py` add the filter which will be using the helper custom module function created
```python
'filters': {
    'user_id_filter': {
        '()': 'path.to.UserIDFilter',
    },
},
...
'handlers': {
    'master_file': {
       'filters': ['user_id_filter'],  # attach the filter
       ...
    },
}
```

    - in the code: just use it this way for the custom field `user_id` to be populated. Maybe need here to add hashing of the id before storing so it is really anonymized (or an algo that only Devops Security team can verse to identify user (Ban, notify, warn..etc..))

```python
logger = logging.getLogger('agents')
logger.info("Something happened", extra={'user_id': request.user.id})
```
  3. Rust logging to be improved for more pro code using `tracing` and `tracing_subscriber`
    - so here we will create this function in `rust` and then use PyO3 to be able to call it from p`Django`
      in `common` app's `app.py` that is where you call it, so it is called once only when `Django` starts, this can be done also:
        - `lazy` the first time we call `rust` funcitons
        - or in `wsgi.py` or `asgi,py`: the real entrypoints of the `Django` project

```bash
# install tracing and the subscriber and listener (can be done in one line)
cargo add tracing
cargo add tracing-subscriber
cargo add tracing-appender
```
```rust
// those are the macros that can be used to write logs at different levels, eg.: `info!("Rust function invoked");`
use tracing::{info, error, warn};
use tracing_subscriber::{fmt, EnvFilter};
use std::path::Path;

#[pyfunction]
pub fn init_rust_logging(log_dir: &str) {  // function to be called to initialize log file location
    let log_file_path = Path::new(log_dir).join("rust.log");
    // here we have the log file rust.log and the dir will be givieng as parameter
    // from the python side so that we can control and centralize all logs in same folder
    // here we log `daily` before opening a new file
    let file_appender = tracing_appender::rolling::daily(log_dir, "rust.log");

    let (non_blocking, _guard) = tracing_appender::non_blocking(file_appender);

    tracing_subscriber::fmt()
        .json()
        .with_env_filter(EnvFilter::from_default_env())
        .with_writer(non_blocking)
        .init();
}
...
#[pyfunction]
fn your_pyo3_func() -> PyResult<()> {
    info!("Rust function invoked");
    // ...
    Ok(())
}
...
// need to import the log funciton in python to initialize there from any `app.py` apps or `wsgi` or `asgi` or calling it once in the code logic like `lazy init`
#[pymodule]
fn my_rust_module(py: Python, m: &PyModule) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(init_rust_logging, m)?)?;
```
```python
# in the python side eample here in agents/app.py
from django.apps import AppConfig
import os
from rust_lib import init_rust_logging  # or wherever your PyO3 module is accessible

class AgentsConfig(AppConfig):
    name = 'agents'

    def ready(self):
        # This method is called once when Django loads this app.
        # here we set where the log folder will be, we might use an `os.getenv('LOG_FOLDER_CENTER')`
        logs_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'logs')
        # Or read from settings: logs_dir = settings.LOGS_DIR
        try:
            my_rust_module.init_rust_logging(logs_dir)
        except Exception as e:
            print(f"Failed to init rust logging: {e}")

```
      - Now use `tracing` and call logs from anywhere like that
```rust
// so you can just use this import and call any of the macros `info, debug, error` where ever you want in the functions
use tracing::{info, debug, error};

pub fn do_something() {
    debug!("Some debug info about do_something()");
}
```

# logs output format `JSON` normalized for easy ELK/ Prometheus cosomption
- Rust:
```json
{
  "timestamp":"2024-12-21T12:34:56.789Z",
  "level":"INFO",
  "fields":{"message":"Rust logger initialized successfully!"},
  "target":"my_crate",
  ...
}
```
- Python:
```json
'{"time":"%(asctime)s","level":"%(levelname)s","logger":"%(name)s","msg":"%(message)s"}'
```

# **Important about log files**
- `Django` log file a really rotated meaning deleted for new ones (here 7 days frequency and at midnight as setup)
- `Rust` log files from `tracing` are rotated so a new file is created but the previous file is not deleted: **Need to setup a `CRON` job for exampel to get rid of files every 7 days at midnightooooo**


- Finally log anything like that

```
# in any app put a file with this (I will use common app and call the file logs_filters.py)
import logging
from common.middleware import get_current_user

class UserIDFilter(logging.Filter):
  def filter(self, record):
    user = get_current_user()
    record.user_id = getattr(user, 'id', 'anonymous') if user and user.is_authenticated else 'anonymous'
    return True

```

```python
# in any app create a middleware_logs_custom.py file (but we will use the common app for that)
import threading
from django.utils.deprecation import MiddlewareMixin
from django.http import HttpRequest


_user = threading.local()

class CurrentUserMiddleware:
  def __init__(self, get_response):
    self.get_response = get_response

  def __call__(self, request):
    # Set the current user
    _user.value = getattr(request, 'user', None)
    response = self.get_response(request)
    # Clear the current user after the response
    _user.value = None
    return response

def get_current_user():
  return getattr(_user, 'value', None)
```

```python
# in settings.py, add to the existing middleware your custom middleware
MIDDLEWARE += ['common.middleware_logs_custom.CurrentUserMiddleware']
```

```python
# in settings.py add the filter to the logging settings
'filters': {
  'user_id': {
    '()': 'common.logs_filters.UserIDFilter,
  },
},
```

If the logger has the formatter in `settings.py` set to `json` it will populate automatically the `user_id` fields of the formatter
```python
import logging

agents_app_logger = logging.getLogger('agents')
...
# and in the code
agents_app_logger.info("YO! Log me mate!")

```



# Logs Analyzer Agent
- Have decided to have this workflow for those agents (diagram)[https://excalidraw.com/#json=_0ArgZFueZlFBjbaY8JTo,2uLdGqeTDsLRgZgrdlqiRw]: 
  1. - Copy log file
  2. - chunk and store to `SQLite`
  3. - Classify Logs : check chunks for error, warning, critical flags
  4. - Provide Advice: Get from error, critical, warning flagged schemas
  5. - Notify Devops/Security (`email`, `discord`, `Slack`.....)
  6. - Delete all logs from the agents temporary files folder and delete from database (`SQLite` special for log agents only)

- Have choose to just use `SQLite` for agents to work with log parsing and classification as it is fast and good for small cron job temporary database
  we can even detroy it completly and recreate a new one. but wil just free the database and have it emptied out
- Need to add the `SQLite` database in Django's `setting.py` (documenting myself on subject reading Django  docs)
  1. - selecting which database to record get from: `<model_class_name>.objects.using("<other_db_name>")`
  2. - saving to other db than the default one: `<model_class_object>.save(using="<other-db_name>")`
  3. - will need to create a model for the SQLite database to store data chunks and schemas
  4. - will need in `settings.py` to add a router for this `SQLite` database agent log analyzer only so it is separated from user's `PostgresQL` database default
  5. - command to migrate the to the database `SQLite3`: `python3 manage.py migrate --database=logs_analyzer`
       - This will see the models.py 
         > admin.py registered model
           > go to setting.py see the database router
             > which points to the router.py file
               > which has the class that tells to save model to the SQLite3 database
                 > database that is listed in the databases of settings.py

- command to install `SQLite3` but should be installed with Django but we never know
```bash
# ubuntu
sudo apt update
sudo apt install sqlite3
# python module compatibility
sudo apt install libsqlite3-dev
```
- `routing.py` like file
```python
class LogsAnalyzerRouter:
  logs_analyzer_db = "logs_analyzer"
  default_db = "default"

  def db_for_read(self, model, **hints):
    if model._meta.app_label == 'agents':
      return self.logs_analyzer_db
    return None

  def db_for_write(self, model, **hints):
    if model._meta.app_label == 'agents':
      return self.logs_analyzer_db
    return None

  def allow_migrate(self, db, app_label, model_name=None, **hints):
    if db == 'logs_analyzer':  # Only target the SQLite database
      # Allow migrations only for the agents app
      return app_label == 'agents'
    # For the default database, allow migrations for other apps
    return db == 'default'
```

- in `models.py` we need to setup a app_label meta class in the model
```python
class .....:
  fields...
  ...

  class Meta:
    app_label = 'agents'
```

- in `setting.py` have the second database listed on your `routing.py` file like located in `DATABASE_ROUTER`
```python
# PostgresQL db custom
DATABASES = {
  'default': {
    'ENGINE': 'django.db.backends.postgresql_psycopg2',
    'NAME': os.getenv("DBNAME"),
    'USER': os.getenv("DBUSER"),
    'PASSWORD': os.getenv("DBPASSWORD"),
    'HOST': os.getenv("DBHOST"),
    'PORT': os.getenv("DBPORT"),
  },
  'logs_analyzer': {
    'ENGINE': 'django.db.backends.sqlite3',
    'NAME': BASE_DIR / 'db.sqlite3',
  }
}

# this for the log analyzer agent to use only the SQLite database
DATABASE_ROUTERS = ["agents.routing_sqlite_db.LogsAnalyzerRouter"]
```

**HAVE PIVOTTED AND DECIDED TO JUST USE THE POSTGRESQL DATABASE AS THE ROUTING TO THE SECOND DATABASE IS NOT WORKING AND i AM NOT GONNA STAY ON IT SEVERAL DAYS**

**How to record data using psycopg3 connection to a django model defined table from the database ?**
- Django maps each model to a database table. The table name is: <app_label>_<model_name> (e.g., agents_loganalyzer for the LogAnalyzer model in the agents app).


### Log lines are like:
`{"time": "2024-12-26 21:40:05,565", "level": "INFO", "name": "users", "message": "Username OR Password is incorrect", "user_id": "anonymous"}`
`{"time": "2024-12-28 23:35:23,345", "level": "DEBUG", "name": "httpx", "message": "load_verify_locations cafile='/home/creditizens/djangochatAI/djangochatbotAI_venv/lib/python3.12/site-packages/certifi/cacert.pem'", "user_id": "anonymous"}`
'format': (
  '{"time": "%(asctime)s",'
  ' "level": "%(levelname)s",'
  ' "name": "%(name)s",'
  ' "message": "%(message)s",'
  ' "user_id": "%(user_id)s"}'
)

so maybe use json.dumps(line)["level"], to get filter on log levels.

### Python log levels:
[source](https://www.logicmonitor.com/blog/python-logging-levels-explained) 
- Debug = 10: This level gives detailed information, useful only when a problem is being diagnosed.
- Info = 20: This is used to confirm that everything is working as it should.
- Warning = 30: This level indicates that something unexpected has happened or some problem is about to happen in the near future.
- Error = 40: As it implies, an error has occurred. The software was unable to perform some function.
- Critical = 50: A serious error has occurred. The program itself may shut down or not be able to continue running properly.


# notification of Devops/Security team via Discord (as Node)
```python
# install the webhook tro form this kind of url and have access to discord channel: `https://discord.com/api/webhooks/{webhook_id}/{webhook_token})`
pip install discord-webhook
# in dsicord: go to `settings > Integration > Create Webhook` to create the webhook
# create a `discord_notification_app_logs` function and beware file size max for discord uplaod 8MB maybe less

import os
from discord_webhook import DiscordWebhook

def send_large_log_to_discord(log_file_path):
    """
    Sends a large log file to a Discord channel using a webhook. If the file exceeds 8 MB, it splits the file into
    smaller chunks and sends each chunk separately.

    :param log_file_path: Path to the log file to be sent.
    """
    # Replace with your actual Discord Webhook URL
    webhook_url = "https://discord.com/api/webhooks/{webhook_id}/{webhook_token}"

    # Define the maximum file size in bytes (8 MB)
    MAX_FILE_SIZE = 8 * 1024 * 1024  # 8 MB in bytes

    # Check if the file exists
    if not os.path.exists(log_file_path):
        print(f"Error: The file '{log_file_path}' does not exist.")
        return

    # Get the file size
    file_size = os.path.getsize(log_file_path)

    if file_size <= MAX_FILE_SIZE:
        # Send the file as-is if it's under the limit
        send_file_to_discord(webhook_url, log_file_path)
    else:
        # Split and send the file in chunks
        print(f"The file '{log_file_path}' exceeds 8 MB (size: {file_size / (1024 * 1024):.2f} MB). Splitting into chunks.")
        
        # Open the file in binary mode
        with open(log_file_path, "rb") as file:
            chunk_number = 1
            while True:
                # Read a chunk of MAX_FILE_SIZE bytes
                chunk = file.read(MAX_FILE_SIZE)
                if not chunk:
                    break
                
                # Create a temporary chunk file
                chunk_filename = f"{log_file_path}_part{chunk_number}.log"
                with open(chunk_filename, "wb") as chunk_file:
                    chunk_file.write(chunk)
                
                # Send the chunk to Discord
                print(f"Sending chunk {chunk_number}...")
                send_file_to_discord(webhook_url, chunk_filename)

                # Delete the temporary chunk file after sending
                os.remove(chunk_filename)
                chunk_number += 1

        print("All chunks have been sent successfully.")

def send_file_to_discord(webhook_url, file_path):
    """
    Helper function to send a single file to Discord.

    :param webhook_url: The Discord webhook URL.
    :param file_path: Path to the file to be sent.
    """
    webhook = DiscordWebhook(url=webhook_url, content=f"📄 **Log Report Chunk**: {os.path.basename(file_path)}")
    try:
        with open(file_path, "rb") as file:
            webhook.add_file(file=file.read(), filename=os.path.basename(file_path))

        response = webhook.execute()

        if response.status_code == 200:
            print(f"Chunk {os.path.basename(file_path)} sent successfully.")
        else:
            print(f"Failed to send chunk {os.path.basename(file_path)}. HTTP Status Code: {response.status_code}")
            print(response.content)
    except Exception as e:
        print(f"An unexpected error occurred while sending {file_path}: {e}")




# can set up then a crontab but see the example in the next point better as it is using a script `.sh`
crontab -e
#Add an entry (replace paths as necessary):
0 6 * * * /path/to/python /path/to/send_discord_log.py /path/to/log_report.log
```

# cronjob to start periodically the Log Agent Team
```python
import os
from langgraph import LangGraph  # Replace with your actual LangGraph import

def main():
  try:
    # Initialize LangGraph agent
    agent = LangGraph(config_file="path/to/langgraph_config.json")

    # Run the agent
    result = agent.run()

    print(f"LangGraph agent completed with result: {result}")
  except Exception as e:
    print(f"Error running LangGraph agent: {str(e)}")

if __name__ == "__main__":
    main()
```
```bash
# make it executable to not get any errors
sudo chmod +x /path/to/start_langgraph_agent.py
```
```bash
# this will setup the cronjob using a script file so that we can reuse
nano setup_cronjob.sh:
#!/bin/bash

# Variables
PROJECT_ROOT="$(dirname "$(realpath "$0")")"  # Automatically find the root directory of the Django project
PYTHON_PATH="/path/to/python"  # Path to the Python executable
SCRIPT_PATH="$PROJECT_ROOT/common/log_agents_jobs.py"  # Path to the Python script inside the common app
CRON_TIME="0 3 * * *"  # Schedule: 3:00 AM daily

# Check if cronjob already exists for the script
if crontab -l 2>/dev/null | grep -q "$SCRIPT_PATH"; then
  echo "Cronjob already exists for the script."
else
  # Add the cronjob
  (crontab -l 2>/dev/null; echo "$CRON_TIME $PYTHON_PATH $SCRIPT_PATH") | crontab -
  echo "Cronjob added successfully."
fi


```
**CRONJOB NEED TO BE SET UP ONLY ONCE WEB SETTING UP THE SERVER**
```bash
# make the file executable
sudo chmod +x setup_cronjob.sh
# run job
./setup_cronjob.sh

```

# to update cronjob time:
```bash
crontab -e
# then select vim or nano and update time
10 19 * * *   fo rme to see it running now and test it which is 19:10
# to delete cronjob
crontab -r
# to list available cronjobs
crontab -e
# where is cron file located
sudo cat  /var/spool/cron/crontabs/<user>
```

# final cronjob setup
- have created a `.sh` file in root project dir and cronjob will call it to start the log analyzer job.
  the `.sh` script has the path of the virtualenv `python` binary and the path of the graph


# curl command to test Discord webhook
curl -X POST -H "Content-Type: application/json" \
-d '{"content": "Hello, Discord! This is a test message from curl."}' \
"https://discord.com/api/webhooks/{id}/{token}"


# Next
- [x] need to test nodes independently
- [x] have already added dummy data is logs files and will use that to verify that the data expected to have on `discord` is the same
- [x] Have already tested the discord webhook using curl command and it works so if agent is not hallucinating while using the tool it should work
- [x] run the full graph successfully
- [x] have to test the cronjob after having ran successfully the full graph to see if it launches the job and works fine (no permission errors for example)
- [x] add logging to common app utility functions
- [x] run the django server with gunicorn until it works fine and then use the application and see if all works fine at minimum
- [x] setup nginx after gunicorn works
- [] do unit tests even if we don't want to do those, lets cover some percentage of the application using GPT or Gemini or Bolt.new/ottodev ....
- [] check that the github action works fine
- [] create container of app and also a docker-compose and see if it wokrs in local docker so that we can kubernetize it...
- [] then use this app for any devops workflow that we want to do (push enhancement of app and have the ci/cd work by itself and do all necessary notifications (Dicord: the webhook stuff is simple and works fine so we will be using that)


### troubleshooting
- now trying to run the graph and pass nodes one by one by debugging and checking logic.
  - noticed that not all files are read and CRITICAL and ERROR are not detected: check logic , something is wrong
  - we get success message but in postgresql nothing is stored, database is empty: test function independently with dummy data

Better test each function independently, then run graph node...

### Graph Log Analyzer Agent Works!
Now that the graph works fine and environment variables are set, just need to move it away form the django workflow as this is a cronjob that is going to run on the server running the django app.
Therefore, we will put the graph in a folder at the root directory of the project. where the cronjob will be able to action it from. all folders path are set properly already but still need to change the one that copies the log files. to be next to the graph log analyzer. so, set this up and then start coding the bash script


# Decisions for the agent graph flow and how it would be trigggered
I wanted to use cronjob but actually, I have decided to have a full django workflow for that and not a cronjob, 
The admin would login and go to a specific path which will be hosted by the`common` app.
Then it will render a html page with a button asking to start log analysis by agent team.
Then the html page would render the result while in parallele the agent team would send log files chunks to the discord server for those Devops/Security team emmber having there an acces to it.
Also this is decided as later on prometheus will be plugged in to handle logs and this is an extra using AI agents that would be triggered by Devops/Security team to get report in Discord. And when the process starts it runs by itself even if user logs out as I will subprocess and the agent is running not dependent of `settings.py`.
I will see if I can make it `asynchronous` and also havea table in database that would write the outcome and date of launch and who launch the agents team. So that when Devops/Security team logs in again the webUI for that special route would show the database history of a certain number of lastes row of the db table.

### Logging Agent Now Works Fine 
With the implementation of Django view special for super_user to start the agent team we get the webui returning the status `error/success/running` 
depending on the where the task is at and if it fails or not thanks to the database record of those and the sdtout and stderr recorded to db.
This permits to have a table showing history of how many runs have been done and how long it took and who started those runs.
The agent is sending notification to discord on success with the advice on each log lines. And in the code there is a sleep time of `0.7` seconds to not get rate limited.
But here we could also implement a full local llm solution like `LMStudio` or `Ollama`

- for the asynchronous run ofit, we are not going to it now to passto next task and keep going and not add complexity.
But having talked with ChatGPT-4o, I got recommendation to run `Celery` queues and maybe use `Redis`. It is good idea but not now yet.
**GPT-4o Recommendation**
```markdown
- Recommendation
  If the current solution meets your needs for performance and scale, you can leave it as-is for now. However, consider this a temporary solution and plan for the following:

  - Load Testing:
    Simulate high usage and larger log datasets to see if the subprocess-based approach holds up under load.
  - Future-Proofing:
    As your project grows, plan to migrate to a task queue like Celery for better scalability, fault tolerance, and distributed execution.
  - Code Readiness:
    Design the code so the transition to Celery or another task queue would be smooth. For example, encapsulate the log analysis logic in a separate module or function.
```

**might need to implement a cronjob still that would delete all logs files for rotation as django rotate those files but create more files actually. so the past ones need to be deleted.**


# GUNICORN

### To know how many core the system has:
```bash
nproc --all
```

### To know workers limit capacity
```bash
ulimit -u
```
If too low can update config file directly: `/etc/security/limits.conf` OR use `ulimit`

### Formula used for `Gunicorn` Workers number setup
```bash
... --workers $((2 * $(nproc --all) + 1)) ...
```
By multiplying the number of CPU cores by 2, the formula accounts for a scenario where workers alternate between being active (CPU-bound) and waiting (I/O-bound).
Adding +1 for Additional Capacity:
The +1 ensures there is always one extra worker ready to handle a request when all other workers are busy.
This is particularly useful in cases where there are occasional spikes in traffic, preventing the application from queuing requests unnecessarily. (Chatte J'ai Pipi)

### How many workers for server running it all

Yes, in fact not only `gunicorn` is running in the server so we need to make sure every process has enough processor/memory to work smoothly... like a smoothy!


```bash
eg.:
Total CPU cores: 12 (from nproc --all).
Reserved cores: 2 (for Nginx, Prometheus, and OS).
Gunicorn workers:

workers = ((12 - 2) * 2) + 1 = 21
```
**Calculation estimation of workers needed for `gunicorn` CPU based**
`gunicorn` command would be to dynamically get that:
```bash
gunicorn --workers $((( $(nproc --all) - 2 ) * 2 + 1)) --bind unix:/path/to/gunicorn.sock <project>.wsgi:application
`:w!```
**Calculation estimation of worker needed for `gunicorn` MEmory based**
```bash
eg.:
Available RAM: 16 GB.
Reserved for other services: 4 GB.
Available for Gunicorn: 12 GB.
Memory per worker: 100 MB.
Max workers by memory:

workers = 12 GB / 100 MB = 120 workers
```

**Choose the smaller value between the CPU-based and memory-based calculations.**
**Also do not create the `.sock` file otherwise you will get an error `...sock is not a socket`. Just let gunicorn create it where it has been confirgured in the config servcie file**

**Start django server using gunicorn**
- have the `gunicorn.service` file located at : `/etc/systemd/system/gunicorn.service`
- then enable the service: `sudo systemctl daemon-reload && sudo systemctl enable gunicorn`
- then start the servcie:  `sudo systemctl start gunicorn`
- then if you change the config you need to reload and start service again: `sudo systemctl reload gunicorn && sudo systemctl start gunicorn`
- `gunicorn.service` config file content (can use formula for numebr of workers here we just use 3):
```bash
[Unit]
Description=gunicorn daemon
After=network.target

[Service]
User=creditizens
Group=creditizens
WorkingDirectory=/home/creditizens/djangochatAI/chatbotAI
ExecStart=/home/creditizens/djangochatAI/djangochatbotAI_venv/bin/gunicorn --workers 3 --bind unix:/home/creditizens/djangochatAI/chatbotAI/gunicorn/gunicorn.sock chatbotAI.wsgi:application

[Install]
WantedBy=multi-user.target
```
- can also start `Django` using `gunicorn` for debugging using the following command otherwise for production server use `systemd` with the config file `systemctl` enabled:
gunicorn -b 0.0.0.0:8000 chatbotAI.wsgi:application


# How to check from another server which ports are exposed from the server that we have setup

### **Remotely**
- nmap:
```bash
sudo apt update
sudo apt install nmap
# `-p` to scan the 65535 port (ALL) or adjust for port range
nmap -p 1-65535 SERVER_IP
# most common port scan only
nmap  SERVER_IP
```
- telnet:
```bash
sudo apt update
sudo apt install telnet
# eg. fro port 80
telnet SERVER_IP 80
```
- netcat
```bash
sudo apt update
sudo apt install netcat
# eg. for port 80 with option `-z`(no data sent), -v (verbose)
netcat -zv SERVER_IP 80
# eg. for mutiple ports
nc -zv SERVER_IP 1-1000
```
- curl
```bash
curl -I http://SERVER_IP
```

### **From the server itself**
```bash
sudo ufw status
sudo iptables -L -n -v
```

### Disable and reset ufw
- get rid of all rule
```bash
sudo ufw disable
sudo ufw reset
sudo ufw reload
sudo ufw status
```

### Nginx firewall rule setup
- if `Nginx Full` available (but should be normally)`:
  -  interactive mode (you provide password ont erminal:
     sudo ufw allow "Nginx Full"
  -  for headless script mode and using env var to pass in password use `S` flag
     subprocess.run(
       ["sudo", "-S", "ufw", "allow", "Nginx Full"],
       # just have env var set to pass the password in `f-string`
       input=f"{sudo_password}\n",
       text=True,
       check=True
     )

- if it is not available just set rules like that:
```bash
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp
```

# Next
Have setup a python script that will setup a full server. have tried all functions except the postgresql setup functions and th epython dependencies install one , so the first functions
All of the rest works fine and have variabilized those, meaning that centralized .env file will be the point to set all path and names and so on.
- Nginx setup almost still need to fix the static files rendering as runing `python3 manage.py collecstatic` does collec but nginx is not rendering the site properly... need to see if those need to be in a special folder as i use the project root directory from the user home at the moment. Need to check logs of `nginx` as maybe the user of nginx need permission on those.

- Gunicorn setup OK!
- [x] add logging to common app utility functions
- [x] run the django server with gunicorn until it works fine and then use the application and see if all works fine at minimum
- [x] setup nginx after gunicorn works
- [x] use the wsl part to test the postgresql setup functions and the python dependencies installl creating a virtual env that we are going to get rid of when it works and after come back here to validate that it works fine
- [x] fix nginx serving static files with correct permissions or copy those after a `collectstatic` to a folder where `nginx` or `www-data` user have permission.
- [x] update the `full_server setup` script with the correclt files as now the server works fine and nginx finds the static files correcly.
- [x] add logic to the script `full_server setup` to create right permissions and create the files and folders properly and to `reload-daemon` properly
- [x] do unit tests even if we don't want to do those, lets cover some percentage of the application using GPT or Gemini or Bolt.new/ottodev ....
- [] check that the github action works fine
- [] create container of app and also a docker-compose and see if it wokrs in local docker so that we can kubernetize it...
- [] then use this app for any devops workflow that we want to do (push enhancement of app and have the ci/cd work by itself and do all necessary notifications (Dicord: the webhook stuff is simple and works fine so we will be using that)

# Lessons From Error Setting Up Full Server
- need to set the upstream in nginx to point to gunicorn with the domain name and in the sevrers under at any location be proxy passing http://domain name..
- need to set permission on /run/gunicorn to the server user creditizens:creditizens
- for nginx access to static files make sure to not forget the `/` at he end of `../media/` and `../static/` path otherwise it will just `no such file in directory` error
- didn't need to change/set in nginx.conf the user from `www-data` to `creditizens` like in pdf_llm AI project previously while used doyble server behind ngins `sreamlit` and `django gunicorn`
- will get rid of the gunicorn service config that writes logs to file as django logging is already writing logs this would be just double logs so no need.

After that it worked perfectly!!!!

### Nginx config file to variablize:
```bash
### NGINX CONF
# Redirect HTTP traffic to HTTPS
upstream creditizens.local {
    server unix:/run/gunicorn/gunicorn.sock fail_timeout=0;
}

# to not display nginx server version in headers
server_tokens             off;

server {
  listen 80;
  server_name creditizens.local;

  # Redirect all HTTP requests to HTTPS
  return 301 https://$host$request_uri;
}
server {
  listen 443 ssl;
  server_name creditizens.local;

  ssl_certificate /etc/ssl/creditizens/creditizens.crt;
  ssl_certificate_key /etc/ssl/creditizens/creditizens.key;

  # General proxy settings
  proxy_http_version 1.1;
  proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
  proxy_set_header Host $host;
  proxy_set_header Upgrade $http_upgrade;
  proxy_set_header Connection "upgrade";
  proxy_read_timeout 86400;

  # if user file upload enabled this is for: file upload max size allowed
  #client_max_body_size 2000M;


  location /favicon.ico {
      access_log off;
      log_not_found off;
  }

  gzip on;
  gzip_types application/json text/css text/plain text/javascript application/javascript;
  gzip_proxied any;
  gzip_min_length 256;
  gzip_vary on;
  gunzip on;

  add_header Strict-Transport-Security "max-age=15768000; includeSubDomains; preload" always;
  add_header Referrer-Policy origin;
  add_header Permissions-Policy "geolocation=(),midi=(),sync-xhr=(),microphone=(),camera=(),fullscreen=(self),payment=()";
  add_header X-XSS-Protection "1; mode=block";
  add_header X-Frame-Options "SAMEORIGIN";
  add_header X-Content-Type-Options "nosniff";

  location / {
      # we are not using direct connection to Django server, Gunicorn handles it
      #proxy_pass http://localhost:8000/;
      # we are using gunicorn UNIX socket to point to Django server
      proxy_pass http://creditizens.local;
      proxy_set_header Host $host;
      proxy_set_header X-Real-IP $remote_addr;
      proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
      proxy_set_header X-Forwarded-Proto $scheme;
  }

  location /static/ {
      alias /var/www/static/;
      expires 30d;
      add_header Cache-Control "public, max-age=2592000";
  }

  location /media/ {
      alias /var/www/static/media/;
      expires 30d;
      add_header Cache-Control "public, max-age=2592000";
  }


  error_log /home/creditizens/djangochatAI/chatbotAI/logs/nginx_error.log;
  access_log /home/creditizens/djangochatAI/chatbotAI/logs/nginx_access.log;
}


```
### Gunicorn service to variablelize:
```bash
[Unit]
Description=gunicorn daemon
After=network.target

[Service]
User=creditizens
Group=creditizens
WorkingDirectory=/home/creditizens/djangochatAI/chatbotAI
ExecStart=/home/creditizens/djangochatAI/djangochatbotAI_venv/bin/gunicorn --workers 3 --bind unix:/run/gunicorn/gunicorn.sock chatbotAI.wsgi:application
# see doc for more:https://docs.gunicorn.org/en/stable/deploy.html#systemd
#Restart=on-failure
#ExecReload=/bin/kill -s HUP $MAINPID
#KillMode=mixed
#TimeoutStopSec=5

[Install]
WantedBy=multi-user.target

```
### can add this to `setting.py` to define site for django using the domain name:
```python
from django.contrib.sites.models import Site

def configure_site():
    site_id = 1  # Default site ID
    domain = "creditizens.local"
    name = "Creditizens"
    Site.objects.update_or_create(
        id=site_id,
        defaults={"domain": domain, "name": name}
    )

# Call the function when the app starts
configure_site()

```

# Check how many lines of code in the project
```bash
# install `nic`
sudo apt install cloc -y
# run
cloc .
# output:
'''
     368 text files.
     345 unique files.
      80 files ignored.

github.com/AlDanial/cloc v 1.90  T=0.25 s (1248.1 files/s, 211106.6 lines/s)
----------------+--------------+---------------+-------------+--------+
Language        | files        | blank         | comment     |  code  |
----------------+--------------+---------------+-------------+--------+
JavaScript      |  97          | 5091          | 4549        |  19661 |
CSS             |  25          | 1230          |  220        |   6675 |
Python          | 121          | 1526          | 2329        |   6046 | 
Markdown        |  17          |  396          |    0        |   2539 |
HTML            |  17          |   91          |   47        |   1085 | 
SVG             |  23          |    0          |    0        |    880 |
YAML            |   3          |   24          |   16        |    274 |
Rust            |   8          |   46          |   60        |    238 |
TOML            |   2          |    4          |    5        |     34 |
Dockerfile      |   1          |   13          |   11        |     20 |
----------------+--------------+-----------------------------+--------+
SUM:            | 314          | 8421          | 7237        |  37452 |
------------------------------+--------------+---------------+--------+
'''
```

# Purge openssl and do a fresh start as it is not standard
Got to install some torch libraries and other stuff for testing in my server, feel like it has messed up with openssl.
so the script should do fresh install of openssl for consistency purpose. 
As it worked before without any issues and now, I tested and it is not working anymore.

```bash
sudo apt purge openssl -y
sudo apt autoremove --purge -y
# Verify OpenSSL is Removed
which openssl
# If a path is returned, it means there’s another OpenSSL binary on your system. Locate it with:
sudo find / -iname openssl
# Manually delete any leftover OpenSSL-related binaries or files if necessary.

### Reinstall OpenSSL
sudo apt update
sudo apt install openssl -y
# Check the Installation. The default configuration file should be located at /etc/ssl/openssl.cnf.
openssl version -a
# Verify Default OpenSSL Configuration File
ls -l /etc/ssl/openssl.cnf
# If the file is missing or corrupt, reinstall the ca-certificates package, which ensures the correct configuration:
sudo apt install --reinstall ca-certificates
sudo apt update
# Recreate Symbolic Links
sudo ln -sf /etc/ssl/openssl.cnf /usr/lib/ssl/openssl.cnf
# Test OpenSSL
openssl req -x509 -newkey rsa:2048 -keyout test.key -out test.crt -days 365 -nodes

# **Unit Tests Better With `ChatGPT4o`**
Will continue to work on those unit test with `ChatGPT4o` as the `gemini-2.0-flash-exp` is a bit tired...
```bash
coverage run --source='.' -m pytest --ds=chatbotAI.settings --cache-clear
================================================================= test session starts ==================================================================
platform linux -- Python 3.12.7, pytest-8.3.3, pluggy-1.5.0
django: version: 5.1.3, settings: chatbotAI.settings (from option)
rootdir: /home/creditizens/aider_assistant/aider_working_project_dir
plugins: django-4.9.0, anyio-4.7.0
collected 31 items                                                                                                                                     

tests/agents/test_ai_personality.py ...                                                                                                          [  9%]
tests/agents/test_beautiful_graph_output.py ...                                                                                                  [ 19%]
tests/agents/test_call_llm.py ....                                                                                                               [ 32%]
tests/agents/test_delete_embeddings.py ..                                                                                                        [ 38%]
tests/agents/test_embed_data.py ..                                                                                                               [ 45%]
tests/agents/test_formatters.py ...                                                                                                              [ 54%]
tests/agents/test_json_dumps_manager.py ....                                                                                                     [ 67%]
tests/agents/test_prompt_creation.py ....                                                                                                        [ 80%]
tests/agents/test_retrieve_answer.py ....                                                                                                        [ 93%]
tests/agents/test_token_count_helper.py ..                                                                                                       [100%]

================================================================== 31 passed in 6.36s ===
```



# `AIDER` Unit Test Coder Assistnat
Using here `Architect` node in a `Python` script where the config files are used to have:
- `gemini` as Architect
- `cerebras llama3.3-7b` as secondary model
- `groq llama3.3-70b` as fallback separate config.

Need to install requirements and for the `rust_lib` need to `cd` in the folder and run `maturin` develop tobuild all `PYo3` dependencies.
(`have commented out the line form requirements.txt that is trying to build rust from github links as it fails everytimes. so it will be a two step. `)
- 2 steps are therefore:
  - `pip install -r requirements.txt` # this will install `maturin` and the rest
  - `cd rust_lib && maturin develop` # this will build `PYo3` rust libraries

Need also to do a `git init` in the root directory of the project for `aider` to commit there and be aware of files and folders from there.
- run `git init`
- then start the script
```bash
python3 aider_assistant_unit_test_coder.py
```

# runnin aider command
```bash
aider --auto-commit --model gemini/gemini-2.0-flash-exp --architect --editor-model groq/deepseek-r1-distill-llama-70b
```
- use `/add` to add files to `aider` context
- use `/drop` to drop files from the context of `aider`
- use `/read-only`to put files as `read-only` to aider context so it doesn't chnage their content

- **Warning with `aider`**: be careful as even though we can control a bi the context and what is changed, 
    `aider` will always try to ask you to put a file in its context or try to ask you if it can change it,
     this is `Hallucination`. Just say `N` (no) and repeat your query.



### Running test command to target one test file or folder
```bash
# like in `Rust` `Pytest` is using `::` to reference the tree 
coverage run --source='.' -m pytest --ds=chatbotAI.settings --cache-clear tests/clientchat/test_views.py::TestClientUserChatView
```

- have done tests with chatGPT4o until it becomes weak and have been in Gemini and it could do it easily.
- so i will be keeping doing that to gain some time until au unit tests are done.

- if issue with `coverage report`, run `coverage erase` and rerun `coverage run --source='.' -m pytest --ds=chatbotAI.settings` and then you will be able to get report by running `coverage report`
```bash
# create a coverage config file
nano .coveragerc
[run]
source = .
omit =
    */tests/*
    */test/*
    */migrations/*
    manage.py
    full_server_setup.py
# then run
coverage erase
# rerun tests
coverage run --source='.' --omit="*/tests/*,*/test/*,*/migrations/*,manage.py,full_server_setup.py" -m pytest --ds=chatbotAI.settings
# save report
coverage report >> coverage_report.md
```

# Next
- [x] check that the github action works fine
- [] create container of app and also a docker-compose and see if it wokrs in local docker so that we can kubernetize it...
- [] then use this app for any devops workflow that we want to do (push enhancement of app and have the ci/cd work by itself and do all necessary notifications (Dicord: the webhook stuff is simple and works fine so we will be using that)


# Issue while doing unit tests
- `cleaned_data()` method used in `chatbotsettings/models.py` is not working and can't check for image doubles in database as it is only available for `forms.py` checks.
  As I have decided to do those checks at the models.py level when the `chatbot settings` are savedm I need to change it for a `.` notation to access image in database and check.
```python
# before:
# this will check that file doesn't exist already for the picture
def clean_avatar(self):
  avatar = self.cleaned_data.get('avatar')

  if avatar:
    # Check if there's an existing ChatBotSettings with the same avatar filename
    existing_avatar = ChatBotSettings.objects.filter(avatar=avatar.name).first()
    if existing_avatar:
      raise ValidationError("This image filename is already being used by another ChatBot. Please upload a unique image.")
return avatar # here we return avatar as it is a form.py `cleaned_data()` so we need the cleane `avatar`	  
```
- so use :
```python
def clean_avatar(self):
  """Ensure avatar filename uniqueness within ChatBotSettings."""
  if self.avatar:
    # Check if an existing ChatBotSettings has the same avatar filename
    existing_avatar = ChatBotSettings.objects.filter(avatar=self.avatar.name).exclude(id=self.id).first()
    if existing_avatar:
      raise ValidationError("This image filename is already being used by another ChatBot. Please upload a unique image.")
# Here no return needed as it is a `models.py` check not like in forms.py when we need the value to save it after check
```
- Error not getting mocks work:
```bash
# dont forget to install `pytest-mock`
pip install pytest-mock
```

# command to get coverage report in markdown, i=omitting the files that we are not going to test
```bash
coverage report --format=markdown --omit=log_analysis_center/*,users/serializers.py,chatbotAI/asgi.py,chatbotAI/wsgi.py,agents/graph/*
```

# this is the `.coveragerc` coverage ignore file content and run the above command without --omit after having run the test again
```bash
[run]
source = .
omit =
    */tests/*
    */test/*
    */migrations/*
    manage.py
    full_server_setup.py
    log_analysis_center/*
    users/serializers.py
    chatbotAI/asgi.py
    chatbotAI/wsgi.py
    agents/graph/*
    __pycache__/
    *__init__.py

[report]
exclude_lines =
    pragma: no cover
    def __repr__
    if settings.DEBUG
    raise NotImplementedError
```

Excluded Code	                | Why?                                                         |
--------------------------------+--------------------------------------------------------------+
pragma: no cover	        | Explicitly marked lines to skip.                             |
def __repr__	                | String representations of models, not critical for coverage. |
if settings.DEBUG         	| Conditional code used only in debugging mode.                |
raise NotImplementedError	| Placeholder methods that are not meant to be executed.       |
--------------------------------+---------------------------------------------------------------

# Final coverage report:
| Name                                            |    Stmts |     Miss |   Cover |
|------------------------------------------------ | -------: | -------: | ------: |
| agents/admin.py                                 |        3 |        0 |    100% |
| agents/app\_utils/ai\_personality.py            |       32 |       17 |     47% |
| agents/app\_utils/beautiful\_graph\_output.py   |       17 |        3 |     82% |
| agents/app\_utils/call\_llm.py                  |       41 |       14 |     66% |
| agents/app\_utils/delete\_embeddings.py         |       11 |        0 |    100% |
| agents/app\_utils/embed\_data.py                |       37 |        0 |    100% |
| agents/app\_utils/formatters.py                 |       20 |        1 |     95% |
| agents/app\_utils/json\_dumps\_manager.py       |        8 |        0 |    100% |
| agents/app\_utils/prompt\_creation.py           |       10 |        0 |    100% |
| agents/app\_utils/retrieve\_answer.py           |      114 |       38 |     67% |
| agents/app\_utils/token\_count\_helper.py       |       11 |        0 |    100% |
| agents/apps.py                                  |        4 |        0 |    100% |
| agents/llms/llms.py                             |       11 |        0 |    100% |
| agents/models.py                                |        4 |        0 |    100% |
| agents/prompts/prompts.py                       |        9 |        0 |    100% |
| agents/structured\_output/structured\_output.py |        6 |        0 |    100% |
| agents/tools/tools.py                           |       56 |        5 |     91% |
| agents/urls.py                                  |        4 |        0 |    100% |
| agents/views.py                                 |      133 |       28 |     79% |
| businessdata/admin.py                           |        3 |        0 |    100% |
| businessdata/apps.py                            |        4 |        0 |    100% |
| businessdata/forms.py                           |       14 |        0 |    100% |
| businessdata/mixins.py                          |       14 |        0 |    100% |
| businessdata/models.py                          |       15 |        0 |    100% |
| businessdata/urls.py                            |        4 |        0 |    100% |
| businessdata/views.py                           |      172 |       67 |     61% |
| chatbotAI/settings.py                           |       30 |        0 |    100% |
| chatbotAI/urls.py                               |        5 |        0 |    100% |
| chatbotsettings/admin.py                        |        3 |        0 |    100% |
| chatbotsettings/apps.py                         |        4 |        0 |    100% |
| chatbotsettings/forms.py                        |       13 |        0 |    100% |
| chatbotsettings/models.py                       |       34 |       11 |     68% |
| chatbotsettings/urls.py                         |        4 |        0 |    100% |
| chatbotsettings/views.py                        |      103 |       73 |     29% |
| clientchat/admin.py                             |        3 |        0 |    100% |
| clientchat/apps.py                              |        4 |        0 |    100% |
| clientchat/forms.py                             |       10 |        0 |    100% |
| clientchat/models.py                            |       11 |        0 |    100% |
| clientchat/urls.py                              |        4 |        0 |    100% |
| clientchat/views.py                             |      159 |       37 |     77% |
| common/admin.py                                 |        3 |        0 |    100% |
| common/apps.py                                  |        4 |        0 |    100% |
| common/discord\_notifications.py                |       70 |       56 |     20% |
| common/logs\_filters.py                         |        7 |        0 |    100% |
| common/middleware\_logs\_custom.py              |       14 |        0 |    100% |
| common/models.py                                |        8 |        0 |    100% |
| common/record\_to\_db.py                        |       32 |        1 |     97% |
| common/templatetags/form\_tags.py               |       11 |        0 |    100% |
| common/urls.py                                  |        4 |        0 |    100% |
| common/views.py                                 |       57 |        0 |    100% |
| users/admin.py                                  |        3 |        0 |    100% |
| users/apps.py                                   |        4 |        0 |    100% |
| users/forms.py                                  |       62 |        1 |     98% |
| users/models.py                                 |       10 |        0 |    100% |
| users/urls.py                                   |        4 |        0 |    100% |
| users/views.py                                  |      155 |       40 |     74% |
|                                       **TOTAL** | **1592** |  **392** | **75%** |

__________________________________________________________________________________________________

# issues with `Githib actions`
Requirements.tt got a line to install the rust libraray that we have created using `PyO3` but it will fail as `pip` can build that.
Therefore we need to remove the line `-e git+https://github.com/Diallo75012/djangochatbotAI@55951cd92939a196c6bc6a6c08023063096cd065#egg=rust_lib&subdirectory=rust_lib`
after each `pip freeze > requirements.txt`
To install the `rust_lib` we need to:
```bash
# get all install including maturin
pip install -r requiremnts.txt
# go in the rust_lib
cb rust_lib
# compile the rust library into a Python one
maturin develop
```

# Isuues with `Github Action` secrets:
Had the rust PyO3 lib trying to pull some env vars but couldn't has have considered the entry in the env var files as not well formatted.
Initially i have just added the vars just as those are, but apparently the Rust dotenv is more strict than the Python one.
So i have just to go to that env var and add single qotes:
```bash
# Error
`❌ Rust function failed: Failed to load .env file from path '.vars.env': Error parsing line: 'What is Purikura Skin Effect?', error at line index: 5
=========================== short test summary info ============================
FAILED tests/agents/test_ai_personality.py::TestAIPersonality::test_personality_trait_formatting - AssertionError: Rust function failed unexpectedly: Failed to load .env file from path '.vars.env': Error parsing line: 'What is Purikura Skin Effect?', error at line index: 5
======================== 1 failed, 122 passed in 26.77s ========================
Error: Process completed with exit code 1`

# Fix
saved `What is Purikura Skin Effect?` with single quotes: `'What is Purikura Skin Effect?'`
might need to do it for all other vars, but there are so many that i didn;t do it. 
```

# Lesson
**JUST PUT ENV VAR BETWEEN QUOTES ALWAYS!** : as Rust interpreter might parse it at the space character is there is a sentence without quotes and consider the rest as malformation of the file

# Next
- [] create container of app and also a docker-compose and see if it wokrs in local docker so that we can kubernetize it...
- [] then use this app for any devops workflow that we want to do (push enhancement of app and have the ci/cd work by itself and do all necessary notifications (Discord: the webhook stuff is simple and works fine so we will be using that)


So now we need to check those `Dockerfiles` and `docker-compose` files created but the full server setup script and see if those work as it is through `docker`. Fix the errors, enhance the files until it works fine. Then we will consider that the app is `Kubernetizable` potentially. So don't forget to update those `Dockerfile` and `docker-compose` only through the script so the script will be creating what works formt he begin.

See if we can use `crictl` so `containerd` instead of `docker` as everything is moving away from it and be opensource.



# Git Credentials
- Enable credential caching to not have to authenticate everytime I push:
`git config --global credential.helper cache`
- Or use a credential store:
`git config --global credential.helper store`

# Docker Replacement
- will install containerd instead of `docker` to run containers
- will use `crictl` for commands instead of `docker`
- will use `nerdctl` for `docker-compose` support as `crictl` doesn't
- commands for `crictl` vs `docker`:
Docker Command		|crictl Equivalent
------------------------+-------------------------------
docker ps 		|crictl ps
docker images		|crictl images
docker pull nginx	|crictl pull docker.io/library/nginx
docker run -d nginx	|crictl run (requires a config file)
docker exec -it <id> sh	|crictl exec -it <id> sh
docker logs <id>	|crictl logs <id>

- commands for `nerdctl` vs `docker compose`:
Docker Command		|nerdctl Equivalent
------------------------+--------------------------------
docker run -d nginx	|nerdctl run -d nginx
docker ps		|nerdctl ps
docker images		|nerdctl images
docker-compose up -d	|nerdctl compose up -d

# using `nerdctl` to replace `docker` as it supports all docker commands
```bash
# compose
nerdctl compose up -d
# OR Dockerfile
nerdctl build -t django_app -f <dockerfile_name> .
# sudo nerdctl build -t django_app -f Dockerfile .
nerdctl run --rm --env-file .env -v "$(pwd)/.env:/app/.env" -p 8000:8000 django_app
# sudo nerdctl run --rm --env-file .env --env-file .vars.env -v "$(pwd)/.env:/home/creditizens/djangochatAI/chatbotAI/.env" -v "$(pwd)/.vars.env:/home/creditizens/djangochatAI/chatbotAI/.vars.env" -p 8000:8000 django_app

```
- info: `nerdctl` needs `buildkit` to be installed and `buildctl` service to be running. otherwhise you won't be able to build images
- info: I have put all in one script that will install `crictl`, `containerd`, `nerdctl`, `buildkit`, `buildctl`, `cni pluggins for networking` (otherwise can't run containers)
- create a `.dockerignore` file and put what we need to ignore..
