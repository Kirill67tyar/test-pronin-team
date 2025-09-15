#!/usr/bin/env bash

set -e

chown www-data:www-data /var/log

cd /opt/app && python manage.py migrate --noinput

python manage.py loaddata seed-file.json

# python manage.py collectstatic --noinput

# cp -r /opt/app/staticfiles/ /var/www/staticfiles/

python manage.py runserver 0.0.0.0:8000