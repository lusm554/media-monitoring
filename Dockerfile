FROM python:3.12-alpine

WORKDIR /app

COPY requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt

COPY backend.py .
COPY bot ./bot
COPY storage ./storage
COPY scraper ./scraper

CMD ["python3", "backend.py"]
