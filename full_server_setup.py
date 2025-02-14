#!/usr/bin/env python3
import os
import time
import shutil
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
SOCK_FILE_DIR="/run/gunicorn"
SOCK_FILE_NAME="gunicorn.sock"
PROJECT_WSGI=os.getenv("PROJECT_WSGI")
GUNICORN_CENTRAL_DIR = os.getenv("GUNICORN_CENTRAL_DIR")
SSL_DIR = os.getenv("SSL_DIR")
NGINX_IMAGE = os.getenv("NGINX_IMAGE")
VIRTUAL_ENV_PATH_FROM_USER_HOME = os.getenv("VIRTUAL_ENV_PATH_FROM_USER_HOME")
LOGS_FOLDER_PATH = os.getenv("LOGS_FOLDER_PATH")

# Functions
def install_python_dependencies():
    print("Installing Python build dependencies...")
    subprocess.run(["sudo", "apt", "install", "-y", "build-essential", "python3.12-dev", "libpq-dev"], check=True)
    print("Python dependencies installed.")

def install_postgresql():
    POSTGRES_VERSION = os.getenv("POSTGRES_VERSION", "17")
    print("Installing PostgreSQL...")

    try:
        # Add PostgreSQL APT repository
        subprocess.run(
            "sudo sh -c 'echo \"deb [arch=amd64] http://apt.postgresql.org/pub/repos/apt $(lsb_release -cs)-pgdg main\" > /etc/apt/sources.list.d/pgdg.list'",
            shell=True,
            check=True
        )

        # Create the keyrings directory and add the PostgreSQL GPG key
        subprocess.run(
            "sudo mkdir -p /etc/apt/keyrings && sudo wget -qO /etc/apt/keyrings/postgresql.asc https://www.postgresql.org/media/keys/ACCC4CF8.asc",
            shell=True,
            check=True
        )

        # Update package lists
        subprocess.run(["sudo", "apt", "update", "-y"], check=True)

        # Install PostgreSQL and contrib packages
        subprocess.run(
            ["sudo", "apt", "install", f"postgresql-{POSTGRES_VERSION}", "postgresql-contrib", "-y"],
            check=True
        )

        # Install pgvector extension
        subprocess.run(
            ["sudo", "apt", "install", f"postgresql-{POSTGRES_VERSION}-pgvector", "-y"],
            check=True
        )

        # Start PostgreSQL service
        #subprocess.run(["sudo", "service", "postgresql", "start"], check=True)
        # Start and enable PostgreSQL service
        subprocess.run(["sudo", "systemctl", "start", "postgresql"], check=True)
        subprocess.run(["sudo", "systemctl", "enable", "postgresql"], check=True) # `enable` to start on every reboot (Prod)

        print("PostgreSQL and pgvector installed and started successfully.")

    except subprocess.CalledProcessError as e:
        print(f"Error installing PostgreSQL: {e}")

