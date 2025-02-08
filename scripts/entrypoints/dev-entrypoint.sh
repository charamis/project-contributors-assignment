#!/bin/sh

set -e  # Exit immediately if any command fails

. /app/.venv/bin/activate

cd $APP_DIR

../apply_migrations.sh

exec python manage.py runserver 0.0.0.0:8000