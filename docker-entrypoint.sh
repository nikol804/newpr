#!/usr/bin/env bash
set -e

# Wait for Postgres to be ready (if using docker-compose with postgres)
if [ -n "$DATABASE_HOST" ]; then
  until nc -z "$DATABASE_HOST" "$DATABASE_PORT"; do
    echo "Waiting for database $DATABASE_HOST:$DATABASE_PORT..."
    sleep 1
  done
fi

# Apply Django migrations and collect static files
python manage.py makemigrations --noinput
python manage.py migrate --noinput
python manage.py collectstatic --noinput

exec "$@"


