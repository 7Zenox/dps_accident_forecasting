# Use Python 3.11.9 slim-bullseye as the base image
FROM python:3.11.9-slim-bullseye

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set the working directory
WORKDIR /app

# Install system dependencies required for Prophet and other packages
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    build-essential \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements-prod.txt .
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements-prod.txt

# Copy the application code
COPY . .

# Expose the port if necessary (adjust as per your app's port)
EXPOSE 8000

# Command to run the application with Uvicorn
CMD ["python", "start-server.py"]