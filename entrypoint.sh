#!/bin/sh

# Apply database migrations
python manage.py migrate

# Create Superuser for django
python manage.py createsuperuser --noinput

# Collect static files using Django's manage.py
python manage.py collectstatic --noinput

# Start Gunicorn server
exec gunicorn config.wsgi:application \
    --bind 0.0.0.0:8000 \
    --workers 3 \
    --timeout 120 \
    --reload \
