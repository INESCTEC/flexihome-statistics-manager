FROM python:3.8-alpine

WORKDIR /app

COPY . /app

RUN pip3 install -r requirements.txt

CMD [ "python3", "input_dongle_raw_measurements.py" ]