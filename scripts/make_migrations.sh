#!/bin/sh

set -e  # Exit immediately if any command fails

cd $APP_DIR

python manage.py makemigrations