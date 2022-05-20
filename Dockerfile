FROM python:3.10 AS base

RUN apt-get update && apt-get install -y gettext

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONFAULTHANDLER=1


FROM base AS builder

RUN pip install --upgrade pip

RUN pip install pipenv

WORKDIR /app

COPY Pipfile Pipfile.lock ./

RUN pipenv install --system --deploy --ignore-pipfile


FROM builder AS dev


FROM builder AS stage

RUN pip install uwsgi

COPY . .

RUN ./manage.py compilemessages
RUN ./manage.py collectstatic --noinput
