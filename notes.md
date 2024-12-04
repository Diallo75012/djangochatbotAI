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
- need to fix the logic and get those document_titles showing in the drop down as for the time being they are not
- need to go step by step, after that, need to have the chatbotsetting so informnation being displayed on the sidebar or if no chatbotsettings associated with the document_title have an empty form for user to customize chatbot, if user sends message without customization, we need to handle that in the backend with default value for chatbot more neutral
- need to have user message visible in the webui with picture next to it
- need to have response andswer just under it with chatbot avatar if any or a default one that will be stored in static files just in case
- then need to do all the unit tests
- then need to start pluggin in AI
- then make those agents to interact with user
- then add logging in the codebase
- then create the other asynchrone workflow with agents analyzing logs
- then replace caching with memecache isntead of native django cache or have that as fallback
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

