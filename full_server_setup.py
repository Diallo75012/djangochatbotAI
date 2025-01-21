#!/usr/bin/env python3
import os
import subprocess
from dotenv import load_dotenv


# Load environment variables from .env file
load_dotenv(dotenv_path='.env', override=False)
load_dotenv(dotenv_path=".vars.env", override=True)

POSTGRES_VERSION = os.getenv("POSTGRES_VERSION", "17")
DB_NAME = os.getenv("DBNAME")
DB_USER = os.getenv("DBUSER")
DB_PASSWORD = os.getenv("DBPASSWORD")
DB_HOST = os.getenv("DBHOST", "localhost")
DB_PORT = os.getenv("DBPORT", "5432")

USER=os.getenv("USER")
GROUP=os.getenv("GROUP")
PROJECT_DIR=os.getenv("PROJECT_DIR")
# this one should be installed in the virtual env so be in requirements.txt
GUNICORN_BINARY=os.getenv("GUNICORN_BINARY")
# the `gunicorn.sock` file will be created by `gunicorn` we just need to provide the path otherwise you get error
SOCK_FILE_PATH=os.getenv("SOCK_FILE_PATH")
PROJECT_WSGI=os.getenv("PROJECT_WSGI")
GUNICORN_CENTRAL_DIR = os.getenv("GUNICORN_CENTRAL_DIR")
SSL_DIR = os.getenv("SSL_DIR")
NGINX_IMAGE = os.getenv("NGINX_IMAGE")
VIRTUAL_ENV_PATH_FROM_USER_HOME = os.getenv("VIRTUAL_ENV_PATH_FROM_USER_HOME")
NGINX_LOGS_FOLDER_PATH = os.getenv("NGINX_LOGS_FOLDER_PATH")

