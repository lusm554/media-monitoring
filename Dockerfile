FROM python:3.12-slim

WORKDIR /app

COPY backend.py .
COPY requirements.txt .
COPY bot ./bot
COPY storage ./storage
COPY scraper ./scraper

RUN ls

RUN pip3 install -r requirements.txt
CMD python3 backend.py
