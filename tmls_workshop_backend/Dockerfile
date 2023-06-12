FROM python:3.11-slim-buster
USER root

COPY . .

RUN pip install pipenv && pipenv install --system --deploy && chmod +x main.py

USER 1001
