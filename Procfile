release: python manage.py makemigrations
release: python manage.py migrate
web: gunicorn imagegallery.wsgi --log-file -
