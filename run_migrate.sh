#!/usr/bin/env bash

set -e

chown www-data:www-data /var/log

cd src/ && python manage.py migrate --noinput