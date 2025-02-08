#!/bin/sh

set -e

. /app/.venv/bin/activate

exec gunicorn --bind 0.0.0.0:8000 --workers 3 project_contributors_api.wsgi:application