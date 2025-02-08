#!/bin/sh

set -e

. /app/.venv/bin/activate

cd /app/project-contributors-api/

exec python manage.py runserver 0.0.0.0:8000