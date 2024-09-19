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

#RUN apt-get update -y && apt-get install -y wget xvfb unzip jq curl wget
#RUN apt-get install -y libxss1 libappindicator1 libgconf-2-4 \
#  fonts-liberation libasound2 libnspr4 libnss3 libx11-xcb1 libxtst6 lsb-release xdg-utils \
#  libgbm1 libnss3 libatk-bridge2.0-0 libgtk-3-0 libx11-xcb1 libxcb-dri3-0
#
#RUN curl --tlsv1 -s https://googlechromelabs.github.io/chrome-for-testing/last-known-good-versions-with-downloads.json > /tmp/versions.json
#
#RUN CHROME_URL=$(jq -r '.channels.Stable.downloads.chrome[] | select(.platform=="linux64") | .url' /tmp/versions.json) && \
#  wget -q --continue -O /tmp/chrome-linux64.zip $CHROME_URL && \
#  unzip /tmp/chrome-linux64.zip -d /opt/chrome
#
#RUN chmod +x /opt/chrome/chrome-linux64/chrome
#
#RUN CHROMEDRIVER_URL=$(jq -r '.channels.Stable.downloads.chromedriver[] | select(.platform=="linux64") | .url' /tmp/versions.json) && \
#  wget -q --continue -O /tmp/chromedriver-linux64.zip $CHROMEDRIVER_URL && \
#  unzip /tmp/chromedriver-linux64.zip -d /opt/chromedriver && \
#  chmod +x /opt/chromedriver/chromedriver-linux64/chromedriver
#
#ENV CHROMEDRIVER_DIR /opt/chromedriver
#ENV PATH $CHROMEDRIVER_DIR:$PATH
#
#RUN rm /tmp/chrome-linux64.zip /tmp/chromedriver-linux64.zip /tmp/versions.json

RUN pip3 install --no-cache-dir pdfminer.six

COPY backend.py .
COPY bot ./bot
COPY storage ./storage
COPY scraper_lib ./scraper_lib
COPY nlp ./nlp

RUN export LC_ALL=C

CMD ["python3", "backend.py"]
