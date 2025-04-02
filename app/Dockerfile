# Используем официальный образ Python
FROM python:3.9-slim

# Устанавливаем рабочую директорию внутри контейнера
WORKDIR /app

# Устанавливаем зависимости (если есть)
COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Копируем файлы проекта в контейнер
COPY . .

# Команда для запуска приложения
CMD ["python", "app.py"]
