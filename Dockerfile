# Stage 1: Builder
FROM python:3.12-slim AS builder

WORKDIR /app

# Install build tools and dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    python3-dev \
    libpq-dev \
    libjpeg-dev \
    zlib1g-dev \
    curl \
    graphviz \
    graphviz-dev \
    pkg-config \
    libssl-dev \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Install the latest Rust toolchain using rustup
RUN curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y
ENV PATH="/root/.cargo/bin:$PATH"
# Verify Rust and Cargo versions (should be latest)
RUN rustc --version && cargo --version

# Set up the virtual environment
RUN python3 -m venv djangochatbotAI_venv
ENV PATH="/app/djangochatbotAI_venv/bin:$PATH"
ENV VIRTUAL_ENV="/app/djangochatbotAI_venv"

# Install Python dependencies
COPY requirements.txt .
RUN /app/djangochatbotAI_venv/bin/pip install --no-cache-dir -r requirements.txt

# Build rust
# Copy the Rust library source code
COPY ./rust_lib /app/rust_lib
# Build the Rust library using Maturin
WORKDIR /app/rust_lib
RUN maturin develop && \
    rm -rf /app/rust_lib/target /app/rust_lib/venv /app/rust_lib/__pycache__

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
RUN groupadd -r creditizens && useradd --no-log-init -r -g creditizens creditizens

# Copy virtual environment from the builder stage
COPY --from=builder /app/djangochatbotAI_venv /home/creditizens/djangochatAI/djangochatbotAI_venv

# Update PATH to use the virtual environment
ENV PATH="/home/creditizens/djangochatAI/djangochatbotAI_venv/bin:$PATH"

# Copy project files
COPY . /home/creditizens/djangochatAI/chatbotAI
# replace the rust_lib folder with the one that we have built in previous stage
RUN rm -rf /home/creditizens/djangochatAI/chatbotAI/rust_lib
# we copy from `/app` folder to `home`
COPY --from=builder /app/rust_lib /home/creditizens/djangochatAI/chatbotAI/rust_lib

# Copy and use entrypoint script
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /home/creditizens/djangochatAI/chatbotAI/entrypoint.sh

# Then we set permissions on home to `1000` uid user
RUN chown -R creditizens:creditizens /home

USER creditizens

WORKDIR /home/creditizens/djangochatAI/chatbotAI

ENTRYPOINT ["/home/creditizens/djangochatAI/chatbotAI/entrypoint.sh"]
# Define the command to run the application `"--log-level=debug"` can be moved out for prod when it works, `--preload` to make sure app loads before starting workers
# CMD ["/home/creditizens/djangochatAI/djangochatbotAI_venv/bin/python", "-m", "gunicorn", "--workers=3","--log-level=debug", "-b", "0.0.0.0:8000", "chatbotAI.wsgi:application", "--timeout", "300", "--preload",  "--forwarded-allow-ips='*'",  "--proxy-allow-from='*'"]
