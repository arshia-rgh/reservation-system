#!/bin/sh

# Apply database migrations
python manage.py migrate

# Start Gunicorn server
exec gunicorn config.wsgi:application \
    --bind 0.0.0.0:8000 \
    --workers 3 \
    --timeout 120
