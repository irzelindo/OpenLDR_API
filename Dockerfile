# Use an official Python image
FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set working directory
WORKDIR /app

# Install system dependencies (for pyodbc and other libs)
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    unixodbc-dev \
    build-essential \
    curl \
    gnupg2 \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Copy app code
COPY . .

# Expose port
EXPOSE 5000

# Start the app with gunicorn (use your main file/module if different)
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:app"]
