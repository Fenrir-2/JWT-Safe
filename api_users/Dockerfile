FROM python:3.8.2-slim

RUN apt-get update && \
  apt-get install -y --no-install-recommends \
  gcc

ADD . /app
WORKDIR /app

RUN pip install -r requirements.txt
