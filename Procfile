web: gunicorn Shifty.wsgi:application --log-file -
worker: celery -A Shifty worker -l info --beat