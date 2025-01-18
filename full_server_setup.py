#!/usr/bin/env python3
import os
import subprocess
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()
DB_NAME = os.getenv("DBNAME")
DB_USER = os.getenv("DBUSER")
DB_PASSWORD = os.getenv("DBPASSWORD")
DB_HOST = os.getenv("DBHOST", "localhost")
DB_PORT = os.getenv("DBPORT", "5432")

PROJECT_DIR = f"/home/creditizens/{os.getenv('PROJECT_NAME')}"
# need to create those two folders in root directory of django project `mkdir gunicorn nginx_logs`
GUNICORN_LOG_DIR = os.path.join(PROJECT_DIR, "gunicorn")
NGINX_LOG_DIR = os.path.join(PROJECT_DIR, "nginx_logs")
POSTGRES_VERSION = os.getenv("POSTGRES_VERSION") # 17

# Functions
def install_python_dependencies():
    print("Installing Python build dependencies...")
    subprocess.run(["sudo", "apt", "install", "-y", "build-essential", "python3.12-dev", "libpq-dev"], check=True)
    print("Python dependencies installed.")

def setup_gunicorn_logs():
    os.makedirs(GUNICORN_LOG_DIR, exist_ok=True)
    print(f"Gunicorn logs directory created at {GUNICORN_LOG_DIR}")

def install_postgresql():
    print("Installing PostgreSQL...")
    # Add PostgreSQL repository
    subprocess.run([
        "sudo", "sh", "-c",
        "echo \"deb [arch=amd64] http://apt.postgresql.org/pub/repos/apt $(lsb_release -cs)-pgdg main\" > /etc/apt/sources.list.d/pgdg.list"
    ], check=True)
    subprocess.run([
        "wget", "-qO", "-", "https://www.postgresql.org/media/keys/ACCC4CF8.asc", "|", "sudo", "apt-key", "add", "-"
    ], check=True)

    subprocess.run(["sudo", "apt", "update"], check=True)
    subprocess.run(["sudo", "apt", "install", f"postgresql-{POSTGRES_VERSION}", "postgresql-contrib", "-y"], check=True)
    subprocess.run(["sudo", "systemctl", "start", "postgresql"], check=True)
    subprocess.run(["sudo", "systemctl", "enable", "postgresql"], check=True)

    print("PostgreSQL installed and started.")

def configure_postgresql():
    print("Configuring PostgreSQL...")
    setup_script = f"""
sudo su postgres <<EOF
createdb {DB_NAME};
psql -c \"CREATE ROLE {DB_USER};\"
psql -c \"ALTER ROLE {DB_USER} WITH LOGIN;\"
psql -c \"ALTER ROLE {DB_USER} WITH SUPERUSER;\"
psql -c \"CREATE USER {DB_USER} WITH PASSWORD '{DB_PASSWORD}';\"
psql -c \"ALTER ROLE {DB_USER} SET client_encoding TO 'utf8';\"
psql -c \"ALTER ROLE {DB_USER} SET default_transaction_isolation TO 'read committed';\"
psql -c \"ALTER ROLE {DB_USER} SET timezone TO 'UTC';\"
psql -c \"GRANT ALL PRIVILEGES ON DATABASE {DB_NAME} TO {DB_USER};\"
psql -c \"CREATE EXTENSION IF NOT EXISTS pgvector;\"
exit
EOF
"""
    subprocess.run(setup_script, shell=True, check=True)
    print(f"PostgreSQL configured with database {DB_NAME}, user {DB_USER}, and extensions.")

