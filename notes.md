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
- make the user client routes, templates, forms, views, models..
- fix issue with picture upload and see if is saved at location, then test deletion and see if function override works and actually delete the file and also make the field picture upload unique
- prepare user using the diagram to know how UI would look like and make logic for User Client/Buisiness Registration
- Have a set of numbers in a list that is like a number representing the business legal registration number, 
  , we could have also a system here that uses governmental API to check if business exist and other flags,
  here we are just making it simple to simulate only verified businesses registration allowed.
- Add this number to business model as field that cannot change and will be used also in the bot model so add a field to get that number set for the chatbot getting it from the business user field.

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

