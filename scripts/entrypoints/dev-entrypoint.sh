#!/bin/sh

set -e  # Exit immediately if any command fails

. /app/.venv/bin/activate

cd $APP_DIR

../apply_migrations.sh

# For dev env only, continue even if it fails - when superuser already exists
export DJANGO_SUPERUSER_PASSWORD='admin'
python manage.py createsuperuser --username=admin --email=admin@admin.com --birth_year=1980 --first_name=Super --last_name=AdminUser --address=RandomStreet --country_code=GB --noinput || echo "Superuser already exists!"

exec python manage.py runserver 0.0.0.0:3000