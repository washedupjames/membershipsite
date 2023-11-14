release: python membersite/manage.py migrate
gunicorn --pythonpath membersite membersite.config.wsgi:application



