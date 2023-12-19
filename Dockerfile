FROM python:3.10-slim
WORKDIR /app
COPY . /app
RUN pip3 install -r requirements.txt
RUN ls
CMD ./run.sh
