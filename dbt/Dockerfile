# Use official lightweight Python base image
FROM python:3.11-slim

# Set working directory
WORKDIR /usr/app

# Install system packages required for dbt + Snowflake
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    git \
    && rm -rf /var/lib/apt/lists/*

# Install dbt and Snowflake adapter from requirements.txt
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy dbt project files
COPY . .

# Keep container running unless overridden
CMD ["tail", "-f", "/dev/null"]
