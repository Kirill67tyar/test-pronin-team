#!/usr/bin/env bash

set -e

chown www-data:www-data /var/log

cd /opt/app && python manage.py migrate --noinput

python manage.py runserver 0.0.0.0:8000
