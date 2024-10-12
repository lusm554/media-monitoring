FROM python:3.12-slim

WORKDIR /app

RUN apt-get update
RUN apt-get install -y libpq-dev gcc
RUN apt-get install -y locales

COPY requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt

# For RU locale
RUN apt-get update && \
    apt-get install -y locales && \
    sed -i -e 's/# ru_RU.UTF-8 UTF-8/ru_RU.UTF-8 UTF-8/' /etc/locale.gen && \
    dpkg-reconfigure --frontend=noninteractive locales

ENV LANG ru_RU.UTF-8
ENV LC_ALL ru_RU.UTF-8

COPY backend.py .
COPY bot ./bot
COPY storage ./storage
COPY scraper_lib ./scraper_lib
COPY nlp ./nlp

RUN export LC_ALL=C

CMD ["python3", "backend.py"]
