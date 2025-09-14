#!/bin/bash
set -e

# Ждать Redis и Postgres (nc из netcat-openbsd в Dockerfile)
until nc -z ${REDIS_HOST} ${REDIS_PORT}; do
    echo "Waiting for Redis at ${REDIS_HOST}:${REDIS_PORT}..."
    sleep 2
done
until nc -z ${POSTGRES_HOST} ${POSTGRES_PORT}; do
    echo "Waiting for Postgres at ${POSTGRES_HOST}:${POSTGRES_PORT}..."
    sleep 2
done

# Запуск
if [[ "${1}" == "celery" ]]; then
    celery -A core worker -l info
elif [[ "${1}" == "flower" ]]; then
    celery -A core flower
else
    echo "Usage: $0 {celery|flower}"
    exit 1
fi