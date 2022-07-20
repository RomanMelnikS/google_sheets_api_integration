#!/bin/sh
python -m pip install --upgrade pip

pip install -r requirements.txt

python manage.py collectstatic --noinput
python manage.py makemigrations google_sheets_service
python manage.py migrate

gunicorn config.wsgi:application --bind 0.0.0.0 --daemon

celery -A config worker -B --loglevel=info