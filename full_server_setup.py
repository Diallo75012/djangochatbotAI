#!/usr/bin/env python3
import os
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
SOCK_FILE_PATH=os.getenv("SOCK_FILE_PATH")
PROJECT_WSGI=os.getenv("PROJECT_WSGI")
GUNICORN_CENTRAL_DIR = os.getenv("GUNICORN_CENTRAL_DIR")
SSL_DIR = os.getenv("SSL_DIR")
NGINX_IMAGE = os.getenv("NGINX_IMAGE")
VIRTUAL_ENV_PATH_FROM_USER_HOME = os.getenv("VIRTUAL_ENV_PATH_FROM_USER_HOME")
NGINX_LOGS_FOLDER_PATH = os.getenv("NGINX_LOGS_FOLDER_PATH")

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


    DB_NAME = os.getenv("DB_NAME")
    DB_USER = os.getenv("DB_USER")
    DB_PASSWORD = os.getenv("DB_PASSWORD")
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

def setup_gunicorn_logs():
    GUNICORN_CENTRAL_DIR = os.getenv("GUNICORN_CENTRAL_DIR")
    os.makedirs(GUNICORN_CENTRAL_DIR, exist_ok=True)
    print(f"Gunicorn logs directory created at {GUNICORN_CENTRAL_DIR}")

def setup_ssl():
    import subprocess
    import os

    print("Setting up self-signed SSL certificate...")

    # Define the SSL directory (eg.: "/etc/ssl/creditizens")
    SSL_DIR = os.getenv("SSL_DIR")
    USER = os.getenv("USER")

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
    STATIC_DESTINATION = os.getenv("STATIC_DESTINATION")
    MEDIA_DESTINATION = os.getenv("MEDIA_DESTINATION")
    PROJECT_DIR = os.getenv("PROJECT_DIR")
    NGINX_LOGS_FOLDER_PATH = os.getenv("NGINX_LOGS_FOLDER_PATH")
    os.makedirs(NGINX_LOGS_FOLDER_PATH, exist_ok=True)
    subprocess.run(["sudo", "chown", f"{USER}:{GROUP}", NGINX_LOGS_FOLDER_PATH], check=True)

    nginx_conf = f"""### NGINX CONF
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
      alias {STATIC_DESTINATION};
      expires 30d;
      add_header Cache-Control "public, max-age=2592000";
  }}

  location /media/ {{
      alias {MEDIA_DESTINATION};
      expires 30d;
      add_header Cache-Control "public, max-age=2592000";
  }}


  error_log {os.path.join(NGINX_LOGS_FOLDER_PATH, 'error.log')};
  access_log {os.path.join(NGINX_LOGS_FOLDER_PATH, 'access.log')};
}}"""

    nginx_conf_path = f"/etc/nginx/sites-available/{USER}.local"
    nginx_symlink_path = "/etc/nginx/sites-enabled/{USER}.local"

    # Write Nginx configuration with sudo
    try:
        with open("/tmp/creditizens.local", "w") as temp_file:
            temp_file.write(nginx_conf)

        subprocess.run(["sudo", "mv", f"/tmp/{USER}.local", nginx_conf_path], check=True)
        subprocess.run(["sudo", "ln", "-sf", nginx_conf_path, nginx_symlink_path], check=True)
    except Exception as e:
        print(f"Error writing Nginx configuration: {e}")
        return

    # Restart Nginx to apply changes
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
    NGINX_USER = "www-data"  # Directly using www-data as confirmed from nginx.conf

    # Ensure the destination directories for static and media exist
    for destination in [STATIC_DESTINATION, MEDIA_DESTINATION]:
        if not os.path.exists(destination):
            subprocess.run(["sudo", "mkdir", "-p", destination], check=True)
        # Give ownership to the current user during preparation
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
    #subprocess.run(["sudo", "service", "gunicorn", "start"], check=True) # `service` way like `WSL2`
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

def create_docker_compose():
    GUNICORN_CENTRAL_DIR = os.getenv("GUNICORN_CENTRAL_DIR")
    NGINX_IMAGE = os.getenv("NGINX_IMAGE")
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
        # install python3.12 and setup environment and installs requirements
        #install_python_dependencies()
        # creates the gunicor log folder in root project directory
        #setup_gunicorn_logs()
        # install postgresql {version} and enables service, installs pgvector
        #install_postgresql()
        # create user, database, activates pgvector, permissions, hba config set to md5
        #configure_postgresql()
        # setup ssl certificates self signed on domain `user.local` and updates `/etc/hosts` with `user.local`
        setup_ssl()
        # option to rotate ssl certificates and reloads nginx
        #rotate_ssl_certificates()
        # setup nginx domain to serve django on `user.local` starts nginx service
        setup_nginx()
        # does collecti static, migration and copy static to nginx path with permissions for nginx
        prepare_django_app()
        # create systemd `gunicorn.service` file and enables it to start django server through `chatbotAI.wsgi`
        create_gunicorn_service()
        # configures the `ufw` to have only port 80 and 443 (http and https) opened
        configure_ufw()
        # created a `Dockerfile` for the project but doesn't build it just create the file
        create_dockerfile()
        # creates a `docker-compose` file for the project but doesn't start stack has server `gunicorn`, database 'postgresql' with set version, proxy `nginx`, volumes and network
        create_docker_compose()
        print("Setup completed successfully.")
    except subprocess.CalledProcessError as e:
        print(f"An error occurred: {e}")

