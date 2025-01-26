# Developer Documentation 
Minimal dev documentation for the project made in collaboration with ChatGPT4o which has repeated some stuff but have covered some important parts of my notes.
## Python and Environment Setup

### Install Python 3.12
```bash
sudo apt install software-properties-common -y
sudo add-apt-repository ppa:deadsnakes/ppa -y
sudo apt update -y
sudo apt install python3.12 -y
```

### Install Pip
```bash
sudo apt install curl -y
sudo apt install python3-pip
curl -sS https://bootstrap.pypa.io/get-pip.py | python3.12
```

### Switch to Python 3.12
1. Create alternatives:
```bash
sudo cp /usr/bin/python3.12 /usr/local/bin/python3.12
sudo update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.10 1
sudo update-alternatives --install /usr/bin/python3 python3 /usr/local/bin/python3.12 2
```
2. Configure Python version:
```bash
sudo update-alternatives --config python3
```
3. Fix potential issues with `apt`:
```bash
ls /usr/lib/python3/dist-packages/apt_pkg*.so
# Example output: /usr/lib/python3/dist-packages/apt_pkg.cpython-310-x86_64-linux-gnu.so
cd /usr/lib/python3/dist-packages/
sudo ln -s apt_pkg.cpython-310-x86_64-linux-gnu.so apt_pkg.so
sudo apt-get update
sudo apt-get install --reinstall python3-apt
sudo apt update
```

### Install Virtual Environment for Python 3.12
```bash
sudo apt install python3.12-venv
```
**Note:** Avoid changing the default Python version on Ubuntu 22. Create virtual environments using:
```bash
python3.12 -m venv <name_of_env>
```
If terminal issues occur, access a headless terminal with `Ctrl + Alt + F3` to fix it.

---

## PostgreSQL Installation

### Fresh Installation
1. Remove any existing PostgreSQL installations:
```bash
sudo apt purge postgresql* -y
sudo apt autoremove --purge -y
sudo rm -rf /etc/postgresql /var/lib/postgresql /var/log/postgresql
sudo rm -f /etc/apt/sources.list.d/pgdg.list
```
2. Add PostgreSQL repository:
```bash
echo "deb [arch=amd64] http://apt.postgresql.org/pub/repos/apt $(lsb_release -cs)-pgdg main" | sudo tee /etc/apt/sources.list.d/pgdg.list
wget -qO - https://www.postgresql.org/media/keys/ACCC4CF8.asc | sudo apt-key add -
```
3. Install PostgreSQL 17:
```bash
sudo apt update
sudo apt install postgresql-17 postgresql-contrib -y
```
4. Start and enable PostgreSQL:
```bash
sudo systemctl start postgresql
sudo systemctl enable postgresql
```
5. Verify installation:
```bash
psql --version
```

### Install Psycopg2
Ensure you include the correct Python version for `python3.x-dev`:
```bash
sudo apt install -y build-essential python3.12-dev libpq-dev
pip install psycopg2-binary psycopg2
```

---

## Django Setup

### Install Django REST Framework
```bash
pip install djangorestframework markdown django-filter
```

### Running Tests
1. Install required packages:
```bash
pip install pytest pytest-django coverage
```
2. Run tests:
```bash
coverage run --source='.' -m pytest --ds=chatbotAI.settings
```
3. Generate reports:
```bash
coverage report
coverage html
```

### Next Steps
- **Achieve 80%+ test coverage.**
- Estimated test functions:
  - Views: 8-12 new tests.
  - URLs: 2-3 new tests.
  - Forms: 2-3 additional tests.
  - Mixins: 2-3 additional tests.
  - Template Tags: 1-2 new tests.
  - Models: 1-2 additional tests.

---

## GitHub Actions

### Skip CI for Specific Commits
Add the following to your commit message to skip CI:
```bash
[skip ci] or [ci skip]
```

---

## CURL Commands Reference

### GET and POST Requests
```bash
curl -X GET <URL>
curl -X POST <URL>
```

### Headers
```bash
-H "<header_key>: <header_value>"
```

### JSON Data
```bash
-d '<json_format_data>'
```

### Verbose Mode
```bash
-v
```

### Example
```bash
curl -v -X POST https://<your_url> -H "Content-Type: application/json" -H "Authorization: bearer <token>" -d '{"key": "value"}'
```

---

