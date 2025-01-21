# Stage 1: Builder
FROM python:3.12-slim as builder

WORKDIR /app

# Install build tools and dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    python3.12-dev \
    libpq-dev \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Set up the virtual environment
RUN python3 -m venv /home/creditizens/djangochatAI/chatbotAI/venv
ENV PATH="/home/creditizens/djangochatAI/chatbotAI/venv/bin:$PATH"

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Stage 2: Final Image
FROM python:3.12-slim

WORKDIR /app

# Create user and group for running the application
RUN groupadd -r creditizens && useradd --no-log-init -r -g creditizens creditizens

# Copy virtual environment from the builder stage
COPY --from=builder /home/creditizens/djangochatAI/chatbotAI/venv /home/creditizens/djangochatAI/chatbotAI/venv

# Update PATH to use the virtual environment
ENV PATH="/home/creditizens/djangochatAI/chatbotAI/venv/bin:$PATH"

# Copy project files
COPY . /home/creditizens/djangochatAI/chatbotAI

# Set permissions
RUN chown -R creditizens:creditizens /home/creditizens/djangochatAI/chatbotAI

USER creditizens

# Define the command to run the application
CMD ["/home/creditizens/djangochatAI/chatbotAI/venv/bin/gunicorn", "-b", "0.0.0.0:8000", "chatbotAI.wsgi:application"]