def setup_nginx():
    print("Installing and configuring Nginx...")
    subprocess.run(["sudo", "apt", "install", "-y", "nginx"], check=True)

    os.makedirs(NGINX_LOG_DIR, exist_ok=True)
    subprocess.run(["sudo", "chown", "creditizens:creditizens", NGINX_LOG_DIR], check=True)

    nginx_conf = f"""
    ### NGINX CONF

    server {{

      # Define the domain names this server block will handle
      server_name creditizens.local;

      # Disable logging for requests to /favicon.ico
      location /favicon.ico {{
          access_log off; # Turn off access logging for favicon requests
          log_not_found off; # Turn off logging if favicon is not found
      }}

      # Enable Gzip compression to reduce file sizes sent to the client
      gzip on;

      # Specify MIME types to be compressed with Gzip
      gzip_types application/atom+xml application/javascript application/json application/ld+json application/manifest+json application/rss+xml
                 application/vnd.geo+json application/vnd.ms-fontobject application/x-font-ttf application/x-web-app-manifest+json application/xhtml+xml
                 application/xml font/opentype image/bmp image/svg+xml image/x-icon text/cache-manifest text/css text/plain text/vcard text/vnd.rim.location.xloc
                 text/vnd.geojson+json;

      # Compress all requests coming from proxies
      gzip_proxied any;

      # Only compress files larger than 256 bytes
      gzip_min_length 256;

      # Enable response variation based on the Accept-Encoding header (for Gzip)
      gzip_vary on;

      # Allow decompression of Gzipped content if the client does not support it
      gunzip on;

      # Add HTTP Strict Transport Security (HSTS) to enforce HTTPS
      add_header Strict-Transport-Security "max-age=15768000; includeSubDomains; preload" always;

      # Add headers to improve security
      add_header 'Referrer-Policy' 'origin';
      add_header Feature-Policy "vibrate 'none';";
      add_header Permissions-Policy "geolocation=(),midi=(),sync-xhr=(),microphone=(),camera=(),magnetometer=(),gyroscope=(),fullscreen=(self),payment=();";
      add_header X-XSS-Protection "1; mode=block";
      add_header X-Frame-Options "SAMEORIGIN";
      add_header X-Content-Type-Options "nosniff";
      add_header Content-Security-Policy "default-src 'self'; script-src 'self'; style-src 'self'; img-src 'self';";

      # Proxy all requests to the backend application server
      location / {{
          proxy_pass http://localhost:8000/;
          proxy_set_header Host $host;
          proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
          proxy_set_header X-Real-IP $remote_addr;
          proxy_set_header X-Forwarded-Proto $scheme;
      }}

      # Serve static files directly from the specified directory
      location /static/ {{
        alias {os.path.join(PROJECT_DIR, 'static')};
        expires 30d;
        add_header Cache-Control "public, max-age=2592000";
      }}

      error_log {os.path.join(NGINX_LOG_DIR, 'error.log')};
      access_log {os.path.join(NGINX_LOG_DIR, 'access.log')};
    }}
    """
    nginx_conf_path = "/etc/nginx/sites-available/creditizens.local"
    with open(nginx_conf_path, "w") as f:
        f.write(nginx_conf)

    subprocess.run(["sudo", "ln", "-sf", nginx_conf_path, "/etc/nginx/sites-enabled/"], check=True)
    subprocess.run(["sudo", "systemctl", "restart", "nginx"], check=True)
    print("Nginx installed and configured.")

def setup_ssl():
    print("Setting up self-signed SSL certificate...")
    ssl_dir = os.getenv("SSL_DIR")
    os.makedirs(ssl_dir, exist_ok=True)

    subprocess.run([
        "sudo", "openssl", "req", "-x509", "-nodes", "-days", "365", "-newkey", "rsa:2048",
        "-keyout", f"{ssl_dir}/creditizens.key",
        "-out", f"{ssl_dir}/creditizens.crt",
        "-subj", "/C=US/ST=State/L=City/O=Organization/OU=Unit/CN=creditizens.local"
    ], check=True)

    subprocess.run(["sudo", "chmod", "600", f"{ssl_dir}/creditizens.key"], check=True)
    print("Self-signed SSL certificate created.")

    # Update /etc/hosts
    with open("/etc/hosts", "a") as hosts_file:
        hosts_file.write("\n127.0.0.1 creditizens.local\n")
    print("/etc/hosts updated for creditizens.local")

def create_dockerfile():
    dockerfile_content = f"""
    # Multi-stage build Dockerfile

    FROM python:3.12-slim as builder

    WORKDIR /app

    RUN apt-get update && apt-get install -y build-essential python3.12-dev libpq-dev && apt-get clean

    COPY requirements.txt ./
    RUN pip install --no-cache-dir -r requirements.txt

    FROM python:3.12-slim

    WORKDIR /app

    RUN groupadd -r creditizens && useradd --no-log-init -r -g creditizens creditizens

    COPY --from=builder /app /app
    COPY . /app

    RUN chown -R creditizens:creditizens /app

    USER creditizens

    CMD ["gunicorn", "-b", "0.0.0.0:8000", "<project>.wsgi:application"]
    """
    with open(os.path.join(PROJECT_DIR, "Dockerfile"), "w") as dockerfile:
        dockerfile.write(dockerfile_content)
    print("Dockerfile created.")

def create_docker_compose():
    docker_compose_content = f"""
    version: '3.8'

    services:
      web:
        build: .
        ports:
          - "8000:8000"
        env_file:
          - .env
        volumes:
          - ./gunicorn:/app/gunicorn_logs
        networks:
          - app_network

      nginx:
        image: nginx:latest
        ports:
          - "80:80"
        volumes:
          - ./nginx_logs:/var/log/nginx
        depends_on:
          - web
        networks:
          - app_network

      db:
        image: postgres:{POSTGRES_VERSION}
        environment:
          POSTGRES_USER: {DB_USER}
          POSTGRES_PASSWORD: {DB_PASSWORD}
          POSTGRES_DB: {DB_NAME}
        volumes:
          - pgdata:/var/lib/postgresql/data
        networks:
          - app_network

    volumes:
      pgdata:

    networks:
      app_network:
    """
    with open(os.path.join(PROJECT_DIR, "docker-compose.yml"), "w") as docker_compose:
        docker_compose.write(docker_compose_content)
    print("docker-compose.yml created.")

if __name__ == "__main__":
    try:
        install_python_dependencies()
        setup_gunicorn_logs()
        install_postgresql()
        configure_postgresql()
        setup_nginx()
        setup_ssl()
        create_dockerfile()
        create_docker_compose()
        print("Setup completed successfully.")
    except subprocess.CalledProcessError as e:
        print(f"An error occurred: {e}")

