FROM huecker.io/library/python:3.11

ENV DST=/usr/src/app/ \
    POETRY_VIRTUALENVS_CREATE=false \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    POETRY_VERSION=1.7.1 \
    PYTHONPATH="/usr/src/app/src/common"

WORKDIR ${DST}

RUN apt update && apt install -y libsm6 libxext6
RUN apt-get install -y libxrender-dev
RUN apt-get install -y libgl1-mesa-glx

RUN apt-get update
RUN apt-get install -y ffmpeg

RUN pip3 install "poetry==$POETRY_VERSION"

COPY poetry.lock ./
COPY pyproject.toml ./

RUN poetry install --only main --no-interaction --no-root

COPY src/ ${DST}src
COPY models/ ${DST}models

RUN mkdir videos

CMD ["python3", "src/main.py"]