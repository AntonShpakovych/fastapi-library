FROM python:3.11

LABEL maintainer="a.shpakovych.work@gmail.com"

ENV PYTHONBUFFERED 1

WORKDIR /app

COPY requirements.txt requirements.txt

RUN apt-get update && apt-get install -y --no-install-recommends libpq-dev gcc wait-for-it

RUN pip install --no-cache-dir -r requirements.txt

COPY . .
