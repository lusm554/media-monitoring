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

RUN apt-get install -y chromium
RUN apt-get install -y chromium-browser
#RUN apt-get install -y chromium-chromedriver

#RUN pip3 install --no-cache-dir webdriver-manager
#COPY install_chrome.py . 
#RUN python3 install_chrome.py

#RUN apt-get install -y gnupg2
#RUN apt-get install -y curl wget

# install google chrome
#RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add -
#RUN sh -c 'echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list'
#RUN apt-get -y update
#RUN apt-get install -y google-chrome-stable

# install chromedriver
#RUN apt-get install -yqq unzip
#RUN wget -O /tmp/chromedriver.zip http://chromedriver.storage.googleapis.com/`curl -sS chromedriver.storage.googleapis.com/LATEST_RELEASE`/chromedriver_linux64.zip
#RUN unzip /tmp/chromedriver.zip chromedriver -d /usr/local/bin/

# set display port to avoid crash
#ENV DISPLAY=:99

COPY backend.py .
COPY bot ./bot
COPY storage ./storage
COPY scraper_lib ./scraper_lib
COPY nlp ./nlp

RUN export LC_ALL=C

CMD ["python3", "backend.py"]
