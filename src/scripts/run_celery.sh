#!/bin/bash
set -e

if [[ "${1}" == "celery" ]]; then
    celery -A core worker -l info
elif [[ "${1}" == "flower" ]]; then
    celery -A core flower
else
    echo "Usage: $0 {celery|flower}"
    exit 1
fi
