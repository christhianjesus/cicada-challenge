# syntax=docker/dockerfile:1
FROM python:3.8.14-buster

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /usr/src/app
COPY requirements.txt /usr/src/app/
RUN pip install -r requirements.txt

COPY . /usr/src/app/
