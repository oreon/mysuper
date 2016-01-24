web: gunicorn config.wsgi:application
worker: celery worker --app=mysuper.taskapp --loglevel=info