## Diagram V1: High-Level View
[Diagram V1: High-Level View of App](https://excalidraw.com/#json=13cims8czPh4dJf0H06YF,avcPyjTq6wk_9r3-E0tu1Q)

---

## ForeignKey `on_delete` Options
- `CASCADE`
- `PROTECT`
- `SET_NULL`
- `SET_DEFAULT`
- `SET()`
- `DO_NOTHING`

---

## Memcache for Question-Answer Caching

### Installation
```bash
sudo apt update
sudo apt install memcached
sudo systemctl start memcached
```

### Python Client
```bash
pip install python-memcached
```

### Django Configuration
Add the following to `settings.py`:
```python
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
        'LOCATION': '127.0.0.1:11211',
    }
}
```

### Example View
```python
from django.core.cache import cache

def my_view(request):
    cache_key = 'my_unique_key'
    cache_time = 86400  # Cache for 1 day
    data = cache.get(cache_key)
    if not data:
        data = expensive_function_call()
        cache.set(cache_key, data, cache_time)
    return JsonResponse(data, safe=False)
```

---

## Embedding and Retrieval Workflows

### Retrieval
1. Perform safety checks on the user query.
2. Retrieve answers from the database with thresholds.
3. If no data is retrieved:
   - Show sample questions from the database.
   - Optionally display a disclaimer.

### Embedding
1. Data entered by the business user is stored in the database.
2. Embedding documents are created based on database rows.
3. Metadata includes question-answer pairs and document titles.

### Test Command for Embedding Route
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

---

## JavaScript Best Practices

### Accessing Custom Data Attributes
#### HTML
```html
<span id="user-avatar" data-avatar-url="{{ user_avatar }}" hidden></span>
```

#### JavaScript
```javascript
const userAvatarUrl = document.getElementById('user-avatar').dataset.avatarUrl;
```

### Accessing Form and Text Values
```javascript
// Get form value
const value = document.getElementById('form-field').value;

// Get text content
const text = document.getElementById('html-tag').innerText;
```

---

## Python-Rust Interoperability

### Setting Up Rust Library
1. Install Rust and Maturin:
```bash
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh
pip install maturin
```
2. Create Rust Project:
```bash
maturin new --bindings pyo3 rust_lib
cd rust_lib
```
3. Build Rust Module:
```bash
maturin develop
```
4. Use in Python:
```python
import rust_lib
result = rust_lib.some_function()
```

---
# Deployment Documentation

## Deployment Checklist

### Preparing the Environment

1. **Update System Packages:**
   ```bash
   sudo apt update && sudo apt upgrade -y
   ```

2. **Install Required Tools:**
   Ensure essential tools such as Git, Docker, and Docker Compose are installed.
   ```bash
   sudo apt install git docker.io docker-compose -y
   ```

3. **Clone Repository:**
   ```bash
   git clone <repository_url>
   cd <repository_folder>
   ```

### Configure Environment Variables

1. **Create `.env` File:**
   Copy the provided `.env.example` file:
   ```bash
   cp .env.example .env
   ```

2. **Update `.env` Values:**
   Update the environment variables for your production settings, such as database credentials and API keys.

### Build and Run Containers

1. **Start Docker:**
   Ensure Docker service is running:
   ```bash
   sudo systemctl start docker
   ```

2. **Build and Deploy Containers:**
   ```bash
   docker-compose up --build -d
   ```

3. **Verify Deployment:**
   Check the status of running containers:
   ```bash
   docker ps
   ```

### Database Setup

1. **Run Migrations:**
   Inside the application container, run database migrations:
   ```bash
   docker exec -it <container_name> python manage.py migrate
   ```

2. **Create Superuser (Optional):**
   ```bash
   docker exec -it <container_name> python manage.py createsuperuser
   ```

### Static Files and Media

1. **Collect Static Files:**
   ```bash
   docker exec -it <container_name> python manage.py collectstatic --noinput
   ```

2. **Ensure Media Directory Permissions:**
   ```bash
   sudo chown -R www-data:www-data /path/to/media
   sudo chmod -R 755 /path/to/media
   ```

### Monitoring and Logs

1. **View Logs:**
   Use Docker logs to monitor the application:
   ```bash
   docker logs -f <container_name>
   ```

2. **Set Up Monitoring:**
   Configure tools like Prometheus, Grafana, or AWS CloudWatch for application monitoring.

### Health Check

1. **Verify Services:**
   Use curl or a browser to verify endpoints are accessible:
   ```bash
   curl http://localhost:8000/health/
   ```

2. **Debugging Errors:**
   Check logs and ensure configurations are correct.

### Deployment Best Practices

1. **Backup Strategy:**
   - Schedule periodic backups of the database.
   - Use cloud storage (e.g., AWS S3) for critical files.

2. **CI/CD Pipeline:**
   - Integrate GitHub Actions or similar tools for automated testing and deployment.

3. **Security Measures:**
   - Use HTTPS for all endpoints.
   - Regularly update dependencies.
   - Implement a Web Application Firewall (WAF).

---

## Troubleshooting

### Common Issues

1. **Container Not Starting:**
   - Check Docker Compose logs:
     ```bash
     docker-compose logs
     ```
   - Verify `.env` configurations.

2. **Database Connection Errors:**
   - Ensure the database container is running and accessible.
   - Verify database credentials in `.env`.

3. **Static Files Not Loading:**
   - Confirm `collectstatic` was run successfully.
   - Check web server configuration for static file handling.

### Contact Support

For further assistance, reach out to the development team with the following details:
- Log files
- Environment details
- Steps to reproduce the issue

---

## Deployment Checklist

### Pre-Deployment Steps

1. **Code Review**
   - Ensure all recent changes have been reviewed and approved.
   - Verify adherence to coding standards and guidelines.

2. **Unit Tests**
   - Run all unit tests using `pytest`.
   - Check for coverage using `coverage report`.
   - Aim for 80-90% code coverage, especially for critical paths.

3. **Integration Tests**
   - Execute integration tests to confirm components work together.
   - Address any detected failures or edge cases.

4. **Staging Environment**
   - Deploy code to the staging environment.
   - Verify the application works as expected.
   - Perform manual and automated testing in the staging environment.

5. **Documentation**
   - Ensure developer and user documentation is updated.
   - Review installation and setup guides for accuracy.

---

### Deployment Steps

1. **Backup Data**
   - Backup the production database.
   - Archive important server files or configurations.

2. **Update Dependencies**
   - Use `pip list --outdated` to identify outdated packages.
   - Update dependencies using `pip install -r requirements.txt`.
   - Check for compatibility issues with the updated versions.

3. **Migrations**
   - Apply database migrations using:
     ```bash
     python manage.py makemigrations
     python manage.py migrate
     ```
   - Verify migrations were applied successfully.

4. **Restart Services**
   - Restart application services (e.g., Gunicorn, Nginx):
     ```bash
     sudo systemctl restart gunicorn
     sudo systemctl restart nginx
     ```

5. **Verify Deployment**
   - Perform smoke testing to validate key features.
   - Monitor logs for errors or warnings:
     ```bash
     sudo journalctl -u gunicorn
     sudo journalctl -u nginx
     ```

---

### Post-Deployment Steps

1. **Performance Monitoring**
   - Use monitoring tools (e.g., AWS CloudWatch, New Relic) to observe application performance.
   - Set up alerts for error rates or performance degradation.

2. **Bug Fixes**
   - Address any reported issues or bugs promptly.
   - Document fixes for future reference.

3. **Team Feedback**
   - Collect feedback from the development and QA teams.
   - Note suggestions for improving the deployment process.

4. **Update Versioning**
   - Update the version in `settings.py` or a dedicated `version.py` file.
   - Tag the release in Git:
     ```bash
     git tag -a vX.Y.Z -m "Release notes"
     git push origin vX.Y.Z
     ```

---

### Troubleshooting Common Issues

1. **Application Not Starting**
   - Check for syntax errors in configuration files.
   - Review logs:
     ```bash
     sudo journalctl -u <service_name>
     ```

2. **Database Connection Errors**
   - Verify database credentials in `settings.py`.
   - Test connection using:
     ```bash
     psql -h <host> -U <username> -d <database>
     ```

3. **Static Files Not Loading**
   - Collect static files:
     ```bash
     python manage.py collectstatic
     ```
   - Check Nginx configuration for static file handling.

4. **High Latency**
   - Use tools like `htop` to identify server resource bottlenecks.
   - Review database queries for inefficiencies.

---

### Security Checklist

1. **Environment Variables**
   - Ensure sensitive information is stored securely using `.env` files.

2. **Firewall Rules**
   - Restrict access to sensitive ports.
   - Use security groups to control traffic.

3. **SSL Configuration**
   - Verify SSL/TLS certificates are valid and up-to-date.

4. **Regular Audits**
   - Conduct periodic security audits.
   - Address vulnerabilities promptly.

---

### Rollback Plan

1. **Identify Issues**
   - Monitor for errors or feedback after deployment.

2. **Revert Code**
   - Use Git to revert to the last stable release:
     ```bash
     git checkout <last_stable_commit>
     ```
   - Redeploy the reverted codebase.

3. **Database Restore**
   - Restore the database from the backup if schema changes cause issues.

4. **Inform Stakeholders**
   - Notify stakeholders about the rollback and expected downtime.

---

---

## Docker and Containerization Workflow

### Setting Up Docker

1. **Install Docker**
   ```bash
   sudo apt update
   sudo apt install -y docker.io
   sudo systemctl start docker
   sudo systemctl enable docker
   ```

2. **Verify Installation**
   ```bash
   docker --version
   ```

3. **Manage Docker as Non-root User**
   ```bash
   sudo usermod -aG docker $USER
   newgrp docker
   ```

### Docker Compose Installation

1. **Install Docker Compose**
   ```bash
   sudo curl -L "https://github.com/docker/compose/releases/download/v2.5.0/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
   sudo chmod +x /usr/local/bin/docker-compose
   ```

2. **Verify Installation**
   ```bash
   docker-compose --version
   ```

### Writing a Dockerfile

1. **Base Image**
   Use an official Python base image:
   ```Dockerfile
   FROM python:3.12-slim
   ```

2. **Working Directory**
   Set the working directory in the container:
   ```Dockerfile
   WORKDIR /app
   ```

3. **Dependencies**
   Copy `requirements.txt` and install dependencies:
   ```Dockerfile
   COPY requirements.txt requirements.txt
   RUN pip install --no-cache-dir -r requirements.txt
   ```

4. **Application Code**
   Copy the application code:
   ```Dockerfile
   COPY . .
   ```

5. **Command**
   Specify the default command to run the application:
   ```Dockerfile
   CMD ["gunicorn", "app.wsgi:application", "--bind", "0.0.0.0:8000"]
   ```

### Docker Compose File

1. **Create `docker-compose.yml`**
   ```yaml
   version: '3.8'

   services:
     app:
       build: .
       ports:
         - "8000:8000"
       volumes:
         - .:/app
       environment:
         - DEBUG=True
       depends_on:
         - db

     db:
       image: postgres:17
       environment:
         POSTGRES_USER: user
         POSTGRES_PASSWORD: password
         POSTGRES_DB: app_db
       ports:
         - "5432:5432"
   ```

2. **Run Containers**
   ```bash
   docker-compose up --build
   ```

3. **Stop and Remove Containers**
   ```bash
   docker-compose down
   ```

---

## Code Quality Tools Integration

### Linting with Flake8
1. **Install Flake8**
   ```bash
   pip install flake8
   ```
2. **Run Flake8**
   ```bash
   flake8 <directory_or_file>
   ```

### Code Formatting with Black
1. **Install Black**
   ```bash
   pip install black
   ```
2. **Format Code**
   ```bash
   black <directory_or_file>
   ```

### Type Checking with MyPy
1. **Install MyPy**
   ```bash
   pip install mypy
   ```
2. **Run MyPy**
   ```bash
   mypy <directory_or_file>
   ```

---

## ArgoCD Setup

### Installation

1. **Install ArgoCD CLI**
   ```bash
   curl -sSL -o argocd https://github.com/argoproj/argo-cd/releases/download/v2.7.1/argocd-linux-amd64
   chmod +x argocd
   sudo mv argocd /usr/local/bin/
   ```

2. **Install ArgoCD in Kubernetes**
   ```bash
   kubectl create namespace argocd
   kubectl apply -n argocd -f https://raw.githubusercontent.com/argoproj/argo-cd/stable/manifests/install.yaml
   ```

3. **Access ArgoCD**
   - Port-forward the ArgoCD server:
     ```bash
     kubectl port-forward svc/argocd-server -n argocd 8080:443
     ```
   - Access it at `https://localhost:8080`.

4. **Login to ArgoCD**
   ```bash
   argocd login localhost:8080
   ```

5. **Change Default Password**
   ```bash
   argocd account update-password
   ```

### Create an Application
```bash
argocd app create <app-name> \
--repo <repo-url> \
--path <path-to-manifests> \
--dest-server https://kubernetes.default.svc \
--dest-namespace <namespace>
```

---

## Automated Deployment Pipeline

### Pipeline Overview
1. **Stages:**
   - Code Checkout
   - Build Docker Image
   - Push Image to Registry
   - Deploy to Staging
   - Run Tests
   - Deploy to Production

2. **CI/CD Tools:**
   - GitHub Actions
   - Docker Hub/AWS ECR
   - ArgoCD

### Sample GitHub Actions Workflow

```yaml
name: CI/CD Pipeline

on:
  push:
    branches:
      - main

jobs:
  build:
    runs-on: ubuntu-latest

    steps:
      - name: Checkout Code
        uses: actions/checkout@v3

      - name: Log in to Docker Hub
        run: echo "${{ secrets.DOCKER_PASSWORD }}" | docker login -u "${{ secrets.DOCKER_USERNAME }}" --password-stdin

      - name: Build and Push Docker Image
        run: |
          docker build -t <image-name>:latest .
          docker tag <image-name>:latest <docker-repo>/<image-name>:latest
          docker push <docker-repo>/<image-name>:latest

      - name: Deploy to Staging
        run: |
          kubectl apply -f deployment.yaml

      - name: Trigger ArgoCD Sync
        run: |
          argocd app sync <app-name>
```

---

---

## Automated Deployment Pipeline

### Pipeline Overview

1. **Stages:**
   - **Code Checkout:** Pull the latest changes from the repository.
   - **Build Docker Image:** Create Docker images for the application.
   - **Push Image to Registry:** Upload Docker images to Docker Hub or AWS ECR.
   - **Deploy to Staging:** Apply Kubernetes manifests for the staging environment.
   - **Run Tests:** Execute automated tests to verify application functionality.
   - **Deploy to Production:** Deploy the application to the production environment after successful tests.

2. **CI/CD Tools:**
   - **Version Control:** GitHub/GitLab
   - **Build Tools:** GitHub Actions or Jenkins
   - **Container Registry:** Docker Hub or AWS ECR
   - **Orchestration:** Kubernetes with ArgoCD

### GitHub Actions Workflow Example

```yaml
name: CI/CD Pipeline

on:
  push:
    branches:
      - main

jobs:
  build-and-deploy:
    runs-on: ubuntu-latest

    steps:
      - name: Checkout Code
        uses: actions/checkout@v3

      - name: Set up Docker
        uses: docker/setup-buildx-action@v2

      - name: Log in to Docker Hub
        run: echo "${{ secrets.DOCKER_PASSWORD }}" | docker login -u "${{ secrets.DOCKER_USERNAME }}" --password-stdin

      - name: Build and Push Docker Image
        run: |
          docker build -t <image-name>:latest .
          docker tag <image-name>:latest <docker-repo>/<image-name>:latest
          docker push <docker-repo>/<image-name>:latest

      - name: Deploy to Staging
        run: |
          kubectl apply -f k8s/staging-deployment.yaml

      - name: Run Tests
        run: pytest --junitxml=results.xml

      - name: Deploy to Production
        if: success()
        run: |
          kubectl apply -f k8s/production-deployment.yaml

      - name: Trigger ArgoCD Sync
        run: |
          argocd app sync <app-name>
```

---

## Cost Monitoring and Optimization

### Tools for Cost Management

1. **AWS Cost Explorer:** Visualize and manage AWS service costs.
2. **CloudWatch:** Monitor and set alarms for excessive resource usage.
3. **KubeCost:** Track Kubernetes costs in real-time.
4. **Grafana:** Create dashboards for cost monitoring.

### Optimization Techniques

1. **Resource Allocation:**
   - Use **Resource Requests and Limits** in Kubernetes to avoid over-provisioning.
   ```yaml
   resources:
     requests:
       memory: "512Mi"
       cpu: "500m"
     limits:
       memory: "1Gi"
       cpu: "1"
   ```

2. **Spot Instances:** Use AWS Spot Instances for non-critical workloads to save costs.
3. **Scheduled Scaling:**
   - Scale resources during off-peak hours:
     ```yaml
     kind: HorizontalPodAutoscaler
     apiVersion: autoscaling/v2beta2
     spec:
       scaleTargetRef:
         apiVersion: apps/v1
         kind: Deployment
         name: app
       minReplicas: 1
       maxReplicas: 5
       metrics:
         - type: Resource
           resource:
             name: cpu
             target:
               type: Utilization
               averageUtilization: 70
     ```

---

## User Authentication and Authorization

### Authentication

1. **Django Rest Framework (DRF) Token Authentication:**
   ```bash
   pip install djangorestframework-simplejwt
   ```

2. **Configuring JWT in `settings.py`:**
   ```python
   REST_FRAMEWORK = {
       'DEFAULT_AUTHENTICATION_CLASSES': (
           'rest_framework_simplejwt.authentication.JWTAuthentication',
       ),
   }
   ```

3. **Generate Tokens:**
   ```bash
   curl -X POST http://127.0.0.1:8000/api/token/ -d '{"username": "<username>", "password": "<password>"}'
   ```

### Authorization

1. **DRF Permissions:**
   - Example using `IsAuthenticated`:
     ```python
     from rest_framework.permissions import IsAuthenticated

     class MyView(APIView):
         permission_classes = [IsAuthenticated]

         def get(self, request):
             return Response({"message": "Welcome!"})
     ```

2. **Custom Permissions:**
   ```python
   from rest_framework.permissions import BasePermission

   class IsAdminUser(BasePermission):
       def has_permission(self, request, view):
           return request.user and request.user.is_staff
   ```

---

## API Rate Limiting and Throttling

### Configuring Throttling in DRF

1. **Add Throttling Classes in `settings.py`:**
   ```python
   REST_FRAMEWORK = {
       'DEFAULT_THROTTLE_CLASSES': [
           'rest_framework.throttling.AnonRateThrottle',
           'rest_framework.throttling.UserRateThrottle',
       ],
       'DEFAULT_THROTTLE_RATES': {
           'anon': '100/day',
           'user': '1000/day',
       },
   }
   ```

2. **Custom Throttling:**
   ```python
   from rest_framework.throttling import SimpleRateThrottle

   class CustomRateThrottle(SimpleRateThrottle):
       scope = 'custom'

       def get_cache_key(self, request, view):
           if not request.user.is_authenticated:
               return None
           return self.cache_format % {
               'scope': self.scope,
               'ident': request.user.username,
           }
   ```

---

## Advanced Logging and Monitoring

### Centralized Logging with ELK Stack

1. **Install Elasticsearch, Logstash, and Kibana:**
   ```bash
   sudo apt install elasticsearch logstash kibana
   ```

2. **Configure Logstash to Ingest Logs:**
   ```bash
   input {
       file {
           path => "/var/log/app.log"
           start_position => "beginning"
       }
   }

   output {
       elasticsearch {
           hosts => ["localhost:9200"]
       }
   }
   ```

3. **Visualize Logs in Kibana:** Access `http://localhost:5601`.

### Metrics Monitoring with Prometheus and Grafana

1. **Install Prometheus and Grafana:**
   ```bash
   sudo apt install prometheus grafana
   ```

2. **Configure Prometheus:**
   ```yaml
   scrape_configs:
     - job_name: 'app'
       static_configs:
         - targets: ['localhost:8000']
   ```

3. **Visualize Metrics in Grafana:** Access `http://localhost:3000`.

### Application-Level Logging

1. **Configure Logging in Django:**
   ```python
   LOGGING = {
       'version': 1,
       'disable_existing_loggers': False,
       'handlers': {
           'file': {
               'level': 'DEBUG',
               'class': 'logging.FileHandler',
               'filename': '/var/log/app.log',
           },
       },
       'loggers': {
           'django': {
               'handlers': ['file'],
               'level': 'DEBUG',
               'propagate': True,
           },
       },
   }
   ```

---

## Database Optimization

### Indexing Strategies
1. **Primary Keys and Foreign Keys**:
   - Ensure all tables have appropriate primary keys.
   - Add indexes to foreign key columns to optimize joins.

2. **Composite Indexes**:
   - Use composite indexes for queries that filter or sort by multiple columns.
   - Example:
     ```sql
     CREATE INDEX idx_user_activity ON user_activity (user_id, activity_date);
     ```

3. **Covering Indexes**:
   - Use covering indexes to store all necessary query columns in the index.
   - Example:
     ```sql
     CREATE INDEX idx_order_summary ON orders (order_date, total_amount);
     ```

### Query Optimization
1. **Analyze Query Plans**:
   - Use `EXPLAIN` or `EXPLAIN ANALYZE` to inspect query execution plans.
   - Identify and resolve full table scans.

2. **Avoid SELECT***:
   - Always specify required columns in `SELECT` statements to reduce I/O.

3. **Partitioning**:
   - Use table partitioning for large datasets based on range, hash, or list.
   - Example:
     ```sql
     CREATE TABLE orders_2024 PARTITION OF orders FOR VALUES FROM ('2024-01-01') TO ('2024-12-31');
     ```

4. **Materialized Views**:
   - Use materialized views for frequently accessed aggregate data.
   - Example:
     ```sql
     CREATE MATERIALIZED VIEW sales_summary AS
     SELECT product_id, SUM(amount) AS total_sales
     FROM sales
     GROUP BY product_id;
     ```

---

## Backup and Disaster Recovery Plan

### Backup Strategies
1. **Regular Backups**:
   - Perform daily full backups and hourly incremental backups.
   - Use `pg_dump` for logical backups and `pg_basebackup` for physical backups.

2. **Automated Backup Scripts**:
   ```bash
   #!/bin/bash
   TIMESTAMP=$(date +"%Y%m%d%H%M%S")
   pg_dump -U postgres -d mydatabase -F c -f /backups/db_$TIMESTAMP.backup
   ```

3. **Cloud Backup Integration**:
   - Use AWS S3, GCP Storage, or Azure Blob Storage for offsite backups.
   - Example AWS CLI command:
     ```bash
     aws s3 cp /backups/db_$TIMESTAMP.backup s3://my-backup-bucket/
     ```

### Disaster Recovery Plan
1. **Recovery Objectives**:
   - **RTO (Recovery Time Objective):** 2 hours.
   - **RPO (Recovery Point Objective):** 15 minutes.

2. **Failover and Replication**:
   - Set up PostgreSQL streaming replication or a cloud-managed replica.

3. **Testing Recovery**:
   - Perform quarterly disaster recovery drills.
   - Validate data integrity and application functionality after recovery.

---

## Testing Strategies

### Unit Testing
1. **Focus Areas**:
   - Test individual functions and methods.
   - Mock external dependencies.

2. **Tools**:
   - `pytest` for Python.
   - Example:
     ```python
     def test_addition():
         assert add(2, 3) == 5
     ```

### Integration Testing
1. **Test Scenarios**:
   - Validate interaction between modules (e.g., API and database).

2. **Database Setup**:
   - Use an in-memory SQLite database or a dedicated test database.
   
3. **Example**:
   ```python
   def test_api_integration(client):
       response = client.get('/api/v1/resource/')
       assert response.status_code == 200
   ```

### End-to-End Testing
1. **Test Coverage**:
   - Simulate real user workflows.

2. **Tools**:
   - Selenium for UI tests.
   - Playwright for modern web apps.

### Code Coverage
- Target 80–90% coverage.
- Use `coverage.py` to measure test coverage.

---

## Scaling Strategy

### Horizontal Scaling
1. **Load Balancers**:
   - Use Nginx or AWS ALB to distribute traffic across multiple instances.

2. **Database Sharding**:
   - Partition the database by user ID or region.

3. **Container Orchestration**:
   - Deploy applications using Kubernetes for efficient scaling.

### Vertical Scaling
1. **Resource Allocation**:
   - Increase instance size (CPU, memory) for database and application servers.

2. **Caching**:
   - Use Redis or Memcached to reduce database load.

### Auto-Scaling
1. **Application Scaling**:
   - Configure auto-scaling groups in AWS or GCP.

2. **Database Scaling**:
   - Use managed services like AWS Aurora for read replicas and storage scaling.

---

## Business Continuity Plan

### Risk Assessment
1. **Identify Critical Systems**:
   - List essential applications, databases, and APIs.

2. **Threat Analysis**:
   - Assess risks like power outages, cyber-attacks, and hardware failures.

### Business Impact Analysis
1. **Downtime Cost Analysis**:
   - Calculate revenue loss and operational impact per hour of downtime.

2. **Recovery Prioritization**:
   - Rank systems based on criticality.

### Continuity Strategies
1. **Redundant Infrastructure**:
   - Use multi-region deployments for high availability.

2. **Regular Testing**:
   - Perform annual business continuity drills.

3. **Incident Response Plan**:
   - Maintain an up-to-date incident response playbook.

### Communication Plan
1. **Stakeholder Notification**:
   - Define roles for incident communication.

2. **Status Updates**:
   - Use tools like Slack or PagerDuty for real-time updates.

---

---

## Supplemental Developer Notes

These notes serve as additional information, lessons, retrospections, and resolved issues derived from the `notes.md` file to complement the main developer documentation.

---

### ForeignKey `on_delete` Options

When defining `ForeignKey` relationships in Django models, the `on_delete` behavior determines what happens when the referenced object is deleted. Below are the available options:

1. **CASCADE**: Deletes the related object as well.
   ```python
   models.ForeignKey(OtherModel, on_delete=models.CASCADE)
   ```

2. **PROTECT**: Prevents deletion of the referenced object if it is related.
   ```python
   models.ForeignKey(OtherModel, on_delete=models.PROTECT)
   ```

3. **SET_NULL**: Sets the foreign key to `NULL` if the referenced object is deleted (requires `null=True`).
   ```python
   models.ForeignKey(OtherModel, on_delete=models.SET_NULL, null=True)
   ```

4. **SET_DEFAULT**: Sets the foreign key to a default value.
   ```python
   models.ForeignKey(OtherModel, on_delete=models.SET_DEFAULT, default=<value>)
   ```

5. **SET()**: Sets the foreign key to a callable value.
   ```python
   models.ForeignKey(OtherModel, on_delete=models.SET(some_callable))
   ```

6. **DO_NOTHING**: Takes no action. Use cautiously as it can lead to database integrity issues.
   ```python
   models.ForeignKey(OtherModel, on_delete=models.DO_NOTHING)
   ```

---

### Embedding and Retrieval Workflows

#### Retrieval Workflow
1. **Perform Safety Checks:** Validate user queries to ensure they meet business or security standards.
2. **Retrieve Data:** Query the database with thresholds to filter results.
3. **Fallback Options:**
   - Provide sample questions if no data is found.
   - Display a disclaimer to the user if necessary.

#### Embedding Workflow
1. **Data Input:** Business users input question-answer pairs and document titles.
2. **Store in Database:** Data is saved in a structured format.
3. **Create Embeddings:** Generate embeddings from database rows using predefined models.
4. **Include Metadata:** Metadata includes document titles and Q&A pairs.

---

### Curl Commands and Examples

**General Commands:**
- **GET Request:**
  ```bash
  curl -X GET <URL>
  ```
- **POST Request:**
  ```bash
  curl -X POST <URL>
  ```
- **Headers:**
  ```bash
  -H "<header_key>: <header_value>"
  ```
- **JSON Data:**
  ```bash
  -d '<json_format_data>'
  ```
- **Verbose Mode:**
  ```bash
  -v
  ```

**Example Command:**
```bash
curl -v -X POST https://<your_url> \
-H "Content-Type: application/json" \
-H "Authorization: bearer <token>" \
-d '{"key": "value"}'
```

---

### JavaScript Best Practices

**Accessing Custom Data Attributes:**
- **HTML Example:**
  ```html
  <span id="user-avatar" data-avatar-url="{{ user_avatar }}" hidden></span>
  ```
- **JavaScript Code:**
  ```javascript
  const userAvatarUrl = document.getElementById('user-avatar').dataset.avatarUrl;
  ```

**Accessing Form and Text Values:**
- **Form Value:**
  ```javascript
  const value = document.getElementById('form-field').value;
  ```
- **Text Content:**
  ```javascript
  const text = document.getElementById('html-tag').innerText;
  ```

---

### Memcache for Question-Answer Caching

**Installation:**
```bash
sudo apt update
sudo apt install memcached
sudo systemctl start memcached
```

**Python Client:**
```bash
pip install python-memcached
```

**Django Configuration:**
```python
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
        'LOCATION': '127.0.0.1:11211',
    }
}
```

**Example Usage in Views:**
```python
from django.core.cache import cache

def my_view(request):
    cache_key = 'my_unique_key'
    cache_time = 86400  # Cache for 1 day
    data = cache.get(cache_key)
    if not data:
        data = expensive_function_call()
        cache.set(cache_key, data, cache_time)
    return JsonResponse(data, safe=False)
```

---

### Retrospection and Lessons Learned

#### Issue 1: Incorrect Python Version Impacted System
- **Problem:**
  Switching to Python 3.12 caused system-wide issues on Ubuntu.
- **Resolution:**
  - Used virtual environments (`python3.12 -m venv`) to isolate Python environments.
  - Avoided changing the default system Python version.

#### Issue 2: Static Image Path Misconfiguration
- **Problem:**
  Static images were not loading due to incorrect relative paths.
- **Resolution:**
  - Used full paths from the root project directory (`/static/images/...`) instead of relative paths (`/images/...`).

#### Issue 3: Docker Permissions Error
- **Problem:**
  Non-root users could not manage Docker.
- **Resolution:**
  - Added the current user to the `docker` group and applied the `newgrp docker` command.

#### Issue 4: Typo in JavaScript Element ID
- **Problem:**
  A typo in an HTML element ID (`custon` instead of `custom`) caused JavaScript errors.
- **Resolution:**
  - Corrected the ID in both HTML and JavaScript files.
  - Verified element IDs match across all code references.

#### Issue 5: Inefficient Database Calls
- **Problem:**
  Repeated database calls were impacting performance.
- **Resolution:**
  - Introduced `Memcache` to cache frequently accessed data.

#### Key Lessons:
- Always verify compatibility when upgrading dependencies.
- Use caching for frequently accessed data to improve performance.
- Establish clear conventions for element IDs and paths.

---

### Diagram Reference

A high-level diagram was referenced in the original notes:
- **Link:** [Diagram V1: High-Level View of App](https://excalidraw.com/#json=13cims8czPh4dJf0H06YF,avcPyjTq6wk_9r3-E0tu1Q)
- **Purpose:** Visualize the architecture and workflows for the application.

---

---

## Issues Identified and Solutions Implemented

### 1. **Static Image Paths in Django**
#### **Issue:**
Static image paths were incorrectly defined as relative paths (`/images/...`) instead of full paths from the project root (`/static/images/...`).

#### **Solution:**
Update all static image paths in templates and settings to use absolute paths, e.g.:
```html
<img src="/static/images/example.png" alt="Example">
```

---

### 2. **Typographical Error in JavaScript IDs**
#### **Issue:**
An ID used in the JavaScript logic contained a typo (`custon`) instead of `custom`, causing scripts to fail.

#### **Solution:**
Correct the typo in the HTML template:
```html
<div id="custom-action">Action</div>
```
Update the JavaScript to reference the correct ID:
```javascript
const actionElement = document.getElementById('custom-action');
```
---

### 3. **Accessing Form Values in JavaScript**
#### **Issue:**
Repeated calls to `.value` on form fields created unnecessary performance overhead.

#### **Solution:**
Assign the `.value` property to a constant and reuse it:
```javascript
const formValue = document.getElementById('form-field').value;
console.log(formValue);
```
---

### 4. **Avoiding Inline JavaScript**
#### **Issue:**
Inline JavaScript attributes like `onclick` were used, leading to cluttered HTML and maintainability issues.

#### **Solution:**
Use external JavaScript event listeners instead:
```html
<button id="submit-btn">Submit</button>
```
```javascript
const submitButton = document.getElementById('submit-btn');
submitButton.addEventListener('click', () => {
    console.log('Button clicked!');
});
```
---

### 5. **Avoiding `.unwrap()` in Rust**
#### **Issue:**
Using `.unwrap()` for error handling led to potential panics in production code.

#### **Solution:**
Replace `.unwrap()` with `match` patterns to gracefully handle errors:
```rust
let result = some_function();
match result {
    Ok(value) => println!("Success: {}", value),
    Err(e) => eprintln!("Error: {}", e),
}
```
---

### 6. **Preventing Terminal Issues When Changing Python Version**
#### **Issue:**
Changing the default Python version on Ubuntu caused terminal issues, such as `apt` malfunctioning.

#### **Solution:**
- Avoid modifying the system’s default Python version.
- Create virtual environments with the desired Python version:
```bash
python3.12 -m venv <name_of_env>
```
---

### 7. **Handling Database Connections with Memcache**
#### **Issue:**
Frequent database calls were leading to performance bottlenecks.

#### **Solution:**
Implement caching using Memcache for frequently accessed data:
```python
from django.core.cache import cache

def my_view(request):
    cache_key = 'my_unique_key'
    cache_time = 86400  # Cache for 1 day
    data = cache.get(cache_key)
    if not data:
        data = expensive_function_call()
        cache.set(cache_key, data, cache_time)
    return JsonResponse(data, safe=False)
```
---

### 8. **Improper GitHub Actions Workflow Alignment**
#### **Issue:**
The GitHub Actions workflow configuration did not align with the Django `settings.py` file, causing build failures.

#### **Solution:**
Update the workflow to reflect the correct settings and ensure compatibility.
```yaml
env:
  DJANGO_SETTINGS_MODULE: chatbotAI.settings
```
---

### 9. **Embedding and Retrieval Workflow Logic**
#### **Issue:**
Embedding logic was not finalized, causing inconsistencies in retrieval operations.

#### **Solution:**
- Perform independent testing for embedding logic.
- Ensure metadata includes question-answer pairs and document titles.
- Integrate the logic into Django routes after successful testing.
---

### 10. **Rust Function Integration into Python**
#### **Issue:**
Rust functions were not optimized or tested before being used in Python.

#### **Solution:**
- Use PyO3 and Maturin to build and test Rust functions.
- Gradually replace Python functions with validated Rust equivalents:
```bash
maturin develop
```
```python
import rust_lib
result = rust_lib.some_function()
```
---

### 11. **Unit Testing Strategy**
#### **Issue:**
Lack of comprehensive unit tests for critical paths.

#### **Solution:**
- Focus on meaningful test coverage (80-90%) for critical paths and edge cases.
- Use `pytest` and `coverage`:
```bash
coverage run --source='.' -m pytest --ds=chatbotAI.settings
coverage report
coverage html
```
---

### 12. **Security Vulnerabilities in API Rate Limiting**
#### **Issue:**
The API lacked rate limiting, exposing it to potential abuse.

#### **Solution:**
Implement Django REST Framework throttling classes:
```python
from rest_framework.throttling import UserRateThrottle

class CustomRateThrottle(UserRateThrottle):
    rate = '100/day'
```
---

### 13. **ArgoCD Misconfigurations**
#### **Issue:**
Initial ArgoCD configurations did not reflect the Kubernetes setup, causing deployment failures.

#### **Solution:**
- Correct repository paths and namespace settings in ArgoCD:
```bash
argocd app create <app-name> \
--repo <repo-url> \
--path <path-to-manifests> \
--dest-server https://kubernetes.default.svc \
--dest-namespace <namespace>
```
- Trigger sync after updates:
```bash
argocd app sync <app-name>
```
---

### 14. **Business Continuity Challenges**
#### **Issue:**
Lack of a formal disaster recovery and scaling plan.

#### **Solution:**
- Implement automated backups for PostgreSQL.
- Establish scaling strategies for high traffic using load balancers and horizontal pod autoscaling.

---

### Retrospections

1. **Communication Improvements:**
   - Ensure clear documentation and align team workflows to avoid misconfigurations.

2. **Testing Practices:**
   - Incremental testing and independent component validation reduce overall errors.

3. **CI/CD Alignment:**
   - Continuous integration and delivery pipelines should reflect real-world configurations to prevent deployment failures.

4. **Caching Benefits:**
   - Leveraging caching mechanisms can dramatically reduce database load and improve performance.

---

---

## Full Server Setup Issues and Solutions

### 1. **Python Version Conflicts**
#### **Issue:**
Conflicting Python versions on the server caused dependency mismatches and system package issues, leading to broken environments.

#### **Solution:**
- Standardize the server to use Python 3.12 via a controlled setup process:
```bash
sudo apt install software-properties-common -y
sudo add-apt-repository ppa:deadsnakes/ppa -y
sudo apt update -y
sudo apt install python3.12 -y
```
- Avoid modifying the default Python version by setting up a virtual environment:
```bash
python3.12 -m venv /path/to/venv
source /path/to/venv/bin/activate
```
- Ensure all required dependencies are installed within the virtual environment.

---

### 2. **PostgreSQL Version Compatibility**
#### **Issue:**
The PostgreSQL installation initially used an older version, leading to incompatibilities with Django models and data migrations.

#### **Solution:**
- Remove outdated PostgreSQL versions and configure the latest version:
```bash
sudo apt purge postgresql* -y
sudo apt autoremove --purge -y
sudo rm -rf /etc/postgresql /var/lib/postgresql /var/log/postgresql
```
- Add the PostgreSQL 17 repository and install:
```bash
echo "deb [arch=amd64] http://apt.postgresql.org/pub/repos/apt $(lsb_release -cs)-pgdg main" | sudo tee /etc/apt/sources.list.d/pgdg.list
wget -qO - https://www.postgresql.org/media/keys/ACCC4CF8.asc | sudo apt-key add -
sudo apt update
sudo apt install postgresql-17 postgresql-contrib -y
```
- Confirm the correct version:
```bash
psql --version
```

---

### 3. **Django Deployment Issues**
#### **Issue:**
Django application deployment failed due to missing dependencies, improper static files handling, and incorrect Gunicorn configurations.

#### **Solution:**
- Install all required packages:
```bash
pip install -r requirements.txt
```
- Collect static files:
```bash
python manage.py collectstatic --noinput
```
- Use Gunicorn for WSGI server setup:
```bash
gunicorn --workers=3 --bind unix:/path/to/socket.sock projectname.wsgi:application
```
- Configure Nginx to serve static files and proxy requests to Gunicorn.

---

### 4. **Firewall Rules Blocking Connections**
#### **Issue:**
The server firewall blocked connections to essential ports, such as 80 (HTTP) and 443 (HTTPS), causing downtime.

#### **Solution:**
- Update firewall rules to allow traffic on required ports:
```bash
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp
sudo ufw allow 22/tcp  # For SSH
sudo ufw enable
```
- Verify active rules:
```bash
sudo ufw status
```

---

### 5. **SSL Certificate Errors**
#### **Issue:**
SSL certificates were not properly configured, resulting in insecure connections and browser warnings.

#### **Solution:**
- Use Certbot to configure and renew SSL certificates automatically:
```bash
sudo apt install certbot python3-certbot-nginx -y
sudo certbot --nginx -d example.com -d www.example.com
```
- Test the certificate:
```bash
sudo certbot renew --dry-run
```

---

### 6. **Insufficient Resource Allocation**
#### **Issue:**
The server ran out of memory during high-traffic periods, causing application crashes.

#### **Solution:**
- Add swap space to the server:
```bash
sudo fallocate -l 2G /swapfile
sudo chmod 600 /swapfile
sudo mkswap /swapfile
sudo swapon /swapfile
```
- Make the swap file permanent:
```bash
echo '/swapfile none swap sw 0 0' | sudo tee -a /etc/fstab
```
- Optimize Gunicorn worker settings to better utilize available resources:
```bash
gunicorn --workers=3 --threads=2 --bind unix:/path/to/socket.sock projectname.wsgi:application
```

---

### 7. **Cron Job Failures**
#### **Issue:**
Scheduled cron jobs for periodic tasks (e.g., log cleanup, database backups) failed to execute properly due to incorrect paths and permissions.

#### **Solution:**
- Ensure the Python virtual environment is activated within cron jobs:
```bash
* * * * * source /path/to/venv/bin/activate && python /path/to/script.py
```
- Check and fix permissions for the script and log files:
```bash
chmod +x /path/to/script.py
sudo chown -R www-data:www-data /path/to/logs
```

---

### 8. **Backup and Disaster Recovery Plan**
#### **Issue:**
No automated backup system was in place, risking data loss in case of a failure.

#### **Solution:**
- Schedule daily backups of PostgreSQL:
```bash
pg_dump -U postgres dbname > /backups/db_backup_$(date +%F).sql
```
- Automate backups with a cron job:
```bash
0 2 * * * pg_dump -U postgres dbname > /backups/db_backup_$(date +%F).sql
```
- Implement off-site backup storage using AWS S3:
```bash
aws s3 cp /backups/db_backup_$(date +%F).sql s3://my-bucket-name/backups/
```

---

### 9. **Nginx Configuration Errors**
#### **Issue:**
Improper Nginx configurations led to 502 Bad Gateway errors.

#### **Solution:**
- Ensure the upstream server block matches Gunicorn:
```nginx
server {
    listen 80;
    server_name example.com www.example.com;

    location / {
        proxy_pass http://unix:/path/to/socket.sock;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }

    location /static/ {
        alias /path/to/static/;
    }

    location /media/ {
        alias /path/to/media/;
    }
}
```
- Restart Nginx:
```bash
sudo systemctl restart nginx
```

---

### Retrospections and Lessons Learned

1. **Environment Isolation:**
   - Using virtual environments for Python minimized system conflicts and made dependency management easier.

2. **Documentation:**
   - Thoroughly document every step of the setup to reduce onboarding time and errors for future developers.

3. **Automated Monitoring:**
   - Add monitoring tools like Prometheus and Grafana to preemptively identify resource bottlenecks and server health issues.

4. **Regular Testing:**
   - Test server configurations and backups regularly to ensure they work during actual failure scenarios.

5. **Fail-Safe Configurations:**
   - Always validate Nginx, PostgreSQL, and Gunicorn configurations before deploying to production.

---



