# Use the official lightweight Python image.
FROM python:3.10.6-slim

# Allow statements and log messages to immediately appear in the Cloud Run logs
ENV PYTHONUNBUFFERED 1

# Create and change to the app directory.
WORKDIR /usr/src/app

# [CHANGE] Moved this COPY command earlier
# Copy local code to the container image.
COPY . ./

# Copy application dependency manifests to the container image.
COPY requirements.txt ./

# Install dependencies.
RUN pip install -r requirements.txt

# Run the web service on container startup.
CMD exec gunicorn --bind :$PORT --workers 1 --threads 8 --timeout 0 app:app


