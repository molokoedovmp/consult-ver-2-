# Используйте официальный образ Python
FROM python:3.10-slim

# Установите зависимости для операционной системы
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Установите рабочую директорию
WORKDIR /app

# Скопируйте файлы проекта в рабочую директорию
COPY . /app

# Установите зависимости Python
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Соберите статические файлы
RUN python manage.py collectstatic --noinput

# Примените миграции
RUN python manage.py makemigrations
RUN python manage.py migrate

# Откройте порт 8000 для доступа
EXPOSE 8000

# Запустите приложение
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
