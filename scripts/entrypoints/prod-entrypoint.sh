#!/bin/sh

set -e  # Exit immediately if any command fails

. /app/.venv/bin/activate

./apply_migrations.sh

exec gunicorn --bind 0.0.0.0:8000 --workers 3 project_contributors_api.wsgi:application