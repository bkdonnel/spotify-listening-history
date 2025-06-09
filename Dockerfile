# Use an official Python base image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy dependencies
COPY requirements.txt .

# Install dependencies globally in container
RUN pip install --no-cache-dir -r /app/requirements.txt

# Copy the rest of your code
COPY . .

# Run your main script
CMD ["python", "src/main.py"]
