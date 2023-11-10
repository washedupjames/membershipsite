release: python membersite/manage.py migrate
gunicorn --pythonpath membersite.config membersite.config.wsgi:application



