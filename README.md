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


## Read Me From Here
A Django-powered, business-specific chatbot platform leveraging AI agents and retrieval-augmented generation (RAG)

**Table of Contents**
1. [Overview](#overview)
2. [Features](#features)
3. [Architecture](#architecture)
4. [Prerequisites & Dependencies](#prerequisites)
5. [Installation & Setup](#installs)
    - [Python & Virtual Environment Setup](#pythonvirtenv)
    - [PostgreSQL Installation & Configuration](#postgresql)
    - [Environment Files](#envfiles)
    - [Dependency Installation](#dependency)
    - [Rust Module Integration](#rustmodule)
6. [Local Development](#localdev)
7. [Deployment Options](#deployment)
    - [Full Server Setup](#fullserver)
    - [Containerized Deployment](#containerized)
8. [Configuration Details](#configuration)
    - [Caching with Memcached](#caching)
    - [Logging & Debugging](#logging)
9. [Testing & CI/CD](#testing)
10. [Future Enhancements](#future)
11. [Developer Notes](#notes)
12. [License]
13. [Contact]

## Overview <a name="overview"></a>
ChatBoTAI is designed to help businesses deploy a custom chatbot quickly and effectively. It fuses the general knowledge of large language models with business-specific Q&A data in JSON format, using retrieval-augmented generation for enhanced accuracy and efficiency. This hybrid approach minimizes complexity and cost while delivering tailored responses.

### Key Use Cases:

- Automating business-specific Q&A.
- Providing AI-driven, personalized client support.
- Seamlessly integrating domain-specific data with LLM capabilities.
- A high-level diagram (refer to Diagram V1 in the repository’s Excalidraw assets) illustrates the core components and data flows of the system.


## Features <a name="features"></a>
- Business-Specific Responses: Utilize custom JSON Q&A data to tailor chatbot responses.
- Retrieval-Augmented Generation: Dual-layer retrieval logic enhances answer accuracy.
- AI Agent Integration: Dynamically processes user queries using integrated AI agents.
- Rust Module Integration: Critical performance functions are optimized using Rust (via maturin and PyO3).
- Robust Django Backend: Fully powered by Django with support for Django REST Framework.
- Comprehensive Testing & Logging: Extensive unit tests, coverage reports, and detailed logging ensure reliability.


## Architecture <a name="architecture"></a>

### High-Level Overview:

- Data Embedding & Retrieval: Business data is embedded and indexed by document collections. Users select the relevant collection via a sidebar dropdown, and the chatbot adapts its settings accordingly.
- User Flow: The chatbot dynamically adjusts based on selected business data and associated configurations.
- Deployment Components: The design includes plans for using Gunicorn, Nginx, and container orchestration tools (Docker/nerdctl) in production environments.

A diagram in the repository (Diagram V1) visually represents the system’s architecture and interactions.


## Prerequisites & Dependencies <a name="prerequisites"></a>

### Software Requirements:

- Python 3.12: (Detailed installation and version-switching instructions provided below)
- PostgreSQL 17: (Includes purge/reinstall steps and configuration guidance)
- Memcached
- Rust: (along with maturin for Python integration)
- Optional: NodeJS (if additional frontend build tools are required)

### Environment Files:
.env and .vars.env contain necessary environment variables. Refer to the examples in the repository for full details.

- Python Packages:
  - Django, Django REST Framework, psycopg2/psycopg2-binary
  - Testing libraries: pytest, pytest-django, coverage
  - Others: markdown, django-filter, python-memcached


## Installation & Setup <a name="installs"></a>

### Python & Virtual Environment Setup <a name="pythonvirtenv"></a>
Install Python 3.12:
```bash
sudo apt install software-properties-common -y
sudo add-apt-repository ppa:deadsnakes/ppa -y
sudo apt update -y
sudo apt install python3.12 -y
sudo apt install curl -y
sudo apt install python3-pip -y
curl -sS https://bootstrap.pypa.io/get-pip.py | python3.12
```

Set Up Alternatives (if needed):
```bash
sudo cp /usr/bin/python3.12 /usr/local/bin/python3.12
sudo update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.10 1
sudo update-alternatives --install /usr/bin/python3 python3 /usr/local/bin/python3.12 2
sudo update-alternatives --config python3
```

Create & Activate a Virtual Environment:
```bash
python3.12 -m venv venv
source venv/bin/activate  # For Unix/MacOS
# For Windows: venv\Scripts\activate
```
Note: On Ubuntu 22, ensure the default Python3.10 installation remains undisturbed.

### PostgreSQL Installation & Configuration <a name="postgresql"></a>

Purge Existing Installations:

```bash
sudo apt purge postgresql* -y
sudo apt autoremove --purge -y
sudo rm -rf /etc/postgresql /var/lib/postgresql /var/log/postgresql
sudo rm -f /etc/apt/sources.list.d/pgdg.list
```

Add PostgreSQL Repository & Install PostgreSQL 17:

```bash
echo "deb [arch=amd64] http://apt.postgresql.org/pub/repos/apt $(lsb_release -cs)-pgdg main" | sudo tee /etc/apt/sources.list.d/pgdg.list
wget -qO - https://www.postgresql.org/media/keys/ACCC4CF8.asc | sudo apt-key add -
sudo apt update
sudo apt install postgresql-17 postgresql-contrib -y
```

Start & Enable PostgreSQL:

```bash
sudo systemctl start postgresql
sudo systemctl enable postgresql
psql --version  # Verify installation
```

Install psycopg2 dependencies:

```bash
sudo apt install -y build-essential python3.12-dev libpq-dev
pip install psycopg2-binary psycopg2
```

### Environment Files <a name="envfiles"></a>
Create two key configuration files in the project root:

.env

```ini
DEBUG=True
SECRET_KEY=your-secret-key
DATABASE_URL=postgres://user:password@localhost:5432/yourdb
CACHE_LOCATION=127.0.0.1:11211
```

.vars.env

```ini
VARIABLE_1=value1
VARIABLE_2=value2
```
Refer to the repository examples for complete details.

### Dependency Installation <a name="dependencies"></a>
Install the required Python packages:

```bash
pip install -r requirements.txt
# OR, if using chill_requirements.txt:
pip install -r chill_requirements.txt
```

Additionally, install:

```bash
pip install djangorestframework markdown django-filter
```

### Rust Module Integration <a name="rustmodule"></a>
Install Rust & maturin:

```bash
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh
rustc --version
pip install maturin
```

Create and Build the Rust Project:

```bash
maturin new --bindings pyo3 rust_lib
cd rust_lib
cargo add pyo3 --features "extension-module"
# Update pyproject.toml and Cargo.toml with dependencies (e.g., reqwest, serde)
maturin develop
```

Import and Test in Python:

```python
import rust_lib
# or from rust_lib import <function_name>
```
Tip: Use eprintln! for debug logging in Rust modules as println! might not display output when integrated with Python.


## Local Development <a name="localdev"></a>

Database Setup:

```bash
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
```

Run the Development Server:

```bash
python manage.py runserver
```

Testing:

Install testing libraries if not already done:

```bash
pip install pytest pytest-django coverage
```

Run tests and generate coverage reports:

```bash
coverage run --source='.' -m pytest --ds=chatbotAI.settings
coverage report
coverage html
```

API Testing with cURL:

```bash
curl -v -X POST http://127.0.0.1:8000/your_api_endpoint/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer yourtoken" \
  -d '{"key": "value"}'
```

## Deployment Options <a name="deployment"></a>

### Full Server Setup <a name="fullserver"></a>

Production Server Requirements:

- Gunicorn & Nginx:
Configure Gunicorn to serve your Django app and set up Nginx as a reverse proxy. (Self-signed certificates can be used initially for domains such as creditizens.local.)

- Bash Startup Scripts:
Include scripts to start the server, monitor logs, and handle service restarts.

- Manual Deployment:
Follow detailed step-by-step instructions for deploying on a dedicated production server.


### Containerized Deployment <a name="containerized"></a>

Docker Deployment (Planned):
Create a Dockerfile and optionally a Docker Compose file for containerizing the application.

- Containerd / nerdctl Deployment:
Follow provided instructions/scripts for deploying with containerd-based tools (e.g., nerdctl or nerdctl compose).


## Configuration Details

### Caching with Memcached <a name="caching"></a>
Install & Start Memcached:

```bash
sudo apt update
sudo apt install memcached
sudo systemctl start memcached
# Alternatively, run manually:
memcached -d -m 64 -l 127.0.0.1 -p 11211
```

Django Cache Configuration (in settings.py):

```python
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
        'LOCATION': '127.0.0.1:11211',
    }
}
```

### Logging & Debugging <a name="logging"></a>

- Logs Directory:
All logs are stored in the /logs folder.

- Rust Module Debugging:
Consult rust_debug.log for output from the Rust integration.

- CI/CD Logs:
GitHub Actions and supplementary scripts are used for automated log monitoring and analysis.


## Testing & CI/CD <a name="testing"></a>

- Test Coverage:
Aim for a minimum of 80% coverage with unit and integration tests covering views, URLs, forms, mixins, templates, and models.

- CI/CD Pipeline:
  - Configured via GitHub Actions (see .github/workflows).

Tip: To skip CI for a commit, include [skip ci] or [ci skip] in your commit message.

Generating Test Reports:
```bash
coverage html
```


## Future Enhancements <a name="future"></a>

- Feature Roadmap:
  - Finalize CRUD operations and refine UI/UX.
  - Expand AI agent functionality for real-time log analysis.
  - Infrastructure Upgrades:
  - Dockerization, Kubernetes orchestration, and Infrastructure as Code using Terraform/Ansible.
  - Advanced CI/CD integration with tools like SonarQube, Trivy, and ArgoCD.


## Developer Notes <a name="notes"></a>

- Personal Retrospection:
Refer to the personal_retrospection folder for insights on project improvements.

- Usage & Integration:
See notes.md for detailed instructions on installation, caching strategies, embedding/retrieval flows, and code references (e.g., cURL examples, JavaScript integration tips).

- Rust & Python:
Detailed explanations on the Rust module’s setup, dependency management, and troubleshooting are provided in the repository.


@Creditizens
