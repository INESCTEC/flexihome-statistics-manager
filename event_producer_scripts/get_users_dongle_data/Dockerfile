FROM python:3.8-alpine

WORKDIR /app

COPY . /app

RUN pip3 install requests==2.26.0

CMD [ "python3", "producer.py" ]