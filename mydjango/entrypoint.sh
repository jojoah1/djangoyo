#!/bin/bash

# Ожидание доступности базы данных
echo "Waiting for database..."
while ! nc -z $POSTGRES_HOST $POSTGRES_PORT; do
  sleep 0.1
done
echo "Database started"

# Применение миграций
echo "Applying migrations..."
python manage.py makemigrations
python manage.py migrate

# Сбор статических файлов
echo "Collecting static files..."
python manage.py collectstatic --noinput

# Создание суперпользователя (опционально)
echo "Creating superuser..."
python manage.py shell -c "
from django.contrib.auth import get_user_model;
User = get_user_model();
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@admin.com', 'admin')
" || true

# Запуск сервера
echo "Starting server..."
exec gunicorn mydjango.wsgi:application --bind 0.0.0.0:8000 --workers 3