FROM python:3.12-slim

# System dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    curl \
    gnupg2 \
    unixodbc \
    unixodbc-dev \
    libpq-dev \
    libssl-dev \
    libsasl2-dev \
    build-essential \
    libffi-dev \
    libxml2-dev \
    libxmlsec1-dev \
    pkg-config \
    git \
    && rm -rf /var/lib/apt/lists/*

# Install ODBC Driver 17 for SQL Server
RUN curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add - && \
    curl https://packages.microsoft.com/config/debian/12/prod.list > /etc/apt/sources.list.d/mssql-release.list && \
    apt-get update && ACCEPT_EULA=Y apt-get install -y msodbcsql17

# Set working directory
WORKDIR /app

# Install Python dependencies
COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Copy project files
COPY . .

# Expose port (optional, for Flask apps)
EXPOSE 5000

# Run the app (adjust as needed)
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:app"]