# Functions
'''
def install_python_dependencies():
    print("Installing Python build dependencies...")
    subprocess.run(["sudo", "apt", "install", "-y", "build-essential", "python3.12-dev", "libpq-dev"], check=True)
    print("Python dependencies installed.")

def setup_gunicorn_logs():
    GUNICORN_CENTRAL_DIR = os.getenv("GUNICORN_CENTRAL_DIR")
    os.makedirs(GUNICORN_CENTRAL_DIR, exist_ok=True)
    print(f"Gunicorn logs directory created at {GUNICORN_CENTRAL_DIR}")

def install_postgresql():
    POSTGRES_VERSION = os.getenv("POSTGRES_VERSION", "17")
    print("Installing PostgreSQL...")
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
    DB_NAME = os.getenv("DBNAME")
    DB_USER = os.getenv("DBUSER")
    DB_PASSWORD = os.getenv("DBPASSWORD")
    DB_HOST = os.getenv("DBHOST", "localhost")
    DB_PORT = os.getenv("DBPORT", "5432")

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
    import subprocess
    import os

    print("Installing and configuring Nginx...")

    # Install Nginx
    subprocess.run(["sudo", "apt", "update"], check=True)
    subprocess.run(["sudo", "apt", "install", "-y", "nginx"], check=True)

    # Create Nginx configuration
    PROJECT_DIR = os.getenv("PROJECT_DIR")
    NGINX_LOGS_FOLDER_PATH = os.getenv("NGINX_LOGS_FOLDER_PATH")
    os.makedirs(NGINX_LOGS_FOLDER_PATH, exist_ok=True)
    subprocess.run(["sudo", "chown", "creditizens:creditizens", NGINX_LOGS_FOLDER_PATH], check=True)

    nginx_conf = f"""### NGINX CONF
server {{
  server_name creditizens.local;

  location /favicon.ico {{
      access_log off;
      log_not_found off;
  }}

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

  location / {{
      proxy_pass http://localhost:8000/;
      proxy_set_header Host $host;
      proxy_set_header X-Real-IP $remote_addr;
      proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
      proxy_set_header X-Forwarded-Proto $scheme;
  }}

  location /static/ {{
      alias {os.path.join(PROJECT_DIR, 'static')};
      expires 30d;
      add_header Cache-Control "public, max-age=2592000";
  }}

  location /media/ {{
      alias {os.path.join(PROJECT_DIR, 'media')};
      expires 30d;
      add_header Cache-Control "public, max-age=2592000";
  }}

  error_log {os.path.join(NGINX_LOGS_FOLDER_PATH, 'error.log')};
  access_log {os.path.join(NGINX_LOGS_FOLDER_PATH, 'access.log')};
}}"""

    nginx_conf_path = "/etc/nginx/sites-available/creditizens.local"
    nginx_symlink_path = "/etc/nginx/sites-enabled/creditizens.local"

    # Write Nginx configuration with sudo
    try:
        with open("/tmp/creditizens.local", "w") as temp_file:
            temp_file.write(nginx_conf)

        subprocess.run(["sudo", "mv", "/tmp/creditizens.local", nginx_conf_path], check=True)
        subprocess.run(["sudo", "ln", "-sf", nginx_conf_path, nginx_symlink_path], check=True)
    except Exception as e:
        print(f"Error writing Nginx configuration: {e}")
        return

    # Restart Nginx to apply changes
    subprocess.run(["sudo", "systemctl", "restart", "nginx"], check=True)
    print("Nginx installed and configured.")

def setup_ssl():
    import subprocess
    import os

    print("Setting up self-signed SSL certificate...")

    # Define the SSL directory (eg.: "/etc/ssl/creditizens")
    SSL_DIR = os.getenv("SSL_DIR")
    USER = os.getnev("USER")

    # Create the directory with sudo
    subprocess.run(["sudo", "mkdir", "-p", SSL_DIR], check=True)
    subprocess.run(["sudo", "chmod", "700", SSL_DIR], check=True)

    # Generate the self-signed SSL certificate
    subprocess.run([
        "sudo", "openssl", "req", "-x509", "-nodes", "-days", "365", "-newkey", "rsa:2048",
        "-keyout", f"{SSL_DIR}/{USER}.key",
        "-out", f"{SSL_DIR}/{USER}.crt",
        "-subj", "/C=US/ST=State/L=City/O=Organization/OU=Unit/CN={USER}.local"
    ], check=True)

    # Ensure proper permissions for the SSL key
    subprocess.run(["sudo", "chmod", "664", f"{SSL_DIR}/{USER}.key"], check=True)

    # Update /etc/hosts to include the creditizens.local entry
    hosts_entry = f"127.0.0.1 {USER}.local"

    try:
        # Backup the original permissions
        original_permissions = subprocess.check_output(["sudo", "stat", "-c", "%a", "/etc/hosts"]).decode().strip()

        # Temporarily grant write access (read/write for root, read for others)
        subprocess.run(["sudo", "chmod", "666", "/etc/hosts"], check=True)

        # Write the hosts entry if it does not exist
        with open("/etc/hosts", "r+") as hosts_file:
            lines = hosts_file.readlines()
            # Normalize lines by stripping whitespace
            normalized_lines = [line.strip() for line in lines]
            if hosts_entry not in normalized_lines:
                hosts_file.write(f"{hosts_entry}\n")
                print(f"/etc/hosts updated for {USER}.local")
            else:
                print(f"/etc/hosts already contains entry for {USER}.local")

        # Restore original permissions
        subprocess.run(["sudo", "chmod", original_permissions, "/etc/hosts"], check=True)

    except Exception as e:
        print(f"Failed to update /etc/hosts: {e}")
        return

    print("Self-signed SSL certificate created.")


def rotate_ssl_certificates():
    print("Rotating SSL certificates...")
    USER = os.getenv("USER")

    subprocess.run([
        "sudo", "openssl", "req", "-x509", "-nodes", "-days", "367", "-newkey", "rsa:2048",
        "-keyout", f"{SSL_DIR}/{USER}.key",
        "-out", f"{SSL_DIR}/{USER}.crt",
        "-subj", "/C=US/ST=State/L=City/O=Organization/CN={USER}.local"
    ], check=True)
    subprocess.run(["sudo", "systemctl", "reload", "nginx"], check=True)
    print("SSL certificates rotated and Nginx reloaded.")

def create_gunicorn_service():
    print("Creating Gunicorn systemd service...")

    USER=os.getenv("USER")
    GROUP=os.getenv("GROUP")
    PROJECT_DIR=os.getenv("PROJECT_DIR")
    # this one should be installed in the virtual env so be in requirements.txt
    GUNICORN_BINARY=os.getenv("GUNICORN_BINARY")
    # the `gunicorn.sock` file will be created by `gunicorn` we just need to provide the path otherwise you get error
    SOCK_FILE_PATH=os.getenv("SOCK_FILE_PATH")
    PROJECT_WSGI=os.getenv("PROJECT_WSGI")


    gunicorn_service = f"""[Unit]\nDescription=gunicorn daemon\nAfter=network.target\n\n[Service]\nUser={USER}\nGroup={GROUP}\nWorkingDirectory={PROJECT_DIR}\nExecStart={GUNICORN_BINARY} --workers 3 --bind unix:{SOCK_FILE_PATH}/gunicorn.sock {PROJECT_WSGI}:application\n\n[Install]\nWantedBy=multi-user.target"""

    with open(f"{PROJECT_DIR}/setup_gunicorn.txt", "w") as service_file:
        service_file.write(gunicorn_service)

    subprocess.run(["sudo", "mv", f"{PROJECT_DIR}/setup_gunicorn.txt", "/etc/systemd/system/gunicorn.service"], check=True)
    subprocess.run(["sudo", "systemctl", "daemon-reload"], check=True)
    subprocess.run(["sudo", "systemctl", "enable", "gunicorn"], check=True)
    subprocess.run(["sudo", "systemctl", "start", "gunicorn"], check=True)
    print("Gunicorn service created and started.")

def configure_ufw():
    print("Configuring UFW firewall...")

    # Retrieve the password from the environment variable
    SUDO_PASSWORD = os.getenv("SUDO_PASSWORD")

    if not sudo_password:
        print("Error: SUDO_PASSWORD environment variable is not set.")
        return

    # Create the commands to allow Nginx and enable UFW
    commands = [
        ["sudo", "-S", "ufw", "allow", "Nginx Full"],
        ["sudo", "-S", "ufw", "enable"],
    ]

    for command in commands:
        try:
            # Pass the password to the subprocess
            process = subprocess.run(
                command,
                input=f"{SUDO_PASSWORD}\n",  # Pass the password
                text=True,
                check=True
            )
            print(f"Command {' '.join(command)} executed successfully.")
        except subprocess.CalledProcessError as e:
            print(f"Error executing {' '.join(command)}: {e}")

    print("UFW configured to allow Nginx Full.")

def create_dockerfile():
    # Fetch environment variables
    USER = os.getenv("USER", "creditizens")
    GROUP = os.getenv("GROUP", "creditizens")
    PROJECT_DIR = os.getenv("PROJECT_DIR", "/home/creditizens/djangochatAI/chatbotAI")
    GUNICORN_BINARY = os.getenv("GUNICORN_BINARY", "/home/creditizens/djangochatAI/djangochatbotAI_venv/bin/gunicorn")
    PROJECT_WSGI = os.getenv("PROJECT_WSGI", "chatbotAI.wsgi")

    # Define the Dockerfile content dynamically using environment variables
    dockerfile_content = f"""# Stage 1: Builder
FROM python:3.12-slim as builder

WORKDIR /app

# Install build tools and dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \\
    build-essential \\
    python3.12-dev \\
    libpq-dev \\
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Set up the virtual environment
RUN python3 -m venv /home/{USER}/{VIRTUAL_ENV_PATH_FROM_USER_HOME}
ENV PATH="/home/{USER}/{VIRTUAL_ENV_PATH_FROM_USER_HOME}/bin:$PATH"

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Stage 2: Final Image
FROM python:3.12-slim

WORKDIR /app

# Create user and group for running the application
RUN groupadd -r {GROUP} && useradd --no-log-init -r -g {GROUP} {USER}

# Copy virtual environment from the builder stage
COPY --from=builder /home/{USER}/{VIRTUAL_ENV_PATH_FROM_USER_HOME} /home/{USER}/{VIRTUAL_ENV_PATH_FROM_USER_HOME}

# Update PATH to use the virtual environment
ENV PATH="/home/{USER}/{VIRTUAL_ENV_PATH_FROM_USER_HOME}/bin:$PATH"

# Copy project files
COPY . {PROJECT_DIR}

# Set permissions
RUN chown -R {USER}:{GROUP} {PROJECT_DIR}

USER {USER}

# Define the command to run the application
CMD ["{GUNICORN_BINARY}", "-b", "0.0.0.0:8000", "{PROJECT_WSGI}:application"]"""

    # Write the Dockerfile to the project directory
    dockerfile_path = os.path.join(PROJECT_DIR, "Dockerfile")
    with open(dockerfile_path, "w") as dockerfile:
        dockerfile.write(dockerfile_content)

    print(f"Dockerfile created at {dockerfile_path}.")

'''
def create_docker_compose():
    GUNICORN_CENTRAL_DIR = os.getnev("GUNICORN_CENTRAL_DIR")
    NGINX_IMAGE = os.getnev("NGINX_IMAGE")
    NGINX_LOGS_FOLDER_PATH = os.getenv("NGINX_LOGS_FOLDER_PATH")
    POSTGRES_VERSION = os.getenv("POSTGRES_VERSION", "17")
    DB_NAME = os.getenv("DBNAME")
    DB_USER = os.getenv("DBUSER")
    DB_PASSWORD = os.getenv("DBPASSWORD")


    docker_compose_content = f"""version: '3.8'
services:
  web:
    build: .
    ports:
      - "8000:8000"
    env_file:
      - .env
    volumes:
      - ./gunicorn:{GUNICORN_CENTRAL_DIR}
    networks:
      - app_network

  nginx:
    image: {NGINX_IMAGE}
    ports:
      - "80:80"
    volumes:
      - {NGINX_LOGS_FOLDER_PATH}:/var/log/nginx
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
  app_network:"""
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
        rotate_ssl_certificates()
        create_gunicorn_service()
        configure_ufw()
        create_dockerfile()
        create_docker_compose()
        print("Setup completed successfully.")
    except subprocess.CalledProcessError as e:
        print(f"An error occurred: {e}")

