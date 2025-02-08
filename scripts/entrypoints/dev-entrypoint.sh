#!/bin/sh

set -e  # Exit immediately if any command fails

. /app/.venv/bin/activate

cd $APP_DIR

../apply_migrations.sh

# For dev env only, continue even if it fails - when superuser already exists
python manage.py createsuperuser --username=admin --email=admin@admin.com --noinput || echo "Superuser already exists!"

exec python manage.py runserver 0.0.0.0:3000