def configure_postgresql():


    DB_NAME = os.getenv("DBNAME")
    DB_USER = os.getenv("DBUSER")
    DB_PASSWORD = os.getenv("DBPASSWORD")
    POSTGRES_VERSION = os.getenv("POSTGRES_VERSION")

    print("Configuring PostgreSQL...")

    try:
        # Step 1: Update pg_hba.conf to replace peer with md5
        pg_hba_path = f"/etc/postgresql/{POSTGRES_VERSION}/main/pg_hba.conf"
        update_pg_hba_command = f"""
sudo sed -i -e '/^local\\s\\+all\\s\\+all\\s\\+peer/s/peer/md5/' \\
            -e '/^host\\s\\+all\\s\\+all\\s\\+127.0.0.1\\/32\\s\\+peer/s/peer/md5/' \\
            -e '/^host\\s\\+all\\s\\+all\\s\\+::1\\/128\\s\\+peer/s/peer/md5/' {pg_hba_path}
"""
        subprocess.run(update_pg_hba_command, shell=True, check=True)
        print("pg_hba.conf updated for md5 authentication.")

        # Restart PostgreSQL to apply changes
        subprocess.run(["sudo", "systemctl", "restart", "postgresql"], check=True) # `systemctl` way
        #subprocess.run(["sudo", "service", "postgresql", "restart"], check=True) # `service` way for `WSL2`
        print("PostgreSQL service restarted successfully.")

        # Create database, user, and enable pgvector extension
        # Create the database if it doesn't exist
        subprocess.run(
            [
                "sudo",
                "-u",
                "postgres",
                "bash",
                "-c",
                f"if ! psql -lqt | cut -d '|' -f 1 | grep -qw {DB_NAME}; then "
                f"createdb {DB_NAME}; "
                f"echo 'Database {DB_NAME} created successfully.'; "
                f"else "
                f"echo 'Database {DB_NAME} already exists.'; "
                f"fi",
            ],
            check=True,
        )

        # Create the role if it doesn't exist
        subprocess.run(
            [
                "sudo",
                "-u",
                "postgres",
                "bash",
                "-c",
                f"if ! psql -tAc \"SELECT 1 FROM pg_roles WHERE rolname='{DB_USER}';\" | grep -qw 1; then "
                f"psql -c \"CREATE ROLE {DB_USER} WITH LOGIN PASSWORD '{DB_PASSWORD}';\"; "
                f"echo 'Role {DB_USER} created successfully.'; "
                f"else "
                f"echo 'Role {DB_USER} already exists.'; "
                f"fi",
            ],
            check=True,
        )

        # Configure the role
        subprocess.run(
            [
                "sudo",
                "-u",
                "postgres",
                "bash",
                "-c",
                f"psql -c \"ALTER ROLE {DB_USER} WITH SUPERUSER;\"; "
                f"psql -c \"ALTER ROLE {DB_USER} SET client_encoding TO 'utf8';\"; "
                f"psql -c \"ALTER ROLE {DB_USER} SET default_transaction_isolation TO 'read committed';\"; "
                f"psql -c \"ALTER ROLE {DB_USER} SET timezone TO 'UTC';\"; "
                f"echo 'Role {DB_USER} configured successfully.';",
            ],
            check=True,
        )

        # Grant privileges to the user on the database
        subprocess.run(
            [
                "sudo",
                "-u",
                "postgres",
                "bash",
                "-c",
                f"psql -c \"GRANT ALL PRIVILEGES ON DATABASE {DB_NAME} TO {DB_USER};\"",
            ],
            check=True,
        )

        # Enable pgvector extension
        subprocess.run(
            [
                "sudo",
                "-u",
                "postgres",
                "bash",
                "-c",
                f"if ! psql -d {DB_NAME} -tAc \"SELECT 1 FROM pg_extension WHERE extname='vector';\" | grep -qw 1; then "
                f"psql -d {DB_NAME} -c \"CREATE EXTENSION vector;\"; "
                f"echo 'pgvector extension enabled for database {DB_NAME}.'; "
                f"else "
                f"echo 'pgvector extension is already enabled for database {DB_NAME}.'; "
                f"fi",
            ],
            check=True,
        )

        print(f"PostgreSQL configured successfully with database '{DB_NAME}', user '{DB_USER}', and 'pgvector' extension enabled.")

    except subprocess.CalledProcessError as e:
        print(f"Error configuring PostgreSQL: {e}")

