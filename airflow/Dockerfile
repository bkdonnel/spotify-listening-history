FROM apache/airflow:2.8.1-python3.11

# Switch to root to modify group membership and install OS packages
USER root

# Add airflow user to the docker group (create group if needed)
RUN groupadd -f docker && usermod -aG docker airflow

# Install PostgreSQL client libraries and build tools
RUN apt-get update && apt-get install -y \
    libpq-dev \
    gcc \
 && apt-get clean \
 && rm -rf /var/lib/apt/lists/*

# Switch back to airflow BEFORE running pip install (Airflow requirement)
USER airflow

 # Copy and install Python dependencies
COPY requirements.txt /requirements.txt
RUN pip install --no-cache-dir -r /requirements.txt

