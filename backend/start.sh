#!/bin/bash

# Start Celery worker in the background
# We use -P solo to limit memory consumption on Render's free tier (512MB RAM limit)
celery -A celery_worker.celery worker --loglevel=info -P solo &

# Start Flask application in the foreground using Gunicorn
# Render passes the port in the $PORT environment variable
gunicorn run:app --bind 0.0.0.0:$PORT
