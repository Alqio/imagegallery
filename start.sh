#!/bin/bash

echo "----- Collect static files ------ "
python manage.py collectstatic --noinput

echo "-----------Apply migration--------- "
python manage.py makemigrations
python manage.py migrate

echo "-----------Run gunicorn--------- "
gunicorn -b :5000 imagegallery.wsgi:application
