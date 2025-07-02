# Base image
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt

# Copy your full project into container
COPY . .

# Expose FastAPI port
EXPOSE 8002

# Start FastAPI app on port 8002
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8002"]
