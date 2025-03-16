#!/bin/bash

# Exit on error
set -e

# Wait for PostgreSQL to be ready
echo "Waiting for PostgreSQL..."
while ! nc -z db 5432; do
  sleep 0.1
done
echo "PostgreSQL ready!"

# Apply database migrations
echo "Applying database migrations..."
python manage.py migrate

# Load example data if database is empty
PROFILE_COUNT=$(python -c "import django; django.setup(); from fivetool.models import SkillProfile; print(SkillProfile.objects.count())")
if [ "$PROFILE_COUNT" -eq "0" ]; then
  echo "Loading example data..."
  python add_example_data.py
fi

# Start server
echo "Starting server..."
exec "$@"