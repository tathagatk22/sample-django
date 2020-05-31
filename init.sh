#!/bin/sh
set -e

/venv/bin/python /usr/src/app/sample-django/manage.py makemigrations

/venv/bin/python /usr/src/app/sample-django/manage.py migrate

/venv/bin/uwsgi --show-config

exit 0
