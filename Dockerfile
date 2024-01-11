FROM docker.io/python:3.11.7-alpine as todo_bot_base

ENV \
    # python
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    \
    # pip
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100

WORKDIR /opt/app/src
COPY ./src/requirements.txt ./requirements.txt
RUN pip install -r ./requirements.txt

COPY ./src .
WORKDIR /opt/app/src

VOLUME db/

RUN \
    POSTGRES_DSN=postgres://user:password@repositories:5432/not-exist \
    TG_BOT_TOKEN=999
CMD python3 run.py
