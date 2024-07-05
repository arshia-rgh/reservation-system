# Use an official Python runtime as a parent image
FROM python:3.12-alpine

# Set environment variables
# PYTHONDONTWRITEBYTECODE: Prevents Python from writing pyc files to disk
# PYTHONUNBUFFERED: Prevents Python from buffering stdout and stderr
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Install system dependencies
# apk update: Updates the package list
# apk add --no-cache: Installs the listed packages without caching them
RUN apk update && apk add --no-cache \
    build-base \
    libffi-dev \
    postgresql-dev \
    jpeg-dev \
    zlib-dev \
    libjpeg \
    libpng \
    libpq \
    gcc \
    musl-dev

# Set working directory in the container
# WORKDIR: Sets the working directory for any RUN, CMD, ENTRYPOINT, COPY, and ADD instructions that follow it in the Dockerfile
WORKDIR /app

# Copy requirements.txt file to the working directory
# COPY: Copies new files or directories from <src> and adds them to the container's filesystem at the path <dest>
COPY requirements.txt /app/

# Install any needed packages specified in requirements.txt
# RUN: Executes any commands in a new layer on top of the current image and commits the results
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copy the current directory contents into the container at /app
COPY . /app/

# Copy the entrypoint.sh file to the container
COPY entrypoint.sh /app/entrypoint.sh

# Change the permissions of the entrypoint.sh file to make it executable
# RUN: Executes any commands in a new layer on top of the current image and commits the results
RUN chmod +x /app/entrypoint.sh

# Collect static files using Django's manage.py
RUN python manage.py collectstatic --noinput

# Set the entrypoint for the container
# ENTRYPOINT: Allows you to configure a container that will run as an executable
ENTRYPOINT ["/app/entrypoint.sh"]