def setup_ssl():
    import subprocess
    import os

    # install openssl as sometimes you get error because file doesn't exist
    #print("Removing openssl for fresh install")
    #subprocess.run(["sudo", "apt", "remove", "--purge", "openssl"], check=True)
    #subprocess.run(["sudo", "apt", "install", "openssl"], check=True)
    #print("Openssl install done... will now create certs..")

    print("Setting up self-signed SSL certificate...")

    # Define the SSL directory (eg.: "/etc/ssl/creditizens")
    SSL_DIR = os.getenv("SSL_DIR")
    USER = os.getenv("USER")

    # Create the directory with sudo
    subprocess.run(["sudo", "mkdir", "-p", SSL_DIR], check=True)
    subprocess.run(["sudo", "chmod", "700", SSL_DIR], check=True)

    # Generate the self-signed SSL certificate
    #OPENSSL_CONF_FILE_PATH = os.getenv("OPENSSL_CONF_FILE_PATH")
    subprocess.run([
        "sudo", "openssl", "req", "-x509", "-nodes", "-days", "365", "-newkey", "rsa:2048",
        "-keyout", f"{SSL_DIR}/{USER}.key",
        "-out", f"{SSL_DIR}/{USER}.crt",
        "-subj", f"/C=US/ST=State/L=City/O=Organization/OU=Unit/CN={USER}.local",
        #"-config", OPENSSL_CONF_FILE_PATH
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
        "-subj", f"/C=US/ST=State/L=City/O=Organization/CN={USER}.local"
    ], check=True)
    subprocess.run(["sudo", "systemctl", "reload", "nginx"], check=True)
    print("SSL certificates rotated and Nginx reloaded.")

def setup_nginx():
    import subprocess
    import os

    print("Installing and configuring Nginx...")

    # Install Nginx
    subprocess.run(["sudo", "apt", "update"], check=True)
    subprocess.run(["sudo", "apt", "install", "-y", "nginx"], check=True)

    # Create Nginx configuration
    USER = os.getenv("USER")
    GROUP = os.getenv("GROUP")
    SSL_DIR = os.getenv("SSL_DIR")
    GUNICORN_CENTRAL_DIR = os.getenv("GUNICORN_CENTRAL_DIR")
    STATIC_DESTINATION = os.getenv("STATIC_DESTINATION")
    MEDIA_DESTINATION = os.getenv("MEDIA_DESTINATION")
    PROJECT_DIR = os.getenv("PROJECT_DIR")
    LOGS_FOLDER_PATH = os.getenv("LOGS_FOLDER_PATH")
    os.makedirs(LOGS_FOLDER_PATH, exist_ok=True)
    subprocess.run(["sudo", "chown", f"{USER}:{GROUP}", LOGS_FOLDER_PATH], check=True)

    nginx_conf = f"""### NGINX CONF
### NGINX CONF
# Redirect HTTP traffic to HTTPS
upstream {USER}.local {{
    server unix:/run/gunicorn/gunicorn.sock fail_timeout=0;
}}

# to not display nginx server version in headers
server_tokens             off;

# Redirect HTTP traffic to HTTPS
server {{
  listen 80;
  server_name {USER}.local;

  # Redirect all HTTP requests to HTTPS
  return 301 https://$host$request_uri;
}}
server {{
  listen 443 ssl;
  server_name {USER}.local;

  ssl_certificate {SSL_DIR}/{USER}.crt;
  ssl_certificate_key {SSL_DIR}/{USER}.key;

  # General proxy settings
  proxy_http_version 1.1;
  proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
  proxy_set_header Host $host;
  proxy_set_header Upgrade $http_upgrade;
  proxy_set_header Connection "upgrade";
  proxy_read_timeout 86400;

  # if user file upload enabled this is for: file upload max size allowed
  #client_max_body_size 2000M;

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
      # we are not using direct connection to Django server, Gunicorn handles it
      #proxy_pass http://localhost:8000/;
      # we are using gunicorn UNIX socket to point to Django server
      proxy_pass http://unix:{GUNICORN_CENTRAL_DIR}/gunicorn.sock;
      proxy_set_header Host $host;
      proxy_set_header X-Real-IP $remote_addr;
      proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
      proxy_set_header X-Forwarded-Proto $scheme;
  }}

  location /static/ {{
      alias {STATIC_DESTINATION}/;
      expires 30d;
      add_header Cache-Control "public, max-age=2592000";
  }}

  location /media/ {{
      alias {MEDIA_DESTINATION}/;
      expires 30d;
      add_header Cache-Control "public, max-age=2592000";
  }}


  error_log {os.path.join(LOGS_FOLDER_PATH, 'nginx_error.log')};
  access_log {os.path.join(LOGS_FOLDER_PATH, 'nginx_access.log')};
}}"""

    nginx_conf_path = f"/etc/nginx/sites-available/{USER}.local"
    nginx_symlink_path = f"/etc/nginx/sites-enabled/{USER}.local"

    # Write Nginx configuration with sudo
    try:
        with open("/tmp/creditizens.local", "w") as temp_file:
            temp_file.write(nginx_conf)

        subprocess.run(["sudo", "mv", f"/tmp/{USER}.local", nginx_conf_path], check=True)
        subprocess.run(["sudo", "ln", "-sf", nginx_conf_path, nginx_symlink_path], check=True)
    except Exception as e:
        print(f"Error writing Nginx configuration: {e}")
        return
    '''
    # when we runt he script sevral time happens that a file is created in `sites-enables` which causes error
    # is is actually called `{USER}.local` cause forgot to put `f-string` before so should be fine to remove this code check
    nginx_error_path_web_running_again_script = "/etc/nginx/sites-enabled/{USER}.local"
    if not os.path.exists(nginx_error_path_web_running_again_script):
      # Restart Nginx to apply changes
      subprocess.run(["sudo", "systemctl", "restart", "nginx"], check=True)
      print("Nginx installed and configured.")
    # here we delete the file created by error and restart `nginx`
    else:
      # Restart Nginx to apply changes after having delete the troublesome file created
      subprocess.run(["sudo", "systemctl", "restart", "nginx"], check=True)
      subprocess.run(["sudo", "rm", nginx_error_path_web_running_again_script], check=True)
      print("Nginx installed and configured.")
    '''
    subprocess.run(["sudo", "systemctl", "restart", "nginx"], check=True)
    print("Nginx installed and configured.")

