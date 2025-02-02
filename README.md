# ChatBoTAI 

### personal note:
I use ChatGPT as my tutor and superior who don't gatekeep information or how to do stuff.
Why?
- I believe that people who are nto using it the right way won't be needed in the workforce anymore.
- I believe that we shouldn't at this time end of 2024 expect it to build an entire app from few prompts
- I believe that we can talk with it to have optional solutions paths or views in order to decide quicker
- I believe we can use it to improve our understanding of what we would have `stackoverflowed...` in the past
- I believe that it can be used as well to make a profil of how we behaved in the project and help for retrospectives (projectwise and self ones)

This is why I have created a forlder personal_retrospective that would summarize in an objective way what should be improved and what are the strengths.
If you want to know me more about how I develop or think IT it is where you might want to go first.
I have pivoted to IT in 2018. I have entrepreneur mind and I am having fun!
I think in a very high `eagle` level to see everything from top as I believe that coming form other industries provide me an advantage to see problems and solutions in different way as usual. Even if I still need to learn. I believe that project management skills are top notch for future It workers if they want to stay in the field and not be eaten by AI.


## details
This repository is for Businesses which need to just enter a set of question/answer in JSON format and create a custom ChatBot.
Then Client can login and talk to that ChatBotAI which is using AI agents and RAG under the hood to answer to user with personality trait.

## Value Proposition of this project:

**Provide business-specific responses by retrieval.**
**Unlike traditional methods that train an LLM on domain-specific data,**
**my rely on the general knowledge of an LLM and supplement it with domain-specific answers.**
**This can indeed significantly reduce complexity and costs while providing high-quality, accurate responses.**

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

# To install the `rust_lib` we need to:
```bash
# get all install including maturin
pip install -r requiremnts.txt
# go in the rust_lib
cb rust_lib
# compile the rust library into a Python one
maturin develop
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
