#!/bin/python

import random
from datetime import datetime, timedelta, timezone

initial_timestamp = datetime(2021, 1, 1, 1, 0, 0, tzinfo=timezone.utc)
max_slots = 40
min_rand_sec = 60*60*24*5
max_rand_sec = 60*60*24*13
min_rand_power = 100
max_rand_power = 3500

timestamp = initial_timestamp
for i in range(0, max_slots):
    rand_sec = random.randint(min_rand_sec, max_rand_sec)
    rand_power = round(random.uniform(min_rand_power, max_rand_power), 1)

    timestamp = timestamp + timedelta(seconds=rand_sec)
    timestamp_string = timestamp.strftime("%Y-%m-%dT%H:%M:%S+00:00")
    
    print(f"\tdata.append(influxdb_client.Point(API_KEY).field(\"powerImported\", {rand_power}).time(\"{timestamp_string}\"))")
