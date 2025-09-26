# Use official Python slim image
FROM python:3.13-slim

# Set working directory
WORKDIR /app/server

# Install system dependencies for psycopg2 + bcrypt
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    gcc \
    curl \
    libffi-dev \
    libssl-dev \
    python3-dev \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Copy project files
COPY . .

# Upgrade pip and install Python dependencies
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Expose FastAPI port
EXPOSE 8000

# Command: wait for DB, run migrations, start FastAPI
CMD ["bash", "-c", "sleep 5 && python -m db.dbmigrations && uvicorn main:app --host 0.0.0.0 --port 8000 --reload"]
