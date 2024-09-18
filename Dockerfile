# Use an official Python runtime as a base image
FROM python:3.10-slim

COPY wait-for-db-start.sh /usr/local/bin/wait-for-db-start.sh
RUN chmod +x /usr/local/bin/wait-for-db-start.sh

RUN apt update && apt install -y mariadb-client

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set the working directory in the container
WORKDIR /app

LABEL org.opencontainers.image.source=https://github.com/MAtt5816/django-api-server

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    python3-dev \
    libpq-dev \
    pkg-config \
    default-libmysqlclient-dev \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt /app/
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Copy the Django project files into the container
COPY . /app/

# Expose port 8000 for the Django app
EXPOSE 8000

# Run migrations and start the Django development server
CMD ["sh", "-c", "wait-for-db-start.sh -- python manage.py runserver 0.0.0.0:8000"]
