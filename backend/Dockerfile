FROM python:3.13-slim

WORKDIR /app

# Устанавливаем Poetry
RUN pip install poetry

# Копируем ТОЛЬКО файлы зависимостей из папки backend
COPY backend/pyproject.toml backend/poetry.lock ./

# Устанавливаем зависимости Python
RUN poetry config virtualenvs.create false && \
    poetry install --no-root --no-interaction

# Копируем весь backend код
COPY backend/ .

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