def prepare_django_app():
    """
    Prepares the Django application by collecting static files, migrating the database,
    and setting up static/media files for Nginx to serve.
    """
    print("Preparing Django application...")

    USER = os.getenv("USER")
    PROJECT_DIR = os.getenv("PROJECT_DIR")
    STATIC_DESTINATION = os.getenv("STATIC_DESTINATION", "/var/www/static")
    MEDIA_DESTINATION = os.getenv("MEDIA_DESTINATION", "/var/www/media")
    NGINX_USER = os.getenv("NGINX_USER")  # Directly using www-data as confirmed from nginx.conf

    # Ensure the destination directories for static and media exist
    for destination in [STATIC_DESTINATION, MEDIA_DESTINATION]:
        if not os.path.exists(destination):
            subprocess.run(["sudo", "mkdir", "-p", destination], check=True)
        # Give ownership to the current user during preparation to be able to copy without permission issues
        # after later in this function we give right permissions when in the nginx location (`www-data` user)
        subprocess.run(["sudo", "chown", "-R", f"{USER}:{USER}", destination], check=True)

    try:
        # Change to project directory
        os.chdir(PROJECT_DIR)

        # Collect static files
        print("Collecting static files...")
        subprocess.run(["python3", "manage.py", "collectstatic", "--noinput"], check=True)

        # Migrate the database
        print("Running database migrations...")
        subprocess.run(["python3", "manage.py", "migrate"], check=True)

        # Copy static and media files to the Nginx-served directories
        print(f"Copying static files to {STATIC_DESTINATION}...")
        shutil.copytree(
            os.path.join(PROJECT_DIR, "static"), STATIC_DESTINATION, dirs_exist_ok=True
        )

        print(f"Copying media files to {MEDIA_DESTINATION}...")
        shutil.copytree(
            os.path.join(PROJECT_DIR, "media"), MEDIA_DESTINATION, dirs_exist_ok=True
        )

        # Set permissions for Nginx to serve files
        print("Setting permissions for static and media files...")
        subprocess.run(["sudo", "chown", "-R", f"{NGINX_USER}:{NGINX_USER}", STATIC_DESTINATION], check=True)
        subprocess.run(["sudo", "chmod", "-R", "775", STATIC_DESTINATION], check=True)
        subprocess.run(["sudo", "chown", "-R", f"{NGINX_USER}:{NGINX_USER}", MEDIA_DESTINATION], check=True)
        subprocess.run(["sudo", "chmod", "-R", "775", MEDIA_DESTINATION], check=True)

        print("Django application prepared successfully.")

    except subprocess.CalledProcessError as e:
        print(f"Error while preparing Django application: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

class Gunicorn:

  def setup_gunicorn_center_dir():

      USER = os.getenv("USER")
      GUNICORN_CENTRAL_DIR = os.getenv("GUNICORN_CENTRAL_DIR")

      if not os.path.exists(GUNICORN_CENTRAL_DIR):
          try:
              #os.makedirs(GUNICORN_CENTRAL_DIR, exist_ok=True)
              subprocess.run(["sudo", "mkdir", GUNICORN_CENTRAL_DIR], check=True)
              subprocess.run(["sudo", "chown", f"{USER}:{USER}", GUNICORN_CENTRAL_DIR], check=True)
              subprocess.run(["sudo", "chmod", "-R", "755", GUNICORN_CENTRAL_DIR], check=True)
              print(f"Directory {GUNICORN_CENTRAL_DIR} created successfully.")
          except subprocess.CalledProcessError as e:
              print(f"An error occurred: {e}")
      else:
          print(f"Directory {GUNICORN_CENTRAL_DIR} already exists. Just checking permissison and changing those to be sure")
          subprocess.run(["sudo", "chown", f"{USER}:{USER}", GUNICORN_CENTRAL_DIR], check=True)
          subprocess.run(["sudo", "chmod", "-R", "755", GUNICORN_CENTRAL_DIR], check=True)

      print(f"Gunicorn logs directory created at {GUNICORN_CENTRAL_DIR}")

  def create_gunicorn_service():
      import os
      import subprocess
      import time

      print("Creating Gunicorn systemd service...")

      USER = os.getenv("USER")
      GROUP = os.getenv("GROUP")
      PROJECT_DIR = os.getenv("PROJECT_DIR")
      WORKERS = os.getenv("WORKERS")
      GUNICORN_BINARY = os.getenv("GUNICORN_BINARY")
      SOCK_FILE_DIR=os.getenv("SOCK_FILE_DIR")
      SOCK_FILE_NAME=os.getenv("SOCK_FILE_NAME")
      SOCK_FILE_PATH = os.path.join(SOCK_FILE_DIR, SOCK_FILE_NAME)
      PROJECT_WSGI = os.getenv("PROJECT_WSGI")
      LOG_DIR = os.path.join(PROJECT_DIR, "logs")
      

      # Ensure the log directory exists and set permissions
      if not os.path.exists(LOG_DIR):
          os.makedirs(LOG_DIR, exist_ok=True)
          subprocess.run(["sudo", "chown", "-R", f"{USER}:{GROUP}", LOG_DIR], check=True)
          subprocess.run(["sudo", "chmod", "-R", "755", LOG_DIR], check=True)

      gunicorn_service = f"""# see doc for more setup: https://docs.gunicorn.org/en/stable/deploy.html#systemd
[Unit]
Description=gunicorn daemon
After=network.target

[Service]
User={USER}
Group={GROUP}
WorkingDirectory={PROJECT_DIR}
# here `SOCK_FILE_PATH` is combinaison of env vars `SOCK_FILE_DIR`and `SOCK_FILE_NAME`
ExecStart={GUNICORN_BINARY} --workers {WORKERS} --bind unix:{SOCK_FILE_PATH} {PROJECT_WSGI}:application

[Install]
WantedBy=multi-user.target
"""

      # Write the service file
      with open(f"{PROJECT_DIR}/setup_gunicorn.txt", "w") as service_file:
          service_file.write(gunicorn_service)

      # Move the service file to the systemd directory
      subprocess.run(["sudo", "mv", f"{PROJECT_DIR}/setup_gunicorn.txt", "/etc/systemd/system/gunicorn.service"], check=True)
      subprocess.run(["sudo", "systemctl", "daemon-reload"], check=True)
      subprocess.run(["sudo", "systemctl", "enable", "gunicorn"], check=True)
      subprocess.run(["sudo", "systemctl", "start", "gunicorn"], check=True)

      # Wait for the socket file to be created
      print("Waiting for the Gunicorn socket file to be created...")
      for t in range(10):  # Retry for up to 10 seconds
          if os.path.exists(SOCK_FILE_PATH):
              break
          time.sleep(5)
          # restart `Gunicorn` service as the service might run correctly but the file not found and restarting it will create that damn file
          if t == 5:
              subprocess.run(["sudo", "systemctl", "restart", "gunicorn"], check=True)
      else:
          raise FileNotFoundError(f"Socket file {SOCK_FILE_PATH} was not created.")

      # Set permissions for the socket dir | not sure if needed as `gunicorn` service run as 'USER' and not 'ROOT'
      subprocess.run(["sudo", "chown", f"{USER}:{GROUP}", f"{SOCK_FILE_DIR}"], check=True)
      subprocess.run(["sudo", "chmod", "-R", "755", f"{SOCK_FILE_DIR}"], check=True)

      print("Gunicorn service created and started.")


def configure_ufw():
    print("Configuring UFW firewall...")

    # Retrieve the password from the environment variable
    SUDO_PASSWORD = os.getenv("SUDO_PASSWORD")

    if not SUDO_PASSWORD:
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
    GUNICORN_BINARY = os.getenv("GUNICORN_BINARY", "gunicorn")
    IP_PORT = os.getenv("IP_PORT")
    PROJECT_WSGI = os.getenv("PROJECT_WSGI", "chatbotAI.wsgi")
    VIRTUAL_ENV_PATH_FROM_USER_HOME = os.getenv("VIRTUAL_ENV_PATH_FROM_USER_HOME")
    VURTUAL_ENV_NAME = os.getenv("VIRTUAL_ENV_NAME")
    PROJECT_RUST_LIB_DIR = os.getnev("PROJECT_RUST_LIB_DIR")

    # Define the Dockerfile content dynamically using environment variables
    dockerfile_content = f"""# Stage 1: Builder
FROM python:3.12-slim AS builder

WORKDIR /app

# Install build tools and dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \\
    build-essential \\
    python3-dev \\
    libpq-dev \\
    libjpeg-dev \\
    zlib1g-dev \\
    curl \\
    graphviz \\
    graphviz-dev \\
    pkg-config \\
    libssl-dev \\
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Install the latest Rust toolchain using rustup
RUN curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y
ENV PATH="/root/.cargo/bin:$PATH"
# Verify Rust and Cargo versions (should be latest)
RUN rustc --version && cargo --version

# Set up the virtual environment (be carefull here we are in `app/` folder)
RUN python3 -m venv {VIRTUAL_ENV_NAME}
ENV PATH="/app/{VIRTUAL_ENV_NAME}/bin:$PATH"
ENV VIRTUAL_ENV="/app/{VIRTUAL_ENV_NAME}"

# Install Python dependencies
COPY requirements.txt .
RUN /app/{VIRTUAL_ENV_NAME}/bin/pip install --no-cache-dir -r requirements.txt

# Build rust
# Copy the Rust library source code
COPY ./{PROJECT_RUST_LIB_DIR} /app/{PROJECT_RUST_LIB_DIR}
# Build the Rust library using Maturin
WORKDIR /app/{PROJECT_RUST_LIB_DIR}
RUN maturin develop && \
    rm -rf /app/{PROJECT_RUST_LIB_DIR}/target /app/{PROJECT_RUST_LIB_DIR}/venv /app/{PROJECT_RUST_LIB_DIR}/__pycache__

# Stage 2: Final Image
FROM python:3.12-slim

# Install runtime dependencies needed for Django, PostgreSQL, and other packages
RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq-dev \
    libjpeg-dev \
    zlib1g-dev \
    libssl-dev \
    graphviz \
    curl \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Create user and group for running the application
RUN groupadd -r {GROUP} && useradd --no-log-init -r -g {GROUP} {USER}

# Copy virtual environment from the builder stage
COPY --from=builder /app/{VIRTUAL_ENV_NAME} {VIRTUAL_ENV_PATH_FROM_USER_HOME}

# Update PATH to use the virtual environment
ENV PATH="{VIRTUAL_ENV_PATH_FROM_USER_HOME}/bin:$PATH"

# Copy project files
COPY . {PROJECT_DIR}
# replace the rust_lib folder with the one that we have built in previous stage
# so we delete the one that we have copied and replace it with the one built fresh from previous stage
RUN rm -rf {PROJECT_DIR}/{PROJECT_RUST_LIB_DIR}
# we copy from `/app` folder to `home`
COPY --from=builder /app/{PROJECT_RUST_LIB_DIR} {PROJECT_DIR}/{PROJECT_RUST_LIB_DIR}

# Then we set permissions on home to `1000` uid user
RUN chown -R {USER}:{GROUP} /home

USER {USER}

WORKDIR {PROJECT_DIR}

# Define the command to run the application `"--log-level=debug"` can be moved out for prod when it works, `--preload` to make sure app loads before starting workers
CMD ["{VIRTUAL_ENV_PATH_FROM_USER_HOME}/bin/python", "-m", "{GUNICORN_BINARY}", "--workers=3","--log-level=debug", "-b", "{IP_PORT}", "{PROJECT_WSGI}:application", "--timeout", "300", "--preload",  "--forwarded-allow-ips='*'",  "--proxy-allow-from='*'"]"""

    # Write the Dockerfile to the project directory
    dockerfile_path = os.path.join(PROJECT_DIR, "Dockerfile")
    with open(dockerfile_path, "w") as dockerfile:
        dockerfile.write(dockerfile_content)

    print(f"Dockerfile created at {dockerfile_path}.")

def create_docker_compose():
    GUNICORN_CENTRAL_DIR = os.getenv("GUNICORN_CENTRAL_DIR")
    NGINX_IMAGE = os.getenv("NGINX_IMAGE")
    LOGS_FOLDER_PATH = os.getenv("LOGS_FOLDER_PATH")
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
      - .env # so env vars are injected int he docker environment
    volumes:
      - .env:/app/.env  # Mount the .env file at the right location socan be changed by updating .env file in server
      - ./gunicorn:{GUNICORN_CENTRAL_DIR}
    networks:
      - app_network

  nginx:
    image: {NGINX_IMAGE}
    ports:
      - "80:80"
    volumes:
      - {LOGS_FOLDER_PATH}:/var/log/nginx
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
        # install python3.12 and setup environment and installs requirements
        install_python_dependencies()
        # install postgresql {version} and enables service, installs pgvector
        install_postgresql()
        # create user, database, activates pgvector, permissions, hba config set to md5
        configure_postgresql()
        # setup ssl certificates self signed on domain `user.local` and updates `/etc/hosts` with `user.local`
        setup_ssl()
        # option to rotate ssl certificates and reloads nginx
        # rotate_ssl_certificates()
        # does collecti static, migration and copy static to nginx path with permissions for nginx
        prepare_django_app()
        # creates the gunicor log folder in root project directory
        Gunicorn.setup_gunicorn_center_dir()
        # create systemd `gunicorn.service` file and enables it to start django server through `chatbotAI.wsgi`
        Gunicorn.create_gunicorn_service()
        # setup nginx domain to serve django on `user.local` starts nginx service
        setup_nginx()
        # configures the `ufw` to have only port 80 and 443 (http and https) opened
        configure_ufw()
        # created a `Dockerfile` for the project but doesn't build it just create the file
        create_dockerfile()
        # creates a `docker-compose` file for the project but doesn't start stack has server `gunicorn`, database 'postgresql' with set version, proxy `nginx`, volumes and network
        create_docker_compose()
        print("Setup completed successfully.")
    except subprocess.CalledProcessError as e:
        print(f"An error occurred: {e}")

