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
- then make those agents to interact with user
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
- then need to create new app for agents or have it in the `common` app as central point that all other apps can get agents from
- then implement embedding for business data when recorded by business user (Use Rust and LangGraph)
- then implement retrieval when user sends a message (Use Rust and LangGraph)
- then need to do all the unit tests (I want to cry! hihihihihiiii, ChatGPT Agent Will work with me to streamline this quicker/more productive)
- then make those agents to interact with user
- then add logging in the codebase
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


# Logging
eg.:
```python
import os
# we have the choice to use either of those two to have logs rotation
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
**Fetching Logs with Prometheus or Other Tools**
- Prometheus with Loki: Use Loki as a log aggregation tool. It works seamlessly with Prometheus.
  - Install promtail, a log collector, and point it to your log files.
  - Configure promtail to scrape the JSON logs from your Django project.

- ElasticSearch (ELK Stack):
  - Use Filebeat or Logstash to ship logs to ElasticSearch.
  - Parse the JSON logs for advanced search and filtering.

- AWS CloudWatch or GCP Logging:
  - Use SDKs or agents to push logs from your Django server to these managed log services.


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


# think at logging to file instead of printing everywhere
```python
import logging

# this for timestamps
logging.basicConfig(format='%(asctime)s %(message)s')
# this for the logginf message with the level of logging
logging.warning('is when this event was logged.') 

# need to do the configs better in settings.py
We have commented out advance logging settings and need to work on it
```


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
"Where to shop for Shibuya styles?": "109 Shibuya, Parco, and boutique shops in the area are hotspots for trendy fashion.",
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
- []  start implementing logging which is the next big step, decide on log format to be able to be consummed easily for me (custom), ELK, Prometheus and all their friends as well...

# Issue github push
```bash
warning: refname 'HEAD' is ambiguous.
warning: refname 'HEAD' is ambiguous.
warning: refname 'HEAD' is ambiguous.
```
deleted: `rm .git/refs/HEAD` being a double file pointing to HEAD
