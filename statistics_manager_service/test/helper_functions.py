
from statistics_manager_service.config import Config
from statistics_manager_service import db

from datetime import datetime, timedelta, timezone
import influxdb_client
from influxdb_client.client.write_api import SYNCHRONOUS
from statistics_manager_service.models.database.db_models import (
    DBConfirmationToken,
    DBUserSettings,
    DBNotDisturbUser,
    DBUser,
    DBEvent,
    # DBNotDisturb,
)

from time import sleep
import uuid
import string
import secrets
import json

import requests

METER_ID = "NLV_CLIENT_8585"
METER_ID_WITHOUT_API_KEY = "NLV_CLIENT_9564"
API_KEY = "2J3R14CXJ18IWJ4T"


def clean_influxdb():
    client = influxdb_client.InfluxDBClient(
        url=f"http://{Config.INFLUX_URL}:{Config.INFLUX_PORT}",
        token=Config.INFLUX_TOKEN,
        org=Config.INFLUX_ORG
    )

    delete_api = client.delete_api()

    delete_api.delete(datetime.fromtimestamp(0).strftime("%Y-%m-%dT%H:%M:%S.%fZ"), datetime(2200, 1, 1, tzinfo=timezone.utc).strftime(
        "%Y-%m-%dT%H:%M:%S.%fZ"), '', bucket=Config.INFLUX_BUCKET, org=Config.INFLUX_ORG)
    
    
    return


