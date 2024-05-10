# Используем официальный образ Python
FROM python:3.10

# Устанавливаем рабочую директорию внутри контейнера
WORKDIR /app

# Копируем файлы зависимостей и Poetry.lock
COPY pyproject.toml poetry.lock ./

RUN apt update && apt install -y libsm6 libxext6
RUN apt-get install -y libxrender-dev
RUN apt-get install -y libgl1-mesa-glx

RUN apt-get update
RUN apt-get install -y ffmpeg

# Устанавливаем Poetry
RUN pip install poetry

# Устанавливаем зависимости
RUN pip install poetry && \
    poetry config virtualenvs.create false && \
    poetry install --no-interaction --no-ansi

# Копируем исходный код
COPY . .


# Команда для запуска консольного приложения
CMD ["poetry", "run", "python", "main.py"]