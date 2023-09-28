# Use an official Python runtime as the base image
FROM python:3.9

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set the working directory in the container
WORKDIR /usr/src/app

# Копируем requirements.txt внутрь контейнера
COPY requirements.txt ./

# Обновляем pip и устанавливаем зависимости
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Копируем проектный код в рабочую директорию контейнера
COPY ../../.. ./

# Открываем порт для Django development server
EXPOSE 8000

# Запускаем Django development server
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]