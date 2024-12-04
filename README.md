# ChatBoTAI 

## details
This repository is for Businesses which need to just enter a set of question/answer in JSON format and create a custom ChatBot.
Then Client can login and talk to that ChatBotAI which is using AI agents and RAG under the hood to answer to user with personality trait.

## Stack to install and have ready
Django
Memcache
Postgresql
LangChain
Rust

# install maturin and build the Rust module
(I use **python3.12.7** for the virtualenv)
```bash
pip install maturin
maturin develop
```
# install requirements
```bash
pip install -r chill_requirements.txt
OR
pip install -r requirements.txt
```

# make sure that's you have postgresql installed and have a .env file at the root directory with env vars (check /chatbotAI/settings.py)
```bash
# after having installed postgresql and created the user and the database,check that everything is running
sudo systemctl status postgresql
```
# make sure memcached is running
```bash
sudo systemctl start memcached
# OR manual start 
memcached -d -m 64 -l 127.0.0.1 -p 11211
```
# before starting, run migrations
```bash
python3 manage.py makemigrations
python3 manage.py migrate
```
# then create a superuser
```bash
python3 manage.py createsuperuser # and follow prompt
```
# then start the server
```bash
python3 manage.py runserver
```
# check routes available
```bash
127.0.0.1:8000/ # this will display error page with route available or dig in the code `urls.py` files
```


## Next
- [ ] Debug application boilerplate
- [ ] keep it pure Django/Jinja/Vanilla Javascript/CSS
- [ ] Continue coding and at each step make unit tests (github action already set but need updates along the way)
- [ ] Finish all CRUDs
- [ ] Make UI coherent (as it is still very messy)
- [ ] Create logs and plan how it going to be so that we can use Agent to analyze those in a predictable way
- [ ] Move cards on the Trello Board and adjust some cards as we have refactored the code to be full Django
- [ ] Create agents for ChatBot
- [ ] Create agent for app logs analysis
- [ ] Create Rust modules
- [ ] Create Gunicorn configs
- [ ] Create Nginx configs
- [ ] Create Bash script to start server
- [ ] Create Dockerfile of app (see if Docker-Compose or not)
- [ ] See if Langfuse can be added for Agent LLM logs UI interface
- [ ] and more...
