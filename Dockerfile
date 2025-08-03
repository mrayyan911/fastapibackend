# Use an official Python runtime as a parent image
FROM python:3.11-slim

# Set the working directory in the container
WORKDIR /

# Set PYTHONPATH to include the /app directory
ENV PYTHONPATH=.

# Copy the requirements file into the container at /app
COPY ./requirements.txt /app/requirements.txt

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

# Copy the rest of the application's code into the container at /app
COPY ./app /app

# Ensure correct permissions for mounted files
RUN chmod -R 777 /app

# Expose port (not strictly required with docker-compose, but useful)
EXPOSE 8000

# Default command (can be overridden by docker-compose)
#CMD ["gunicorn", "-k", "uvicorn.workers.UvicornWorker", "app.main:app", "--bind", "0.0.0.0:8000", "--workers", "1"]
