# Base image
FROM python:3.10-slim

# Set working directory to pipeline
WORKDIR /app/src/pipeline

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements.txt /app/requirements.txt
RUN pip install --upgrade pip && pip install --no-cache-dir -r /app/requirements.txt

# Copy entire source code
COPY . .

# Expose FastAPI port
EXPOSE 8002

# Run FastAPI from main.py (now inside pipeline folder)
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8002"]
