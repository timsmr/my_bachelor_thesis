FROM huecker.io/library/python:3.11

WORKDIR /app

COPY pyproject.toml poetry.lock ./

RUN apt update && apt install -y libsm6 libxext6
RUN apt-get install -y libxrender-dev
RUN apt-get install -y libgl1-mesa-glx

RUN apt-get update
RUN apt-get install -y ffmpeg

RUN pip install poetry && \
    poetry config virtualenvs.create false && \
    poetry install --only main

COPY . .

RUN mkdir videos

CMD ["poetry", "run", "python", "./src/main.py"]