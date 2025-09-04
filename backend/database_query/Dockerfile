# Use official Python image
FROM python:3.11-slim

# Set work directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    libsqlite3-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy backend code
COPY . /app

# Install Python dependencies
# If you have requirements.txt, uncomment below and add the file
# COPY requirements.txt /app/
# RUN pip install --no-cache-dir -r requirements.txt
# For now, install Django and any other needed packages directly
RUN pip install --no-cache-dir django

# Expose port 8001
EXPOSE 8001

# Run migrations and start server
CMD ["sh", "-c", "python manage.py migrate && python manage.py runserver 0.0.0.0:8001"]
