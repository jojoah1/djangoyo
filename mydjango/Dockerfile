FROM python:3.11-slim

# Установка зависимостей включая netcat
RUN apt-get update && apt-get install -y \
    gcc \
    python3-dev \
    netcat-openbsd \
    && rm -rf /var/lib/apt/lists/* \
    && apt-get clean

# Создание рабочей директории
WORKDIR /app

# Копирование requirements.txt
COPY requirements.txt .

# Установка Python зависимостей
RUN pip install --no-cache-dir -r requirements.txt

# Копирование проекта
COPY . .

# Создание статической папки
RUN mkdir -p /app/static /app/media