def populate_influxdb_energy_imported():
    client = influxdb_client.InfluxDBClient(
        url=f"http://{Config.INFLUX_URL}:{Config.INFLUX_PORT}",
        token=Config.INFLUX_TOKEN,
        org=Config.INFLUX_ORG
    )

    write_api = client.write_api(write_options=SYNCHRONOUS)

    data = []

    # Daily
    data.append(influxdb_client.Point(API_KEY).field("energyImported", 19.1).time("2022-05-01T15:59:30+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("energyImported", 19.1).time("2022-05-01T23:59:30+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("energyImported", 20.3).time("2022-05-02T00:00:00+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("energyImported", 22.3).time("2022-05-02T00:01:00+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("energyImported", 25.3).time("2022-05-02T10:25:30+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("energyImported", 26.3).time("2022-05-02T23:50:30+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("energyImported", 28.9).time("2022-05-03T01:10:00+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("energyImported", 30.3).time("2022-05-03T23:25:30+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("energyImported", 33.3).time("2022-05-04T23:59:30+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("energyImported", 34.1).time("2022-05-05T03:00:30+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("energyImported", 38.3).time("2022-05-05T21:59:30+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("energyImported", 43.9).time("2022-05-06T05:45:30+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("energyImported", 45.5).time("2022-05-06T22:18:00+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("energyImported", 46.3).time("2022-05-07T01:00:30+00:00"))

    # Hourly
    data.append(influxdb_client.Point(API_KEY).field("energyImported", 20.3).time("2022-06-02T01:00:00+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("energyImported", 22.3).time("2022-06-02T01:01:00+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("energyImported", 25.3).time("2022-06-02T01:25:30+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("energyImported", 26.3).time("2022-06-02T01:59:30+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("energyImported", 28.9).time("2022-06-02T02:00:00+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("energyImported", 30.3).time("2022-06-02T02:15:30+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("energyImported", 33.3).time("2022-06-02T02:25:30+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("energyImported", 38.3).time("2022-06-02T02:50:30+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("energyImported", 40.1).time("2022-06-02T03:59:30+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("energyImported", 42.1).time("2022-06-02T04:00:30+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("energyImported", 45.1).time("2022-06-02T04:14:30+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("energyImported", 45.5).time("2022-06-02T04:29:30+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("energyImported", 46.1).time("2022-06-02T04:44:45+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("energyImported", 49.1).time("2022-06-02T04:56:30+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("energyImported", 52.1).time("2022-06-02T05:12:30+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("energyImported", 55.6).time("2022-06-02T05:24:30+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("energyImported", 57.5).time("2022-06-02T05:56:30+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("energyImported", 58.9).time("2022-06-02T06:12:30+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("energyImported", 62.4).time("2022-06-02T06:17:30+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("energyImported", 63.2).time("2022-06-02T06:59:30+00:00"))

    # 15min
    data.append(influxdb_client.Point(API_KEY).field("energyImported", 20.3).time("2022-07-02T01:00:00+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("energyImported", 22.3).time("2022-07-02T01:01:00+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("energyImported", 25.3).time("2022-07-02T01:16:30+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("energyImported", 26.3).time("2022-07-02T01:34:30+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("energyImported", 28.9).time("2022-07-02T01:47:00+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("energyImported", 30.3).time("2022-07-02T02:02:30+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("energyImported", 33.3).time("2022-07-02T02:25:30+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("energyImported", 38.3).time("2022-07-02T02:50:30+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("energyImported", 40.1).time("2022-07-02T03:00:00+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("energyImported", 42.3).time("2022-07-02T03:15:00+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("energyImported", 45.5).time("2022-07-02T03:17:30+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("energyImported", 48.2).time("2022-07-02T03:31:30+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("energyImported", 51.7).time("2022-07-02T03:59:30+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("energyImported", 53.4).time("2022-07-02T04:03:30+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("energyImported", 54.2).time("2022-07-02T04:18:30+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("energyImported", 58.7).time("2022-07-02T04:39:30+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("energyImported", 61.4).time("2022-07-02T05:03:30+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("energyImported", 65.6).time("2022-07-02T05:59:30+00:00"))

    # Weekly
    data.append(influxdb_client.Point(API_KEY).field("energyImported", 20.3).time("2022-08-01T01:00:00+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("energyImported", 22.3).time("2022-08-02T01:01:00+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("energyImported", 25.3).time("2022-08-03T01:16:30+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("energyImported", 26.3).time("2022-08-04T01:34:30+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("energyImported", 28.9).time("2022-08-04T01:47:00+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("energyImported", 30.3).time("2022-08-04T02:02:30+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("energyImported", 33.3).time("2022-08-07T02:25:30+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("energyImported", 38.3).time("2022-08-08T14:50:30+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("energyImported", 38.3).time("2022-08-08T19:50:30+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("energyImported", 40.1).time("2022-08-09T15:03:30+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("energyImported", 41.1).time("2022-08-10T12:03:30+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("energyImported", 42.1).time("2022-08-11T07:03:30+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("energyImported", 42.5).time("2022-08-12T02:03:30+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("energyImported", 45.6).time("2022-08-13T09:03:30+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("energyImported", 46.7).time("2022-08-14T02:03:30+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("energyImported", 47.2).time("2022-08-14T10:03:30+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("energyImported", 49.1).time("2022-08-14T20:03:30+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("energyImported", 50.7).time("2022-08-15T04:03:30+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("energyImported", 51.4).time("2022-08-15T10:03:30+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("energyImported", 51.6).time("2022-08-15T23:03:30+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("energyImported", 53.3).time("2022-08-16T15:03:30+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("energyImported", 56.7).time("2022-08-16T18:03:30+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("energyImported", 58.9).time("2022-08-16T19:03:30+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("energyImported", 59.2).time("2022-08-17T01:00:00+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("energyImported", 60.3).time("2022-08-18T01:01:00+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("energyImported", 61.4).time("2022-08-19T01:16:30+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("energyImported", 64.6).time("2022-08-20T01:34:30+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("energyImported", 65.8).time("2022-08-20T01:47:00+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("energyImported", 65.9).time("2022-08-20T02:02:30+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("energyImported", 66.3).time("2022-08-21T02:25:30+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("energyImported", 68.5).time("2022-08-22T14:50:30+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("energyImported", 69.2).time("2022-08-22T19:50:30+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("energyImported", 70.1).time("2022-08-23T15:03:30+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("energyImported", 70.8).time("2022-08-24T12:03:30+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("energyImported", 71.8).time("2022-08-25T07:03:30+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("energyImported", 72.4).time("2022-08-26T02:03:30+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("energyImported", 72.6).time("2022-08-27T09:03:30+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("energyImported", 75.5).time("2022-08-28T02:03:30+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("energyImported", 78.2).time("2022-08-28T10:03:30+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("energyImported", 79.7).time("2022-08-28T20:03:30+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("energyImported", 82.2).time("2022-08-29T04:03:30+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("energyImported", 84.6).time("2022-08-30T10:03:30+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("energyImported", 86.4).time("2022-08-31T11:03:30+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("energyImported", 88.8).time("2022-09-01T17:03:30+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("energyImported", 89.3).time("2022-09-03T13:03:30+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("energyImported", 92.2).time("2022-09-04T16:03:30+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("energyImported", 93.6).time("2022-09-05T02:03:30+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("energyImported", 93.9).time("2022-09-05T05:03:30+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("energyImported", 94.2).time("2022-09-06T14:03:30+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("energyImported", 96.4).time("2022-09-06T16:03:30+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("energyImported", 98.2).time("2022-09-07T12:03:30+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("energyImported", 99.5).time("2022-09-09T03:03:30+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("energyImported", 103.7).time("2022-09-10T09:03:30+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("energyImported", 103.9).time("2022-09-11T17:03:30+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("energyImported", 105.4).time("2022-09-15T06:03:30+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("energyImported", 107.3).time("2022-09-17T23:03:30+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("energyImported", 109.5).time("2022-09-18T13:03:30+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("energyImported", 110.8).time("2022-09-19T06:03:30+00:00"))

    # Monthly
    data.append(influxdb_client.Point(API_KEY).field("energyImported", 19.1).time("2021-01-01T23:59:30+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("energyImported", 20.3).time("2021-01-30T00:00:00+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("energyImported", 22.3).time("2021-02-02T00:01:00+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("energyImported", 25.3).time("2021-02-28T10:25:30+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("energyImported", 26.3).time("2021-03-02T23:50:30+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("energyImported", 28.9).time("2021-03-26T01:10:00+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("energyImported", 30.3).time("2021-04-03T23:25:30+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("energyImported", 33.3).time("2021-04-30T23:59:30+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("energyImported", 34.1).time("2021-05-15T03:00:30+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("energyImported", 38.3).time("2021-05-31T21:59:30+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("energyImported", 43.9).time("2021-06-01T05:45:30+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("energyImported", 45.3).time("2021-06-30T22:18:00+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("energyImported", 46.7).time("2021-07-06T01:00:30+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("energyImported", 48.2).time("2021-07-27T01:00:30+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("energyImported", 53.4).time("2021-08-01T01:00:30+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("energyImported", 55.7).time("2021-08-31T01:00:30+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("energyImported", 59.5).time("2021-09-24T01:00:30+00:00"))

    write_api.write(bucket=Config.INFLUX_BUCKET, org=Config.INFLUX_ORG, record=data)


def populate_influxdb_energy_exported():
    client = influxdb_client.InfluxDBClient(
        url=f"http://{Config.INFLUX_URL}:{Config.INFLUX_PORT}",
        token=Config.INFLUX_TOKEN,
        org=Config.INFLUX_ORG
    )

    write_api = client.write_api(write_options=SYNCHRONOUS)

    data = []

    # Daily
    data.append(influxdb_client.Point(API_KEY).field("energyExported", 19.1).time("2022-05-01T15:59:30+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("energyExported", 19.1).time("2022-05-01T23:59:30+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("energyExported", 20.3).time("2022-05-02T00:00:00+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("energyExported", 22.3).time("2022-05-02T00:01:00+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("energyExported", 25.3).time("2022-05-02T10:25:30+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("energyExported", 26.3).time("2022-05-02T23:50:30+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("energyExported", 28.9).time("2022-05-03T01:10:00+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("energyExported", 30.3).time("2022-05-03T23:25:30+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("energyExported", 33.3).time("2022-05-04T23:59:30+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("energyExported", 34.1).time("2022-05-05T03:00:30+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("energyExported", 38.3).time("2022-05-05T21:59:30+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("energyExported", 43.9).time("2022-05-06T05:45:30+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("energyExported", 45.5).time("2022-05-06T22:18:00+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("energyExported", 46.3).time("2022-05-07T01:00:30+00:00"))

    # Hourly
    data.append(influxdb_client.Point(API_KEY).field("energyExported", 20.3).time("2022-06-02T01:00:00+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("energyExported", 22.3).time("2022-06-02T01:01:00+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("energyExported", 25.3).time("2022-06-02T01:25:30+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("energyExported", 26.3).time("2022-06-02T01:59:30+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("energyExported", 28.9).time("2022-06-02T02:00:00+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("energyExported", 30.3).time("2022-06-02T02:15:30+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("energyExported", 33.3).time("2022-06-02T02:25:30+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("energyExported", 38.3).time("2022-06-02T02:50:30+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("energyExported", 40.1).time("2022-06-02T03:59:30+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("energyExported", 42.1).time("2022-06-02T04:00:30+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("energyExported", 45.1).time("2022-06-02T04:14:30+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("energyExported", 45.5).time("2022-06-02T04:29:30+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("energyExported", 46.1).time("2022-06-02T04:44:45+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("energyExported", 49.1).time("2022-06-02T04:56:30+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("energyExported", 52.1).time("2022-06-02T05:12:30+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("energyExported", 55.6).time("2022-06-02T05:24:30+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("energyExported", 57.5).time("2022-06-02T05:56:30+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("energyExported", 58.9).time("2022-06-02T06:12:30+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("energyExported", 62.4).time("2022-06-02T06:17:30+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("energyExported", 63.2).time("2022-06-02T06:59:30+00:00"))

    # 15min
    data.append(influxdb_client.Point(API_KEY).field("energyExported", 20.3).time("2022-07-02T01:00:00+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("energyExported", 22.3).time("2022-07-02T01:01:00+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("energyExported", 25.3).time("2022-07-02T01:16:30+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("energyExported", 26.3).time("2022-07-02T01:34:30+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("energyExported", 28.9).time("2022-07-02T01:47:00+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("energyExported", 30.3).time("2022-07-02T02:02:30+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("energyExported", 33.3).time("2022-07-02T02:25:30+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("energyExported", 38.3).time("2022-07-02T02:50:30+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("energyExported", 40.1).time("2022-07-02T03:00:00+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("energyExported", 42.3).time("2022-07-02T03:15:00+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("energyExported", 45.5).time("2022-07-02T03:17:30+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("energyExported", 48.2).time("2022-07-02T03:31:30+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("energyExported", 51.7).time("2022-07-02T03:59:30+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("energyExported", 53.4).time("2022-07-02T04:03:30+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("energyExported", 54.2).time("2022-07-02T04:18:30+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("energyExported", 58.7).time("2022-07-02T04:39:30+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("energyExported", 61.4).time("2022-07-02T05:03:30+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("energyExported", 65.6).time("2022-07-02T05:59:30+00:00"))

    # Weekly
    data.append(influxdb_client.Point(API_KEY).field("energyExported", 20.3).time("2022-08-01T01:00:00+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("energyExported", 22.3).time("2022-08-02T01:01:00+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("energyExported", 25.3).time("2022-08-03T01:16:30+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("energyExported", 26.3).time("2022-08-04T01:34:30+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("energyExported", 28.9).time("2022-08-04T01:47:00+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("energyExported", 30.3).time("2022-08-04T02:02:30+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("energyExported", 33.3).time("2022-08-07T02:25:30+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("energyExported", 38.3).time("2022-08-08T14:50:30+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("energyExported", 38.3).time("2022-08-08T19:50:30+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("energyExported", 40.1).time("2022-08-09T15:03:30+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("energyExported", 41.1).time("2022-08-10T12:03:30+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("energyExported", 42.1).time("2022-08-11T07:03:30+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("energyExported", 42.5).time("2022-08-12T02:03:30+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("energyExported", 45.6).time("2022-08-13T09:03:30+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("energyExported", 46.7).time("2022-08-14T02:03:30+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("energyExported", 47.2).time("2022-08-14T10:03:30+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("energyExported", 49.1).time("2022-08-14T20:03:30+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("energyExported", 50.7).time("2022-08-15T04:03:30+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("energyExported", 51.4).time("2022-08-15T10:03:30+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("energyExported", 51.6).time("2022-08-15T23:03:30+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("energyExported", 53.3).time("2022-08-16T15:03:30+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("energyExported", 56.7).time("2022-08-16T18:03:30+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("energyExported", 58.9).time("2022-08-16T19:03:30+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("energyExported", 59.2).time("2022-08-17T01:00:00+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("energyExported", 60.3).time("2022-08-18T01:01:00+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("energyExported", 61.4).time("2022-08-19T01:16:30+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("energyExported", 64.6).time("2022-08-20T01:34:30+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("energyExported", 65.8).time("2022-08-20T01:47:00+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("energyExported", 65.9).time("2022-08-20T02:02:30+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("energyExported", 66.3).time("2022-08-21T02:25:30+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("energyExported", 68.5).time("2022-08-22T14:50:30+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("energyExported", 69.2).time("2022-08-22T19:50:30+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("energyExported", 70.1).time("2022-08-23T15:03:30+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("energyExported", 70.8).time("2022-08-24T12:03:30+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("energyExported", 71.8).time("2022-08-25T07:03:30+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("energyExported", 72.4).time("2022-08-26T02:03:30+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("energyExported", 72.6).time("2022-08-27T09:03:30+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("energyExported", 75.5).time("2022-08-28T02:03:30+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("energyExported", 78.2).time("2022-08-28T10:03:30+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("energyExported", 79.7).time("2022-08-28T20:03:30+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("energyExported", 82.2).time("2022-08-29T04:03:30+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("energyExported", 84.6).time("2022-08-30T10:03:30+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("energyExported", 86.4).time("2022-08-31T11:03:30+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("energyExported", 88.8).time("2022-09-01T17:03:30+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("energyExported", 89.3).time("2022-09-03T13:03:30+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("energyExported", 92.2).time("2022-09-04T16:03:30+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("energyExported", 93.6).time("2022-09-05T02:03:30+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("energyExported", 93.9).time("2022-09-05T05:03:30+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("energyExported", 94.2).time("2022-09-06T14:03:30+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("energyExported", 96.4).time("2022-09-06T16:03:30+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("energyExported", 98.2).time("2022-09-07T12:03:30+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("energyExported", 99.5).time("2022-09-09T03:03:30+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("energyExported", 103.7).time("2022-09-10T09:03:30+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("energyExported", 103.9).time("2022-09-11T17:03:30+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("energyExported", 105.4).time("2022-09-15T06:03:30+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("energyExported", 107.3).time("2022-09-17T23:03:30+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("energyExported", 109.5).time("2022-09-18T13:03:30+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("energyExported", 110.8).time("2022-09-19T06:03:30+00:00"))

    # Monthly
    data.append(influxdb_client.Point(API_KEY).field("energyExported", 19.1).time("2021-01-01T23:59:30+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("energyExported", 20.3).time("2021-01-30T00:00:00+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("energyExported", 22.3).time("2021-02-02T00:01:00+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("energyExported", 25.3).time("2021-02-28T10:25:30+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("energyExported", 26.3).time("2021-03-02T23:50:30+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("energyExported", 28.9).time("2021-03-26T01:10:00+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("energyExported", 30.3).time("2021-04-03T23:25:30+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("energyExported", 33.3).time("2021-04-30T23:59:30+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("energyExported", 34.1).time("2021-05-15T03:00:30+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("energyExported", 38.3).time("2021-05-31T21:59:30+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("energyExported", 43.9).time("2021-06-01T05:45:30+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("energyExported", 45.3).time("2021-06-30T22:18:00+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("energyExported", 46.7).time("2021-07-06T01:00:30+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("energyExported", 48.2).time("2021-07-27T01:00:30+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("energyExported", 53.4).time("2021-08-01T01:00:30+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("energyExported", 55.7).time("2021-08-31T01:00:30+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("energyExported", 59.5).time("2021-09-24T01:00:30+00:00"))

    write_api.write(bucket=Config.INFLUX_BUCKET, org=Config.INFLUX_ORG, record=data)

def populate_influxdb_power_meter_imported():
    client = influxdb_client.InfluxDBClient(
        url=f"http://{Config.INFLUX_URL}:{Config.INFLUX_PORT}",
        token=Config.INFLUX_TOKEN,
        org=Config.INFLUX_ORG
    )

    write_api = client.write_api(write_options=SYNCHRONOUS)

    data = []
    # Daily
    data.append(influxdb_client.Point(METER_ID_WITHOUT_API_KEY).field("meterPowerImported", 19.1).time("2022-05-01T15:59:30+00:00"))
    data.append(influxdb_client.Point(METER_ID_WITHOUT_API_KEY).field("meterPowerImported", 19.1).time("2022-05-01T23:59:30+00:00"))
    data.append(influxdb_client.Point(METER_ID_WITHOUT_API_KEY).field("meterPowerImported", 20.3).time("2022-05-02T00:00:00+00:00"))
    data.append(influxdb_client.Point(METER_ID_WITHOUT_API_KEY).field("meterPowerImported", 22.3).time("2022-05-02T00:01:00+00:00"))
    data.append(influxdb_client.Point(METER_ID_WITHOUT_API_KEY).field("meterPowerImported", 25.3).time("2022-05-02T10:25:30+00:00"))
    data.append(influxdb_client.Point(METER_ID_WITHOUT_API_KEY).field("meterPowerImported", 26.3).time("2022-05-02T23:50:30+00:00"))
    data.append(influxdb_client.Point(METER_ID_WITHOUT_API_KEY).field("meterPowerImported", 28.9).time("2022-05-03T01:10:00+00:00"))
    data.append(influxdb_client.Point(METER_ID_WITHOUT_API_KEY).field("meterPowerImported", 30.3).time("2022-05-03T23:25:30+00:00"))
    data.append(influxdb_client.Point(METER_ID_WITHOUT_API_KEY).field("meterPowerImported", 33.3).time("2022-05-04T23:59:30+00:00"))
    data.append(influxdb_client.Point(METER_ID_WITHOUT_API_KEY).field("meterPowerImported", 34.1).time("2022-05-05T03:00:30+00:00"))
    data.append(influxdb_client.Point(METER_ID_WITHOUT_API_KEY).field("meterPowerImported", 38.3).time("2022-05-05T21:59:30+00:00"))
    data.append(influxdb_client.Point(METER_ID_WITHOUT_API_KEY).field("meterPowerImported", 43.9).time("2022-05-06T05:45:30+00:00"))
    data.append(influxdb_client.Point(METER_ID_WITHOUT_API_KEY).field("meterPowerImported", 45.5).time("2022-05-06T22:18:00+00:00"))
    data.append(influxdb_client.Point(METER_ID_WITHOUT_API_KEY).field("meterPowerImported", 46.3).time("2022-05-07T01:00:30+00:00"))

    # Hourly
    data.append(influxdb_client.Point(METER_ID_WITHOUT_API_KEY).field("meterPowerImported", 20.3).time("2022-06-02T01:00:00+00:00"))
    data.append(influxdb_client.Point(METER_ID_WITHOUT_API_KEY).field("meterPowerImported", 22.3).time("2022-06-02T01:01:00+00:00"))
    data.append(influxdb_client.Point(METER_ID_WITHOUT_API_KEY).field("meterPowerImported", 25.3).time("2022-06-02T01:25:30+00:00"))
    data.append(influxdb_client.Point(METER_ID_WITHOUT_API_KEY).field("meterPowerImported", 26.3).time("2022-06-02T01:59:30+00:00"))
    data.append(influxdb_client.Point(METER_ID_WITHOUT_API_KEY).field("meterPowerImported", 28.9).time("2022-06-02T02:00:00+00:00"))
    data.append(influxdb_client.Point(METER_ID_WITHOUT_API_KEY).field("meterPowerImported", 30.3).time("2022-06-02T02:15:30+00:00"))
    data.append(influxdb_client.Point(METER_ID_WITHOUT_API_KEY).field("meterPowerImported", 33.3).time("2022-06-02T02:25:30+00:00"))
    data.append(influxdb_client.Point(METER_ID_WITHOUT_API_KEY).field("meterPowerImported", 38.3).time("2022-06-02T02:50:30+00:00"))
    data.append(influxdb_client.Point(METER_ID_WITHOUT_API_KEY).field("meterPowerImported", 40.1).time("2022-06-02T03:59:30+00:00"))
    # data.append(influxdb_client.Point(METER_ID_WITHOUT_API_KEY).field("meterPowerImported", 42.1).time("2022-06-02T04:00:30+00:00"))
    # data.append(influxdb_client.Point(METER_ID_WITHOUT_API_KEY).field("meterPowerImported", 45.1).time("2022-06-02T04:14:30+00:00"))
    # data.append(influxdb_client.Point(METER_ID_WITHOUT_API_KEY).field("meterPowerImported", 45.5).time("2022-06-02T04:29:30+00:00"))
    # data.append(influxdb_client.Point(METER_ID_WITHOUT_API_KEY).field("meterPowerImported", 46.1).time("2022-06-02T04:44:45+00:00"))
    # data.append(influxdb_client.Point(METER_ID_WITHOUT_API_KEY).field("meterPowerImported", 49.1).time("2022-06-02T04:56:30+00:00"))
    data.append(influxdb_client.Point(METER_ID_WITHOUT_API_KEY).field("meterPowerImported", 52.1).time("2022-06-02T05:12:30+00:00"))
    data.append(influxdb_client.Point(METER_ID_WITHOUT_API_KEY).field("meterPowerImported", 55.6).time("2022-06-02T05:24:30+00:00"))
    data.append(influxdb_client.Point(METER_ID_WITHOUT_API_KEY).field("meterPowerImported", 57.5).time("2022-06-02T05:56:30+00:00"))
    data.append(influxdb_client.Point(METER_ID_WITHOUT_API_KEY).field("meterPowerImported", 58.9).time("2022-06-02T06:12:30+00:00"))
    data.append(influxdb_client.Point(METER_ID_WITHOUT_API_KEY).field("meterPowerImported", 62.4).time("2022-06-02T06:17:30+00:00"))
    data.append(influxdb_client.Point(METER_ID_WITHOUT_API_KEY).field("meterPowerImported", 63.2).time("2022-06-02T06:59:30+00:00"))

    # 15min
    data.append(influxdb_client.Point(METER_ID_WITHOUT_API_KEY).field("meterPowerImported", 20.3).time("2022-07-02T01:00:00+00:00"))
    data.append(influxdb_client.Point(METER_ID_WITHOUT_API_KEY).field("meterPowerImported", 22.3).time("2022-07-02T01:01:00+00:00"))
    data.append(influxdb_client.Point(METER_ID_WITHOUT_API_KEY).field("meterPowerImported", 25.3).time("2022-07-02T01:16:30+00:00"))
    data.append(influxdb_client.Point(METER_ID_WITHOUT_API_KEY).field("meterPowerImported", 26.3).time("2022-07-02T01:34:30+00:00"))
    data.append(influxdb_client.Point(METER_ID_WITHOUT_API_KEY).field("meterPowerImported", 28.9).time("2022-07-02T01:47:00+00:00"))
    data.append(influxdb_client.Point(METER_ID_WITHOUT_API_KEY).field("meterPowerImported", 30.3).time("2022-07-02T02:02:30+00:00"))
    data.append(influxdb_client.Point(METER_ID_WITHOUT_API_KEY).field("meterPowerImported", 33.3).time("2022-07-02T02:25:30+00:00"))
    data.append(influxdb_client.Point(METER_ID_WITHOUT_API_KEY).field("meterPowerImported", 38.3).time("2022-07-02T02:50:30+00:00"))
    data.append(influxdb_client.Point(METER_ID_WITHOUT_API_KEY).field("meterPowerImported", 40.1).time("2022-07-02T03:00:00+00:00"))
    data.append(influxdb_client.Point(METER_ID_WITHOUT_API_KEY).field("meterPowerImported", 42.3).time("2022-07-02T03:15:00+00:00"))
    data.append(influxdb_client.Point(METER_ID_WITHOUT_API_KEY).field("meterPowerImported", 45.5).time("2022-07-02T03:17:30+00:00"))
    data.append(influxdb_client.Point(METER_ID_WITHOUT_API_KEY).field("meterPowerImported", 48.2).time("2022-07-02T03:31:30+00:00"))
    data.append(influxdb_client.Point(METER_ID_WITHOUT_API_KEY).field("meterPowerImported", 51.7).time("2022-07-02T03:59:30+00:00"))
    data.append(influxdb_client.Point(METER_ID_WITHOUT_API_KEY).field("meterPowerImported", 53.4).time("2022-07-02T04:03:30+00:00"))
    data.append(influxdb_client.Point(METER_ID_WITHOUT_API_KEY).field("meterPowerImported", 54.2).time("2022-07-02T04:18:30+00:00"))
    data.append(influxdb_client.Point(METER_ID_WITHOUT_API_KEY).field("meterPowerImported", 58.7).time("2022-07-02T04:39:30+00:00"))
    data.append(influxdb_client.Point(METER_ID_WITHOUT_API_KEY).field("meterPowerImported", 61.4).time("2022-07-02T05:03:30+00:00"))
    data.append(influxdb_client.Point(METER_ID_WITHOUT_API_KEY).field("meterPowerImported", 65.6).time("2022-07-02T05:59:30+00:00"))

    # Weekly
    data.append(influxdb_client.Point(METER_ID_WITHOUT_API_KEY).field("meterPowerImported", 20.3).time("2022-08-01T01:00:00+00:00"))
    data.append(influxdb_client.Point(METER_ID_WITHOUT_API_KEY).field("meterPowerImported", 22.3).time("2022-08-02T01:01:00+00:00"))
    data.append(influxdb_client.Point(METER_ID_WITHOUT_API_KEY).field("meterPowerImported", 25.3).time("2022-08-03T01:16:30+00:00"))
    data.append(influxdb_client.Point(METER_ID_WITHOUT_API_KEY).field("meterPowerImported", 26.3).time("2022-08-04T01:34:30+00:00"))
    data.append(influxdb_client.Point(METER_ID_WITHOUT_API_KEY).field("meterPowerImported", 28.9).time("2022-08-04T01:47:00+00:00"))
    data.append(influxdb_client.Point(METER_ID_WITHOUT_API_KEY).field("meterPowerImported", 30.3).time("2022-08-04T02:02:30+00:00"))
    data.append(influxdb_client.Point(METER_ID_WITHOUT_API_KEY).field("meterPowerImported", 33.3).time("2022-08-07T02:25:30+00:00"))
    data.append(influxdb_client.Point(METER_ID_WITHOUT_API_KEY).field("meterPowerImported", 38.3).time("2022-08-08T14:50:30+00:00"))
    data.append(influxdb_client.Point(METER_ID_WITHOUT_API_KEY).field("meterPowerImported", 38.3).time("2022-08-08T19:50:30+00:00"))
    data.append(influxdb_client.Point(METER_ID_WITHOUT_API_KEY).field("meterPowerImported", 40.1).time("2022-08-09T15:03:30+00:00"))
    data.append(influxdb_client.Point(METER_ID_WITHOUT_API_KEY).field("meterPowerImported", 41.1).time("2022-08-10T12:03:30+00:00"))
    data.append(influxdb_client.Point(METER_ID_WITHOUT_API_KEY).field("meterPowerImported", 42.1).time("2022-08-11T07:03:30+00:00"))
    data.append(influxdb_client.Point(METER_ID_WITHOUT_API_KEY).field("meterPowerImported", 42.5).time("2022-08-12T02:03:30+00:00"))
    data.append(influxdb_client.Point(METER_ID_WITHOUT_API_KEY).field("meterPowerImported", 45.6).time("2022-08-13T09:03:30+00:00"))
    data.append(influxdb_client.Point(METER_ID_WITHOUT_API_KEY).field("meterPowerImported", 46.7).time("2022-08-14T02:03:30+00:00"))
    data.append(influxdb_client.Point(METER_ID_WITHOUT_API_KEY).field("meterPowerImported", 47.2).time("2022-08-14T10:03:30+00:00"))
    data.append(influxdb_client.Point(METER_ID_WITHOUT_API_KEY).field("meterPowerImported", 49.1).time("2022-08-14T20:03:30+00:00"))
    data.append(influxdb_client.Point(METER_ID_WITHOUT_API_KEY).field("meterPowerImported", 50.7).time("2022-08-15T04:03:30+00:00"))
    data.append(influxdb_client.Point(METER_ID_WITHOUT_API_KEY).field("meterPowerImported", 51.4).time("2022-08-15T10:03:30+00:00"))
    data.append(influxdb_client.Point(METER_ID_WITHOUT_API_KEY).field("meterPowerImported", 51.6).time("2022-08-15T23:03:30+00:00"))
    data.append(influxdb_client.Point(METER_ID_WITHOUT_API_KEY).field("meterPowerImported", 53.3).time("2022-08-16T15:03:30+00:00"))
    data.append(influxdb_client.Point(METER_ID_WITHOUT_API_KEY).field("meterPowerImported", 56.7).time("2022-08-16T18:03:30+00:00"))
    data.append(influxdb_client.Point(METER_ID_WITHOUT_API_KEY).field("meterPowerImported", 58.9).time("2022-08-16T19:03:30+00:00"))
    data.append(influxdb_client.Point(METER_ID_WITHOUT_API_KEY).field("meterPowerImported", 59.2).time("2022-08-17T01:00:00+00:00"))
    data.append(influxdb_client.Point(METER_ID_WITHOUT_API_KEY).field("meterPowerImported", 60.3).time("2022-08-18T01:01:00+00:00"))
    data.append(influxdb_client.Point(METER_ID_WITHOUT_API_KEY).field("meterPowerImported", 61.4).time("2022-08-19T01:16:30+00:00"))
    data.append(influxdb_client.Point(METER_ID_WITHOUT_API_KEY).field("meterPowerImported", 64.6).time("2022-08-20T01:34:30+00:00"))
    data.append(influxdb_client.Point(METER_ID_WITHOUT_API_KEY).field("meterPowerImported", 65.8).time("2022-08-20T01:47:00+00:00"))
    data.append(influxdb_client.Point(METER_ID_WITHOUT_API_KEY).field("meterPowerImported", 65.9).time("2022-08-20T02:02:30+00:00"))
    data.append(influxdb_client.Point(METER_ID_WITHOUT_API_KEY).field("meterPowerImported", 66.3).time("2022-08-21T02:25:30+00:00"))
    data.append(influxdb_client.Point(METER_ID_WITHOUT_API_KEY).field("meterPowerImported", 68.5).time("2022-08-22T14:50:30+00:00"))
    data.append(influxdb_client.Point(METER_ID_WITHOUT_API_KEY).field("meterPowerImported", 69.2).time("2022-08-22T19:50:30+00:00"))
    data.append(influxdb_client.Point(METER_ID_WITHOUT_API_KEY).field("meterPowerImported", 70.1).time("2022-08-23T15:03:30+00:00"))
    data.append(influxdb_client.Point(METER_ID_WITHOUT_API_KEY).field("meterPowerImported", 70.8).time("2022-08-24T12:03:30+00:00"))
    data.append(influxdb_client.Point(METER_ID_WITHOUT_API_KEY).field("meterPowerImported", 71.8).time("2022-08-25T07:03:30+00:00"))
    data.append(influxdb_client.Point(METER_ID_WITHOUT_API_KEY).field("meterPowerImported", 72.4).time("2022-08-26T02:03:30+00:00"))
    data.append(influxdb_client.Point(METER_ID_WITHOUT_API_KEY).field("meterPowerImported", 72.6).time("2022-08-27T09:03:30+00:00"))
    data.append(influxdb_client.Point(METER_ID_WITHOUT_API_KEY).field("meterPowerImported", 75.5).time("2022-08-28T02:03:30+00:00"))
    data.append(influxdb_client.Point(METER_ID_WITHOUT_API_KEY).field("meterPowerImported", 78.2).time("2022-08-28T10:03:30+00:00"))
    data.append(influxdb_client.Point(METER_ID_WITHOUT_API_KEY).field("meterPowerImported", 79.7).time("2022-08-28T20:03:30+00:00"))
    data.append(influxdb_client.Point(METER_ID_WITHOUT_API_KEY).field("meterPowerImported", 82.2).time("2022-08-29T04:03:30+00:00"))
    data.append(influxdb_client.Point(METER_ID_WITHOUT_API_KEY).field("meterPowerImported", 84.6).time("2022-08-30T10:03:30+00:00"))
    data.append(influxdb_client.Point(METER_ID_WITHOUT_API_KEY).field("meterPowerImported", 86.4).time("2022-08-31T11:03:30+00:00"))
    data.append(influxdb_client.Point(METER_ID_WITHOUT_API_KEY).field("meterPowerImported", 88.8).time("2022-09-01T17:03:30+00:00"))
    data.append(influxdb_client.Point(METER_ID_WITHOUT_API_KEY).field("meterPowerImported", 89.3).time("2022-09-03T13:03:30+00:00"))
    data.append(influxdb_client.Point(METER_ID_WITHOUT_API_KEY).field("meterPowerImported", 92.2).time("2022-09-04T16:03:30+00:00"))
    data.append(influxdb_client.Point(METER_ID_WITHOUT_API_KEY).field("meterPowerImported", 93.6).time("2022-09-05T02:03:30+00:00"))
    data.append(influxdb_client.Point(METER_ID_WITHOUT_API_KEY).field("meterPowerImported", 93.9).time("2022-09-05T05:03:30+00:00"))
    data.append(influxdb_client.Point(METER_ID_WITHOUT_API_KEY).field("meterPowerImported", 94.2).time("2022-09-06T14:03:30+00:00"))
    data.append(influxdb_client.Point(METER_ID_WITHOUT_API_KEY).field("meterPowerImported", 96.4).time("2022-09-06T16:03:30+00:00"))
    data.append(influxdb_client.Point(METER_ID_WITHOUT_API_KEY).field("meterPowerImported", 98.2).time("2022-09-07T12:03:30+00:00"))
    data.append(influxdb_client.Point(METER_ID_WITHOUT_API_KEY).field("meterPowerImported", 99.5).time("2022-09-09T03:03:30+00:00"))
    data.append(influxdb_client.Point(METER_ID_WITHOUT_API_KEY).field("meterPowerImported", 103.7).time("2022-09-10T09:03:30+00:00"))
    data.append(influxdb_client.Point(METER_ID_WITHOUT_API_KEY).field("meterPowerImported", 103.9).time("2022-09-11T17:03:30+00:00"))
    data.append(influxdb_client.Point(METER_ID_WITHOUT_API_KEY).field("meterPowerImported", 105.4).time("2022-09-15T06:03:30+00:00"))
    data.append(influxdb_client.Point(METER_ID_WITHOUT_API_KEY).field("meterPowerImported", 107.3).time("2022-09-17T23:03:30+00:00"))
    data.append(influxdb_client.Point(METER_ID_WITHOUT_API_KEY).field("meterPowerImported", 109.5).time("2022-09-18T13:03:30+00:00"))
    data.append(influxdb_client.Point(METER_ID_WITHOUT_API_KEY).field("meterPowerImported", 110.8).time("2022-09-19T06:03:30+00:00"))

    # Monthly
    data.append(influxdb_client.Point(METER_ID_WITHOUT_API_KEY).field("meterPowerImported", 19.1).time("2021-01-01T23:59:30+00:00"))
    data.append(influxdb_client.Point(METER_ID_WITHOUT_API_KEY).field("meterPowerImported", 20.3).time("2021-01-30T00:00:00+00:00"))
    data.append(influxdb_client.Point(METER_ID_WITHOUT_API_KEY).field("meterPowerImported", 22.3).time("2021-02-02T00:01:00+00:00"))
    data.append(influxdb_client.Point(METER_ID_WITHOUT_API_KEY).field("meterPowerImported", 25.3).time("2021-02-28T10:25:30+00:00"))
    data.append(influxdb_client.Point(METER_ID_WITHOUT_API_KEY).field("meterPowerImported", 26.3).time("2021-03-02T23:50:30+00:00"))
    data.append(influxdb_client.Point(METER_ID_WITHOUT_API_KEY).field("meterPowerImported", 28.9).time("2021-03-26T01:10:00+00:00"))
    data.append(influxdb_client.Point(METER_ID_WITHOUT_API_KEY).field("meterPowerImported", 30.3).time("2021-04-03T23:25:30+00:00"))
    data.append(influxdb_client.Point(METER_ID_WITHOUT_API_KEY).field("meterPowerImported", 33.3).time("2021-04-30T23:59:30+00:00"))
    data.append(influxdb_client.Point(METER_ID_WITHOUT_API_KEY).field("meterPowerImported", 34.1).time("2021-05-15T03:00:30+00:00"))
    data.append(influxdb_client.Point(METER_ID_WITHOUT_API_KEY).field("meterPowerImported", 38.3).time("2021-05-31T21:59:30+00:00"))
    data.append(influxdb_client.Point(METER_ID_WITHOUT_API_KEY).field("meterPowerImported", 43.9).time("2021-06-01T05:45:30+00:00"))
    data.append(influxdb_client.Point(METER_ID_WITHOUT_API_KEY).field("meterPowerImported", 45.3).time("2021-06-30T22:18:00+00:00"))
    data.append(influxdb_client.Point(METER_ID_WITHOUT_API_KEY).field("meterPowerImported", 46.7).time("2021-07-06T01:00:30+00:00"))
    data.append(influxdb_client.Point(METER_ID_WITHOUT_API_KEY).field("meterPowerImported", 48.2).time("2021-07-27T01:00:30+00:00"))
    data.append(influxdb_client.Point(METER_ID_WITHOUT_API_KEY).field("meterPowerImported", 53.4).time("2021-08-01T01:00:30+00:00"))
    data.append(influxdb_client.Point(METER_ID_WITHOUT_API_KEY).field("meterPowerImported", 55.7).time("2021-08-31T01:00:30+00:00"))
    data.append(influxdb_client.Point(METER_ID_WITHOUT_API_KEY).field("meterPowerImported", 59.5).time("2021-09-24T01:00:30+00:00"))

    write_api.write(bucket=Config.INFLUX_BUCKET, org=Config.INFLUX_ORG, record=data)


def populate_influxdb_power_imported():
    client = influxdb_client.InfluxDBClient(
        url=f"http://{Config.INFLUX_URL}:{Config.INFLUX_PORT}",
        token=Config.INFLUX_TOKEN,
        org=Config.INFLUX_ORG
    )

    write_api = client.write_api(write_options=SYNCHRONOUS)

    data = []

    # Daily
    data.append(influxdb_client.Point(API_KEY).field("powerImported", 164.6).time("2022-05-01T06:55:29+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("powerImported", 2687.5).time("2022-05-01T14:31:22+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("powerImported", 2060.0).time("2022-05-01T22:07:46+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("powerImported", 827.8).time("2022-05-02T01:17:03+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("powerImported", 1150.0).time("2022-05-02T09:13:19+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("powerImported", 2120.0).time("2022-05-02T17:40:33+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("powerImported", 1615.1).time("2022-05-03T02:10:57+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("powerImported", 712.2).time("2022-05-03T06:45:11+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("powerImported", 1006.9).time("2022-05-03T12:48:55+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("powerImported", 1633.1).time("2022-05-03T18:16:10+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("powerImported", 290.2).time("2022-05-04T01:33:48+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("powerImported", 488.4).time("2022-05-04T05:49:48+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("powerImported", 400.3).time("2022-05-04T16:09:27+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("powerImported", 1541.9).time("2022-05-04T17:38:24+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("powerImported", 1835.3).time("2022-05-04T23:56:29+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("powerImported", 814.5).time("2022-05-05T10:09:46+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("powerImported", 2789.0).time("2022-05-05T14:19:21+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("powerImported", 84.7).time("2022-05-05T16:59:43+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("powerImported", 717.5).time("2022-05-05T19:25:24+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("powerImported", 3395.8).time("2022-05-05T22:14:24+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("powerImported", 1910.0).time("2022-05-06T04:55:07+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("powerImported", 1409.1).time("2022-05-06T08:13:43+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("powerImported", 768.9).time("2022-05-06T17:04:40+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("powerImported", 2016.3).time("2022-05-07T02:03:21+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("powerImported", 1851.4).time("2022-05-07T05:06:51+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("powerImported", 2999.7).time("2022-05-07T10:37:05+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("powerImported", 2360.7).time("2022-05-07T18:23:15+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("powerImported", 504.5).time("2022-05-07T23:04:01+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("powerImported", 3350.9).time("2022-05-08T04:28:00+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("powerImported", 512.2).time("2022-05-08T12:09:07+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("powerImported", 422.1).time("2022-05-08T21:15:14+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("powerImported", 2111.4).time("2022-05-09T02:44:48+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("powerImported", 890.3).time("2022-05-09T04:54:52+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("powerImported", 881.8).time("2022-05-09T08:27:33+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("powerImported", 248.4).time("2022-05-09T10:40:07+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("powerImported", 2580.6).time("2022-05-09T20:17:06+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("powerImported", 471.4).time("2022-05-10T06:04:30+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("powerImported", 3323.3).time("2022-05-10T16:45:15+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("powerImported", 2925.0).time("2022-05-10T18:28:44+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("powerImported", 84.4).time("2022-05-10T23:43:03+00:00"))

    # Hourly
    data.append(influxdb_client.Point(API_KEY).field("powerImported", 1489.6).time("2022-06-01T01:12:38+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("powerImported", 829.5).time("2022-06-01T01:43:48+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("powerImported", 3285.8).time("2022-06-01T02:15:43+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("powerImported", 2941.2).time("2022-06-01T02:57:02+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("powerImported", 423.5).time("2022-06-01T03:46:36+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("powerImported", 2632.8).time("2022-06-01T04:13:57+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("powerImported", 3290.2).time("2022-06-01T04:22:32+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("powerImported", 1984.4).time("2022-06-01T05:03:27+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("powerImported", 2502.4).time("2022-06-01T05:37:15+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("powerImported", 1008.9).time("2022-06-01T05:51:38+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("powerImported", 2070.1).time("2022-06-01T06:02:20+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("powerImported", 3015.3).time("2022-06-01T06:35:23+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("powerImported", 165.3).time("2022-06-01T06:59:15+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("powerImported", 1375.1).time("2022-06-01T07:21:41+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("powerImported", 2633.1).time("2022-06-01T07:42:49+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("powerImported", 1792.8).time("2022-06-01T07:46:59+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("powerImported", 3317.3).time("2022-06-01T08:29:52+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("powerImported", 3447.5).time("2022-06-01T09:12:49+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("powerImported", 1046.9).time("2022-06-01T09:55:50+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("powerImported", 1887.8).time("2022-06-01T10:05:23+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("powerImported", 2708.9).time("2022-06-01T10:19:38+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("powerImported", 2895.2).time("2022-06-01T10:30:06+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("powerImported", 1963.6).time("2022-06-01T11:18:04+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("powerImported", 3378.1).time("2022-06-01T11:33:05+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("powerImported", 2939.6).time("2022-06-01T11:36:04+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("powerImported", 3021.9).time("2022-06-01T12:13:09+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("powerImported", 1295.1).time("2022-06-01T12:31:22+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("powerImported", 1565.2).time("2022-06-01T13:14:08+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("powerImported", 1793.2).time("2022-06-01T13:50:12+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("powerImported", 2069.6).time("2022-06-01T14:17:25+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("powerImported", 655.2).time("2022-06-01T15:02:53+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("powerImported", 1521.8).time("2022-06-01T15:45:37+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("powerImported", 1069.6).time("2022-06-01T16:32:34+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("powerImported", 189.1).time("2022-06-01T17:12:53+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("powerImported", 3094.9).time("2022-06-01T18:01:14+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("powerImported", 1278.0).time("2022-06-01T18:34:32+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("powerImported", 2182.7).time("2022-06-01T18:44:41+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("powerImported", 657.5).time("2022-06-01T18:57:46+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("powerImported", 2632.2).time("2022-06-01T19:20:19+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("powerImported", 1401.2).time("2022-06-01T19:38:03+00:00"))

    # 15min
    data.append(influxdb_client.Point(API_KEY).field("powerImported", 2730.3).time("2022-07-01T01:02:39+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("powerImported", 2292.7).time("2022-07-01T01:04:16+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("powerImported", 248.8).time("2022-07-01T01:12:23+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("powerImported", 549.4).time("2022-07-01T01:24:06+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("powerImported", 2124.0).time("2022-07-01T01:27:26+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("powerImported", 1110.5).time("2022-07-01T01:38:32+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("powerImported", 2161.7).time("2022-07-01T01:43:44+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("powerImported", 714.7).time("2022-07-01T01:54:45+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("powerImported", 2877.1).time("2022-07-01T02:04:11+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("powerImported", 1202.5).time("2022-07-01T02:08:17+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("powerImported", 3116.8).time("2022-07-01T02:12:33+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("powerImported", 293.6).time("2022-07-01T02:23:19+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("powerImported", 2485.2).time("2022-07-01T02:25:37+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("powerImported", 3115.8).time("2022-07-01T02:27:44+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("powerImported", 1658.6).time("2022-07-01T02:30:24+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("powerImported", 2119.7).time("2022-07-01T02:40:40+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("powerImported", 1742.1).time("2022-07-01T02:51:16+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("powerImported", 2380.8).time("2022-07-01T03:01:51+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("powerImported", 2137.7).time("2022-07-01T03:04:52+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("powerImported", 1611.8).time("2022-07-01T03:11:06+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("powerImported", 3127.4).time("2022-07-01T03:16:21+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("powerImported", 1911.4).time("2022-07-01T03:19:14+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("powerImported", 2743.1).time("2022-07-01T03:22:22+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("powerImported", 1160.3).time("2022-07-01T03:32:28+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("powerImported", 2924.9).time("2022-07-01T03:37:57+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("powerImported", 1384.4).time("2022-07-01T03:46:26+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("powerImported", 1744.5).time("2022-07-01T03:49:48+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("powerImported", 3479.8).time("2022-07-01T03:59:04+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("powerImported", 846.6).time("2022-07-01T04:10:16+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("powerImported", 2240.7).time("2022-07-01T04:11:44+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("powerImported", 2532.1).time("2022-07-01T04:15:44+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("powerImported", 3015.2).time("2022-07-01T04:20:30+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("powerImported", 1435.8).time("2022-07-01T04:24:36+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("powerImported", 3079.5).time("2022-07-01T04:28:44+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("powerImported", 459.5).time("2022-07-01T04:34:03+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("powerImported", 1343.1).time("2022-07-01T04:40:28+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("powerImported", 2138.4).time("2022-07-01T04:50:36+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("powerImported", 212.9).time("2022-07-01T04:57:26+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("powerImported", 340.6).time("2022-07-01T05:02:01+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("powerImported", 200.4).time("2022-07-01T05:11:10+00:00"))

    # Weekly
    data.append(influxdb_client.Point(API_KEY).field("powerImported", 2779.4).time("2022-08-06T00:02:01+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("powerImported", 809.3).time("2022-08-08T21:04:44+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("powerImported", 3094.6).time("2022-08-13T18:33:13+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("powerImported", 742.7).time("2022-08-17T01:42:09+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("powerImported", 1203.7).time("2022-08-21T03:34:17+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("powerImported", 3341.3).time("2022-08-23T13:42:43+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("powerImported", 520.2).time("2022-08-27T13:29:13+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("powerImported", 2793.2).time("2022-09-01T00:37:44+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("powerImported", 2209.1).time("2022-09-04T02:13:59+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("powerImported", 183.0).time("2022-09-08T20:47:19+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("powerImported", 3421.0).time("2022-09-11T08:07:48+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("powerImported", 422.4).time("2022-09-13T14:45:27+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("powerImported", 1255.3).time("2022-09-18T12:04:59+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("powerImported", 2059.8).time("2022-09-22T07:16:53+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("powerImported", 2099.6).time("2022-09-26T23:28:32+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("powerImported", 435.0).time("2022-09-29T17:14:54+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("powerImported", 1278.1).time("2022-10-03T17:09:36+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("powerImported", 2671.4).time("2022-10-07T03:21:00+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("powerImported", 3402.2).time("2022-10-10T01:49:27+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("powerImported", 1922.4).time("2022-10-13T04:22:11+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("powerImported", 3336.8).time("2022-10-17T22:02:20+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("powerImported", 2333.1).time("2022-10-19T23:57:07+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("powerImported", 3405.0).time("2022-10-24T10:51:00+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("powerImported", 1921.9).time("2022-10-27T09:33:33+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("powerImported", 1232.4).time("2022-10-29T23:32:45+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("powerImported", 905.1).time("2022-11-02T01:43:29+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("powerImported", 218.1).time("2022-11-04T18:29:51+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("powerImported", 1144.3).time("2022-11-08T01:06:54+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("powerImported", 633.0).time("2022-11-10T12:49:44+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("powerImported", 2478.2).time("2022-11-15T03:21:59+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("powerImported", 2043.5).time("2022-11-17T18:38:55+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("powerImported", 3337.8).time("2022-11-22T05:40:18+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("powerImported", 1521.7).time("2022-11-26T11:14:58+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("powerImported", 2611.8).time("2022-11-30T22:46:29+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("powerImported", 338.3).time("2022-12-04T22:14:59+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("powerImported", 1988.3).time("2022-12-08T02:57:32+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("powerImported", 3247.6).time("2022-12-12T14:56:24+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("powerImported", 3274.1).time("2022-12-17T13:00:34+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("powerImported", 2094.7).time("2022-12-19T15:52:58+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("powerImported", 879.4).time("2022-12-23T13:00:51+00:00"))

    # Monthly
    data.append(influxdb_client.Point(API_KEY).field("powerImported", 2274.2).time("2021-01-07T03:32:00+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("powerImported", 2002.1).time("2021-01-13T11:14:50+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("powerImported", 471.7).time("2021-01-20T02:09:09+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("powerImported", 1979.6).time("2021-01-26T10:07:38+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("powerImported", 3326.4).time("2021-02-01T19:27:58+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("powerImported", 2570.8).time("2021-02-07T21:14:30+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("powerImported", 2168.8).time("2021-02-13T09:41:52+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("powerImported", 159.9).time("2021-02-26T05:53:44+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("powerImported", 2643.2).time("2021-03-10T04:01:36+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("powerImported", 1290.0).time("2021-03-20T17:42:43+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("powerImported", 3361.7).time("2021-03-26T12:21:27+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("powerImported", 2454.5).time("2021-04-04T07:11:55+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("powerImported", 3134.5).time("2021-04-09T18:09:01+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("powerImported", 3137.0).time("2021-04-15T23:31:57+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("powerImported", 1217.1).time("2021-04-25T02:28:32+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("powerImported", 2238.7).time("2021-05-06T13:14:53+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("powerImported", 1736.9).time("2021-05-14T10:16:48+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("powerImported", 1855.1).time("2021-05-25T20:52:05+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("powerImported", 409.6).time("2021-06-04T00:48:12+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("powerImported", 111.2).time("2021-06-15T18:54:42+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("powerImported", 3273.7).time("2021-06-22T10:27:41+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("powerImported", 1258.8).time("2021-07-05T03:45:10+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("powerImported", 568.6).time("2021-07-17T10:56:53+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("powerImported", 1244.5).time("2021-07-29T09:51:57+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("powerImported", 623.6).time("2021-08-08T00:45:47+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("powerImported", 168.4).time("2021-08-16T02:29:19+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("powerImported", 418.3).time("2021-08-21T13:33:18+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("powerImported", 1254.6).time("2021-08-31T11:18:57+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("powerImported", 729.5).time("2021-09-08T21:05:37+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("powerImported", 2895.0).time("2021-09-19T13:30:49+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("powerImported", 1964.4).time("2021-09-27T18:06:05+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("powerImported", 2086.6).time("2021-10-03T17:06:02+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("powerImported", 3485.0).time("2021-10-16T13:45:45+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("powerImported", 2868.9).time("2021-10-28T08:47:21+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("powerImported", 2172.0).time("2021-11-03T17:38:53+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("powerImported", 3450.1).time("2021-11-11T11:24:12+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("powerImported", 217.3).time("2021-11-21T12:03:27+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("powerImported", 1106.3).time("2021-11-27T18:44:56+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("powerImported", 243.7).time("2021-12-03T11:20:13+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("powerImported", 1726.7).time("2021-12-15T06:15:24+00:00"))

    write_api.write(bucket=Config.INFLUX_BUCKET, org=Config.INFLUX_ORG, record=data)


def populate_influxdb_power_exported():
    client = influxdb_client.InfluxDBClient(
        url=f"http://{Config.INFLUX_URL}:{Config.INFLUX_PORT}",
        token=Config.INFLUX_TOKEN,
        org=Config.INFLUX_ORG
    )

    write_api = client.write_api(write_options=SYNCHRONOUS)

    data = []

    # Daily
    data.append(influxdb_client.Point(API_KEY).field("powerExported", 164.6).time("2022-05-01T06:55:29+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("powerExported", 2687.5).time("2022-05-01T14:31:22+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("powerExported", 2060.0).time("2022-05-01T22:07:46+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("powerExported", 827.8).time("2022-05-02T01:17:03+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("powerExported", 1150.0).time("2022-05-02T09:13:19+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("powerExported", 2120.0).time("2022-05-02T17:40:33+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("powerExported", 1615.1).time("2022-05-03T02:10:57+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("powerExported", 712.2).time("2022-05-03T06:45:11+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("powerExported", 1006.9).time("2022-05-03T12:48:55+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("powerExported", 1633.1).time("2022-05-03T18:16:10+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("powerExported", 290.2).time("2022-05-04T01:33:48+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("powerExported", 488.4).time("2022-05-04T05:49:48+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("powerExported", 400.3).time("2022-05-04T16:09:27+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("powerExported", 1541.9).time("2022-05-04T17:38:24+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("powerExported", 1835.3).time("2022-05-04T23:56:29+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("powerExported", 814.5).time("2022-05-05T10:09:46+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("powerExported", 2789.0).time("2022-05-05T14:19:21+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("powerExported", 84.7).time("2022-05-05T16:59:43+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("powerExported", 717.5).time("2022-05-05T19:25:24+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("powerExported", 3395.8).time("2022-05-05T22:14:24+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("powerExported", 1910.0).time("2022-05-06T04:55:07+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("powerExported", 1409.1).time("2022-05-06T08:13:43+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("powerExported", 768.9).time("2022-05-06T17:04:40+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("powerExported", 2016.3).time("2022-05-07T02:03:21+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("powerExported", 1851.4).time("2022-05-07T05:06:51+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("powerExported", 2999.7).time("2022-05-07T10:37:05+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("powerExported", 2360.7).time("2022-05-07T18:23:15+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("powerExported", 504.5).time("2022-05-07T23:04:01+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("powerExported", 3350.9).time("2022-05-08T04:28:00+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("powerExported", 512.2).time("2022-05-08T12:09:07+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("powerExported", 422.1).time("2022-05-08T21:15:14+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("powerExported", 2111.4).time("2022-05-09T02:44:48+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("powerExported", 890.3).time("2022-05-09T04:54:52+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("powerExported", 881.8).time("2022-05-09T08:27:33+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("powerExported", 248.4).time("2022-05-09T10:40:07+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("powerExported", 2580.6).time("2022-05-09T20:17:06+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("powerExported", 471.4).time("2022-05-10T06:04:30+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("powerExported", 3323.3).time("2022-05-10T16:45:15+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("powerExported", 2925.0).time("2022-05-10T18:28:44+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("powerExported", 84.4).time("2022-05-10T23:43:03+00:00"))

    # Hourly
    data.append(influxdb_client.Point(API_KEY).field("powerExported", 1489.6).time("2022-06-01T01:12:38+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("powerExported", 829.5).time("2022-06-01T01:43:48+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("powerExported", 3285.8).time("2022-06-01T02:15:43+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("powerExported", 2941.2).time("2022-06-01T02:57:02+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("powerExported", 423.5).time("2022-06-01T03:46:36+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("powerExported", 2632.8).time("2022-06-01T04:13:57+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("powerExported", 3290.2).time("2022-06-01T04:22:32+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("powerExported", 1984.4).time("2022-06-01T05:03:27+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("powerExported", 2502.4).time("2022-06-01T05:37:15+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("powerExported", 1008.9).time("2022-06-01T05:51:38+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("powerExported", 2070.1).time("2022-06-01T06:02:20+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("powerExported", 3015.3).time("2022-06-01T06:35:23+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("powerExported", 165.3).time("2022-06-01T06:59:15+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("powerExported", 1375.1).time("2022-06-01T07:21:41+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("powerExported", 2633.1).time("2022-06-01T07:42:49+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("powerExported", 1792.8).time("2022-06-01T07:46:59+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("powerExported", 3317.3).time("2022-06-01T08:29:52+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("powerExported", 3447.5).time("2022-06-01T09:12:49+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("powerExported", 1046.9).time("2022-06-01T09:55:50+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("powerExported", 1887.8).time("2022-06-01T10:05:23+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("powerExported", 2708.9).time("2022-06-01T10:19:38+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("powerExported", 2895.2).time("2022-06-01T10:30:06+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("powerExported", 1963.6).time("2022-06-01T11:18:04+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("powerExported", 3378.1).time("2022-06-01T11:33:05+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("powerExported", 2939.6).time("2022-06-01T11:36:04+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("powerExported", 3021.9).time("2022-06-01T12:13:09+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("powerExported", 1295.1).time("2022-06-01T12:31:22+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("powerExported", 1565.2).time("2022-06-01T13:14:08+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("powerExported", 1793.2).time("2022-06-01T13:50:12+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("powerExported", 2069.6).time("2022-06-01T14:17:25+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("powerExported", 655.2).time("2022-06-01T15:02:53+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("powerExported", 1521.8).time("2022-06-01T15:45:37+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("powerExported", 1069.6).time("2022-06-01T16:32:34+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("powerExported", 189.1).time("2022-06-01T17:12:53+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("powerExported", 3094.9).time("2022-06-01T18:01:14+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("powerExported", 1278.0).time("2022-06-01T18:34:32+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("powerExported", 2182.7).time("2022-06-01T18:44:41+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("powerExported", 657.5).time("2022-06-01T18:57:46+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("powerExported", 2632.2).time("2022-06-01T19:20:19+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("powerExported", 1401.2).time("2022-06-01T19:38:03+00:00"))

    # 15min
    data.append(influxdb_client.Point(API_KEY).field("powerExported", 2730.3).time("2022-07-01T01:02:39+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("powerExported", 2292.7).time("2022-07-01T01:04:16+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("powerExported", 248.8).time("2022-07-01T01:12:23+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("powerExported", 549.4).time("2022-07-01T01:24:06+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("powerExported", 2124.0).time("2022-07-01T01:27:26+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("powerExported", 1110.5).time("2022-07-01T01:38:32+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("powerExported", 2161.7).time("2022-07-01T01:43:44+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("powerExported", 714.7).time("2022-07-01T01:54:45+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("powerExported", 2877.1).time("2022-07-01T02:04:11+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("powerExported", 1202.5).time("2022-07-01T02:08:17+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("powerExported", 3116.8).time("2022-07-01T02:12:33+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("powerExported", 293.6).time("2022-07-01T02:23:19+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("powerExported", 2485.2).time("2022-07-01T02:25:37+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("powerExported", 3115.8).time("2022-07-01T02:27:44+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("powerExported", 1658.6).time("2022-07-01T02:30:24+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("powerExported", 2119.7).time("2022-07-01T02:40:40+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("powerExported", 1742.1).time("2022-07-01T02:51:16+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("powerExported", 2380.8).time("2022-07-01T03:01:51+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("powerExported", 2137.7).time("2022-07-01T03:04:52+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("powerExported", 1611.8).time("2022-07-01T03:11:06+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("powerExported", 3127.4).time("2022-07-01T03:16:21+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("powerExported", 1911.4).time("2022-07-01T03:19:14+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("powerExported", 2743.1).time("2022-07-01T03:22:22+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("powerExported", 1160.3).time("2022-07-01T03:32:28+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("powerExported", 2924.9).time("2022-07-01T03:37:57+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("powerExported", 1384.4).time("2022-07-01T03:46:26+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("powerExported", 1744.5).time("2022-07-01T03:49:48+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("powerExported", 3479.8).time("2022-07-01T03:59:04+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("powerExported", 846.6).time("2022-07-01T04:10:16+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("powerExported", 2240.7).time("2022-07-01T04:11:44+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("powerExported", 2532.1).time("2022-07-01T04:15:44+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("powerExported", 3015.2).time("2022-07-01T04:20:30+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("powerExported", 1435.8).time("2022-07-01T04:24:36+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("powerExported", 3079.5).time("2022-07-01T04:28:44+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("powerExported", 459.5).time("2022-07-01T04:34:03+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("powerExported", 1343.1).time("2022-07-01T04:40:28+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("powerExported", 2138.4).time("2022-07-01T04:50:36+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("powerExported", 212.9).time("2022-07-01T04:57:26+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("powerExported", 340.6).time("2022-07-01T05:02:01+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("powerExported", 200.4).time("2022-07-01T05:11:10+00:00"))

    # Weekly
    data.append(influxdb_client.Point(API_KEY).field("powerExported", 2779.4).time("2022-08-06T00:02:01+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("powerExported", 809.3).time("2022-08-08T21:04:44+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("powerExported", 3094.6).time("2022-08-13T18:33:13+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("powerExported", 742.7).time("2022-08-17T01:42:09+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("powerExported", 1203.7).time("2022-08-21T03:34:17+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("powerExported", 3341.3).time("2022-08-23T13:42:43+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("powerExported", 520.2).time("2022-08-27T13:29:13+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("powerExported", 2793.2).time("2022-09-01T00:37:44+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("powerExported", 2209.1).time("2022-09-04T02:13:59+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("powerExported", 183.0).time("2022-09-08T20:47:19+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("powerExported", 3421.0).time("2022-09-11T08:07:48+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("powerExported", 422.4).time("2022-09-13T14:45:27+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("powerExported", 1255.3).time("2022-09-18T12:04:59+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("powerExported", 2059.8).time("2022-09-22T07:16:53+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("powerExported", 2099.6).time("2022-09-26T23:28:32+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("powerExported", 435.0).time("2022-09-29T17:14:54+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("powerExported", 1278.1).time("2022-10-03T17:09:36+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("powerExported", 2671.4).time("2022-10-07T03:21:00+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("powerExported", 3402.2).time("2022-10-10T01:49:27+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("powerExported", 1922.4).time("2022-10-13T04:22:11+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("powerExported", 3336.8).time("2022-10-17T22:02:20+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("powerExported", 2333.1).time("2022-10-19T23:57:07+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("powerExported", 3405.0).time("2022-10-24T10:51:00+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("powerExported", 1921.9).time("2022-10-27T09:33:33+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("powerExported", 1232.4).time("2022-10-29T23:32:45+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("powerExported", 905.1).time("2022-11-02T01:43:29+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("powerExported", 218.1).time("2022-11-04T18:29:51+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("powerExported", 1144.3).time("2022-11-08T01:06:54+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("powerExported", 633.0).time("2022-11-10T12:49:44+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("powerExported", 2478.2).time("2022-11-15T03:21:59+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("powerExported", 2043.5).time("2022-11-17T18:38:55+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("powerExported", 3337.8).time("2022-11-22T05:40:18+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("powerExported", 1521.7).time("2022-11-26T11:14:58+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("powerExported", 2611.8).time("2022-11-30T22:46:29+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("powerExported", 338.3).time("2022-12-04T22:14:59+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("powerExported", 1988.3).time("2022-12-08T02:57:32+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("powerExported", 3247.6).time("2022-12-12T14:56:24+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("powerExported", 3274.1).time("2022-12-17T13:00:34+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("powerExported", 2094.7).time("2022-12-19T15:52:58+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("powerExported", 879.4).time("2022-12-23T13:00:51+00:00"))

    # Monthly
    data.append(influxdb_client.Point(API_KEY).field("powerExported", 2274.2).time("2021-01-07T03:32:00+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("powerExported", 2002.1).time("2021-01-13T11:14:50+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("powerExported", 471.7).time("2021-01-20T02:09:09+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("powerExported", 1979.6).time("2021-01-26T10:07:38+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("powerExported", 3326.4).time("2021-02-01T19:27:58+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("powerExported", 2570.8).time("2021-02-07T21:14:30+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("powerExported", 2168.8).time("2021-02-13T09:41:52+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("powerExported", 159.9).time("2021-02-26T05:53:44+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("powerExported", 2643.2).time("2021-03-10T04:01:36+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("powerExported", 1290.0).time("2021-03-20T17:42:43+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("powerExported", 3361.7).time("2021-03-26T12:21:27+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("powerExported", 2454.5).time("2021-04-04T07:11:55+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("powerExported", 3134.5).time("2021-04-09T18:09:01+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("powerExported", 3137.0).time("2021-04-15T23:31:57+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("powerExported", 1217.1).time("2021-04-25T02:28:32+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("powerExported", 2238.7).time("2021-05-06T13:14:53+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("powerExported", 1736.9).time("2021-05-14T10:16:48+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("powerExported", 1855.1).time("2021-05-25T20:52:05+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("powerExported", 409.6).time("2021-06-04T00:48:12+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("powerExported", 111.2).time("2021-06-15T18:54:42+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("powerExported", 3273.7).time("2021-06-22T10:27:41+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("powerExported", 1258.8).time("2021-07-05T03:45:10+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("powerExported", 568.6).time("2021-07-17T10:56:53+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("powerExported", 1244.5).time("2021-07-29T09:51:57+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("powerExported", 623.6).time("2021-08-08T00:45:47+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("powerExported", 168.4).time("2021-08-16T02:29:19+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("powerExported", 418.3).time("2021-08-21T13:33:18+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("powerExported", 1254.6).time("2021-08-31T11:18:57+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("powerExported", 729.5).time("2021-09-08T21:05:37+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("powerExported", 2895.0).time("2021-09-19T13:30:49+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("powerExported", 1964.4).time("2021-09-27T18:06:05+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("powerExported", 2086.6).time("2021-10-03T17:06:02+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("powerExported", 3485.0).time("2021-10-16T13:45:45+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("powerExported", 2868.9).time("2021-10-28T08:47:21+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("powerExported", 2172.0).time("2021-11-03T17:38:53+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("powerExported", 3450.1).time("2021-11-11T11:24:12+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("powerExported", 217.3).time("2021-11-21T12:03:27+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("powerExported", 1106.3).time("2021-11-27T18:44:56+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("powerExported", 243.7).time("2021-12-03T11:20:13+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("powerExported", 1726.7).time("2021-12-15T06:15:24+00:00"))

    write_api.write(bucket=Config.INFLUX_BUCKET, org=Config.INFLUX_ORG, record=data)


def populate_influxdb_voltage():
    client = influxdb_client.InfluxDBClient(
        url=f"http://{Config.INFLUX_URL}:{Config.INFLUX_PORT}",
        token=Config.INFLUX_TOKEN,
        org=Config.INFLUX_ORG
    )

    write_api = client.write_api(write_options=SYNCHRONOUS)

    data = []

    # Daily
    data.append(influxdb_client.Point(API_KEY).field("voltage", 164.6).time("2022-05-01T06:55:29+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("voltage", 2687.5).time("2022-05-01T14:31:22+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("voltage", 2060.0).time("2022-05-01T22:07:46+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("voltage", 827.8).time("2022-05-02T01:17:03+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("voltage", 1150.0).time("2022-05-02T09:13:19+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("voltage", 2120.0).time("2022-05-02T17:40:33+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("voltage", 1615.1).time("2022-05-03T02:10:57+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("voltage", 712.2).time("2022-05-03T06:45:11+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("voltage", 1006.9).time("2022-05-03T12:48:55+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("voltage", 1633.1).time("2022-05-03T18:16:10+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("voltage", 290.2).time("2022-05-04T01:33:48+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("voltage", 488.4).time("2022-05-04T05:49:48+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("voltage", 400.3).time("2022-05-04T16:09:27+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("voltage", 1541.9).time("2022-05-04T17:38:24+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("voltage", 1835.3).time("2022-05-04T23:56:29+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("voltage", 814.5).time("2022-05-05T10:09:46+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("voltage", 2789.0).time("2022-05-05T14:19:21+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("voltage", 84.7).time("2022-05-05T16:59:43+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("voltage", 717.5).time("2022-05-05T19:25:24+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("voltage", 3395.8).time("2022-05-05T22:14:24+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("voltage", 1910.0).time("2022-05-06T04:55:07+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("voltage", 1409.1).time("2022-05-06T08:13:43+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("voltage", 768.9).time("2022-05-06T17:04:40+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("voltage", 2016.3).time("2022-05-07T02:03:21+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("voltage", 1851.4).time("2022-05-07T05:06:51+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("voltage", 2999.7).time("2022-05-07T10:37:05+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("voltage", 2360.7).time("2022-05-07T18:23:15+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("voltage", 504.5).time("2022-05-07T23:04:01+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("voltage", 3350.9).time("2022-05-08T04:28:00+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("voltage", 512.2).time("2022-05-08T12:09:07+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("voltage", 422.1).time("2022-05-08T21:15:14+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("voltage", 2111.4).time("2022-05-09T02:44:48+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("voltage", 890.3).time("2022-05-09T04:54:52+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("voltage", 881.8).time("2022-05-09T08:27:33+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("voltage", 248.4).time("2022-05-09T10:40:07+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("voltage", 2580.6).time("2022-05-09T20:17:06+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("voltage", 471.4).time("2022-05-10T06:04:30+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("voltage", 3323.3).time("2022-05-10T16:45:15+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("voltage", 2925.0).time("2022-05-10T18:28:44+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("voltage", 84.4).time("2022-05-10T23:43:03+00:00"))

    # Hourly
    data.append(influxdb_client.Point(API_KEY).field("voltage", 1489.6).time("2022-06-01T01:12:38+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("voltage", 829.5).time("2022-06-01T01:43:48+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("voltage", 3285.8).time("2022-06-01T02:15:43+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("voltage", 2941.2).time("2022-06-01T02:57:02+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("voltage", 423.5).time("2022-06-01T03:46:36+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("voltage", 2632.8).time("2022-06-01T04:13:57+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("voltage", 3290.2).time("2022-06-01T04:22:32+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("voltage", 1984.4).time("2022-06-01T05:03:27+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("voltage", 2502.4).time("2022-06-01T05:37:15+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("voltage", 1008.9).time("2022-06-01T05:51:38+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("voltage", 2070.1).time("2022-06-01T06:02:20+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("voltage", 3015.3).time("2022-06-01T06:35:23+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("voltage", 165.3).time("2022-06-01T06:59:15+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("voltage", 1375.1).time("2022-06-01T07:21:41+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("voltage", 2633.1).time("2022-06-01T07:42:49+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("voltage", 1792.8).time("2022-06-01T07:46:59+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("voltage", 3317.3).time("2022-06-01T08:29:52+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("voltage", 3447.5).time("2022-06-01T09:12:49+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("voltage", 1046.9).time("2022-06-01T09:55:50+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("voltage", 1887.8).time("2022-06-01T10:05:23+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("voltage", 2708.9).time("2022-06-01T10:19:38+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("voltage", 2895.2).time("2022-06-01T10:30:06+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("voltage", 1963.6).time("2022-06-01T11:18:04+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("voltage", 3378.1).time("2022-06-01T11:33:05+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("voltage", 2939.6).time("2022-06-01T11:36:04+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("voltage", 3021.9).time("2022-06-01T12:13:09+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("voltage", 1295.1).time("2022-06-01T12:31:22+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("voltage", 1565.2).time("2022-06-01T13:14:08+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("voltage", 1793.2).time("2022-06-01T13:50:12+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("voltage", 2069.6).time("2022-06-01T14:17:25+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("voltage", 655.2).time("2022-06-01T15:02:53+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("voltage", 1521.8).time("2022-06-01T15:45:37+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("voltage", 1069.6).time("2022-06-01T16:32:34+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("voltage", 189.1).time("2022-06-01T17:12:53+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("voltage", 3094.9).time("2022-06-01T18:01:14+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("voltage", 1278.0).time("2022-06-01T18:34:32+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("voltage", 2182.7).time("2022-06-01T18:44:41+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("voltage", 657.5).time("2022-06-01T18:57:46+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("voltage", 2632.2).time("2022-06-01T19:20:19+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("voltage", 1401.2).time("2022-06-01T19:38:03+00:00"))

    # 15min
    data.append(influxdb_client.Point(API_KEY).field("voltage", 2730.3).time("2022-07-01T01:02:39+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("voltage", 2292.7).time("2022-07-01T01:04:16+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("voltage", 248.8).time("2022-07-01T01:12:23+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("voltage", 549.4).time("2022-07-01T01:24:06+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("voltage", 2124.0).time("2022-07-01T01:27:26+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("voltage", 1110.5).time("2022-07-01T01:38:32+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("voltage", 2161.7).time("2022-07-01T01:43:44+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("voltage", 714.7).time("2022-07-01T01:54:45+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("voltage", 2877.1).time("2022-07-01T02:04:11+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("voltage", 1202.5).time("2022-07-01T02:08:17+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("voltage", 3116.8).time("2022-07-01T02:12:33+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("voltage", 293.6).time("2022-07-01T02:23:19+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("voltage", 2485.2).time("2022-07-01T02:25:37+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("voltage", 3115.8).time("2022-07-01T02:27:44+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("voltage", 1658.6).time("2022-07-01T02:30:24+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("voltage", 2119.7).time("2022-07-01T02:40:40+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("voltage", 1742.1).time("2022-07-01T02:51:16+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("voltage", 2380.8).time("2022-07-01T03:01:51+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("voltage", 2137.7).time("2022-07-01T03:04:52+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("voltage", 1611.8).time("2022-07-01T03:11:06+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("voltage", 3127.4).time("2022-07-01T03:16:21+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("voltage", 1911.4).time("2022-07-01T03:19:14+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("voltage", 2743.1).time("2022-07-01T03:22:22+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("voltage", 1160.3).time("2022-07-01T03:32:28+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("voltage", 2924.9).time("2022-07-01T03:37:57+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("voltage", 1384.4).time("2022-07-01T03:46:26+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("voltage", 1744.5).time("2022-07-01T03:49:48+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("voltage", 3479.8).time("2022-07-01T03:59:04+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("voltage", 846.6).time("2022-07-01T04:10:16+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("voltage", 2240.7).time("2022-07-01T04:11:44+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("voltage", 2532.1).time("2022-07-01T04:15:44+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("voltage", 3015.2).time("2022-07-01T04:20:30+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("voltage", 1435.8).time("2022-07-01T04:24:36+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("voltage", 3079.5).time("2022-07-01T04:28:44+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("voltage", 459.5).time("2022-07-01T04:34:03+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("voltage", 1343.1).time("2022-07-01T04:40:28+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("voltage", 2138.4).time("2022-07-01T04:50:36+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("voltage", 212.9).time("2022-07-01T04:57:26+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("voltage", 340.6).time("2022-07-01T05:02:01+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("voltage", 200.4).time("2022-07-01T05:11:10+00:00"))

    # Weekly
    data.append(influxdb_client.Point(API_KEY).field("voltage", 2779.4).time("2022-08-06T00:02:01+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("voltage", 809.3).time("2022-08-08T21:04:44+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("voltage", 3094.6).time("2022-08-13T18:33:13+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("voltage", 742.7).time("2022-08-17T01:42:09+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("voltage", 1203.7).time("2022-08-21T03:34:17+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("voltage", 3341.3).time("2022-08-23T13:42:43+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("voltage", 520.2).time("2022-08-27T13:29:13+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("voltage", 2793.2).time("2022-09-01T00:37:44+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("voltage", 2209.1).time("2022-09-04T02:13:59+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("voltage", 183.0).time("2022-09-08T20:47:19+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("voltage", 3421.0).time("2022-09-11T08:07:48+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("voltage", 422.4).time("2022-09-13T14:45:27+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("voltage", 1255.3).time("2022-09-18T12:04:59+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("voltage", 2059.8).time("2022-09-22T07:16:53+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("voltage", 2099.6).time("2022-09-26T23:28:32+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("voltage", 435.0).time("2022-09-29T17:14:54+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("voltage", 1278.1).time("2022-10-03T17:09:36+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("voltage", 2671.4).time("2022-10-07T03:21:00+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("voltage", 3402.2).time("2022-10-10T01:49:27+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("voltage", 1922.4).time("2022-10-13T04:22:11+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("voltage", 3336.8).time("2022-10-17T22:02:20+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("voltage", 2333.1).time("2022-10-19T23:57:07+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("voltage", 3405.0).time("2022-10-24T10:51:00+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("voltage", 1921.9).time("2022-10-27T09:33:33+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("voltage", 1232.4).time("2022-10-29T23:32:45+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("voltage", 905.1).time("2022-11-02T01:43:29+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("voltage", 218.1).time("2022-11-04T18:29:51+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("voltage", 1144.3).time("2022-11-08T01:06:54+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("voltage", 633.0).time("2022-11-10T12:49:44+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("voltage", 2478.2).time("2022-11-15T03:21:59+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("voltage", 2043.5).time("2022-11-17T18:38:55+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("voltage", 3337.8).time("2022-11-22T05:40:18+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("voltage", 1521.7).time("2022-11-26T11:14:58+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("voltage", 2611.8).time("2022-11-30T22:46:29+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("voltage", 338.3).time("2022-12-04T22:14:59+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("voltage", 1988.3).time("2022-12-08T02:57:32+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("voltage", 3247.6).time("2022-12-12T14:56:24+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("voltage", 3274.1).time("2022-12-17T13:00:34+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("voltage", 2094.7).time("2022-12-19T15:52:58+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("voltage", 879.4).time("2022-12-23T13:00:51+00:00"))

    # Monthly
    data.append(influxdb_client.Point(API_KEY).field("voltage", 2274.2).time("2021-01-07T03:32:00+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("voltage", 2002.1).time("2021-01-13T11:14:50+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("voltage", 471.7).time("2021-01-20T02:09:09+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("voltage", 1979.6).time("2021-01-26T10:07:38+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("voltage", 3326.4).time("2021-02-01T19:27:58+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("voltage", 2570.8).time("2021-02-07T21:14:30+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("voltage", 2168.8).time("2021-02-13T09:41:52+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("voltage", 159.9).time("2021-02-26T05:53:44+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("voltage", 2643.2).time("2021-03-10T04:01:36+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("voltage", 1290.0).time("2021-03-20T17:42:43+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("voltage", 3361.7).time("2021-03-26T12:21:27+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("voltage", 2454.5).time("2021-04-04T07:11:55+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("voltage", 3134.5).time("2021-04-09T18:09:01+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("voltage", 3137.0).time("2021-04-15T23:31:57+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("voltage", 1217.1).time("2021-04-25T02:28:32+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("voltage", 2238.7).time("2021-05-06T13:14:53+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("voltage", 1736.9).time("2021-05-14T10:16:48+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("voltage", 1855.1).time("2021-05-25T20:52:05+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("voltage", 409.6).time("2021-06-04T00:48:12+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("voltage", 111.2).time("2021-06-15T18:54:42+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("voltage", 3273.7).time("2021-06-22T10:27:41+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("voltage", 1258.8).time("2021-07-05T03:45:10+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("voltage", 568.6).time("2021-07-17T10:56:53+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("voltage", 1244.5).time("2021-07-29T09:51:57+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("voltage", 623.6).time("2021-08-08T00:45:47+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("voltage", 168.4).time("2021-08-16T02:29:19+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("voltage", 418.3).time("2021-08-21T13:33:18+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("voltage", 1254.6).time("2021-08-31T11:18:57+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("voltage", 729.5).time("2021-09-08T21:05:37+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("voltage", 2895.0).time("2021-09-19T13:30:49+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("voltage", 1964.4).time("2021-09-27T18:06:05+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("voltage", 2086.6).time("2021-10-03T17:06:02+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("voltage", 3485.0).time("2021-10-16T13:45:45+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("voltage", 2868.9).time("2021-10-28T08:47:21+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("voltage", 2172.0).time("2021-11-03T17:38:53+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("voltage", 3450.1).time("2021-11-11T11:24:12+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("voltage", 217.3).time("2021-11-21T12:03:27+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("voltage", 1106.3).time("2021-11-27T18:44:56+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("voltage", 243.7).time("2021-12-03T11:20:13+00:00"))
    data.append(influxdb_client.Point(API_KEY).field("voltage", 1726.7).time("2021-12-15T06:15:24+00:00"))

    write_api.write(bucket=Config.INFLUX_BUCKET, org=Config.INFLUX_ORG, record=data)

def clean_account():
    try:
        db.session.query(DBNotDisturbUser).delete()
        db.session.query(DBUserSettings).delete()
        db.session.query(DBEvent).delete()
        db.session.query(DBUser).delete()
        db.session.flush()
        db.session.commit()
    except:
        print("MOCK DATABASE - FAILED TO DELETE ACCOUNT DB")
        db.session.rollback()


# def clean_database():
#     try:
#         db.session.query(DBNotDisturb).delete()
#         db.session.query(DBShiftablePowerProfile).delete()
#         db.session.query(DBShiftableCycle).delete()
#         db.session.query(DBShiftableMachine).delete()
#         db.session.query(DBDongles).delete()
#         db.session.flush()
#         db.session.commit()
#     except:
#         print("MOCK DATABASE - FAILED TO DELETE DB")
#         db.session.rollback()

def id_generator(size, chars=string.ascii_lowercase + string.digits):
    return ''.join(secrets.SystemRandom().choice(chars) for _ in range(size))


def register_super_user(id="aa", meter_id=METER_ID, register_api_key=False):
    body = {
            "first_name": "Test",
            "last_name": "Test",
            "email": f"riscas.cat1+{id}@gmail.com",
            "password": "123456",
            "password_repeat": "123456",
            "meter_id": meter_id,
            "country": "PT",
            "postal_code": "4450-001",
            "tarif_type": "simple",
            "contracted_power": "6.9 kVA",
            "schedule_type": "economic",
    }

    register_data = json.dumps(body)
    headers = {
        "Content-Type": "application/json",
        "X-Correlation-ID": "b2fdda1b-9550-4afd-9b3d-d180a6398986",
    }

    print("REGISTERING USER....")
    new_user = requests.post(
        url=Config.ACCOUNT_MANAGER_ENDPOINT + "/register",
        data=register_data,
        headers=headers,
    )
    # new_user = requests.post(url="http://account-manager-test:8080/api/account"+ "/register", data=register_data, headers=headers)
    print(new_user.content)
    print("REGISTERING USER.... OK!")

    new_user_id = json.loads(new_user.content)["user_id"]
    print(new_user_id)

    print("Activate User Account")
    DBConfirmationToken.query.filter_by(user_id=new_user_id).delete()
    user = DBUser.query.filter_by(user_id=new_user_id).first()
    user.is_active = True
    # user.settings.permissions = "Full"

    if register_api_key:
        user.api_key = API_KEY

    db.session.commit()

    return new_user_id


def superuser_login(id="aa", email=None, password=None):
    if email is None:
        email = f"riscas.cat1+{id}@gmail.com"
    if password is None:
        password = "123456"
    login_data = json.dumps(
        {"email": email, "password": password}
    )
    headers = {
        "Content-Type": "application/json",
        "X-Correlation-ID": "b2fdda1b-9550-4afd-9b3d-d180a6398986",
    }

    user_login = requests.post(
        url=Config.ACCOUNT_MANAGER_ENDPOINT + "/login", data=login_data, headers=headers
    )
    print(user_login.headers)

    return user_login.headers["authorization"]

def mock_update_meter_id(auth, user_id, meter_id):
    headers = {
        "Accept": "application/json",
        "X-Correlation-ID": str(uuid.uuid4()),
        "Authorization": auth,
    }
    user = requests.get(
        url=f"{Config.ACCOUNT_MANAGER_ENDPOINT}/user?user-ids={user_id}",
        headers=headers,
    )

    user_dict = json.loads(user.content)[0]

    user_dict["meter_id"] = meter_id

    new_settings_data = json.dumps(user_dict)
    headers = {
        "Content-Type": "application/json",
        "X-Correlation-ID": "b2fdda1b-9550-4afd-9b3d-d180a6398986",
        "Authorization": auth,
    }

    print("UPDATING USER....")
    user = requests.post(
        url=Config.ACCOUNT_MANAGER_ENDPOINT + "/user",
        data=new_settings_data,
        headers=headers,
    )
    # new_user = requests.post(url="http://account-manager-test:8080/api/account"+ "/register", data=register_data, headers=headers)
    print(user.content)

    if (user.status_code != 200):
        print("UPDATING USER.... ERROR!")
        return False
    
    print("UPDATING USER.... OK!")
    return True


def mock_delete_user(auth, user_id, delete_type="hard"):
    headers = {
        "Accept": "application/json",
        "X-Correlation-ID": str(uuid.uuid4()),
        "Authorization": auth,
    }
    user = requests.delete(
        url=f"{Config.ACCOUNT_MANAGER_ENDPOINT}/user?user-id={user_id}&delete_type={delete_type}",
        headers=headers,
    )

    if (user.status_code != 200):
        print("DELETING USER.... ERROR!")
        return False
    
    print("DELETING USER.... OK!")
    return True


def mock_register(user_key=None, meter_id=METER_ID, register_api_key=False):
    # clean_account()

    # Key to create a new unique user in the db
    # user_key = "aa"  # Must have 2 leters, because of the CPE naming convention
    if user_key == None:
        user_key = id_generator(3)

    user_id = register_super_user(
        id=user_key,
        meter_id=meter_id,
        register_api_key=register_api_key
    )  # The randomly generated ID by the account manager

    sleep(1)

    second_user_key = user_key + "b"
    second_user_id = register_super_user(id=second_user_key, meter_id=METER_ID_WITHOUT_API_KEY)

    sleep(1)

    return user_key, user_id, second_user_key, second_user_id


def mock_change_settings(test_client, auth, serial_number, not_disturb):

    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "x_correlation_id": str(uuid.uuid4()),
        "Authorization": auth,
    }
    params = {"serial_numbers": serial_number}
    response = test_client.client.open(
        "/api/device/settings-by-device",
        method="POST",
        headers=headers,
        query_string=params,
        data=json.dumps(not_disturb),
        content_type="application/json",
    )

    return response
