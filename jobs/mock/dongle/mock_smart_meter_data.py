import requests, uuid, json
from random import uniform
from datetime import datetime, timezone, timedelta
from influxdb_client import Point

from init import logger, write_api, Config

STEPS = 96

# Account Manager: List API keys
headers = {
    "X-Correlation-ID": str(uuid.uuid4())
}
response = requests.get(
    url=Config.ACCOUNT_MANAGER_ENDPOINT + '/list-meter-ids',
    headers=headers
)
if response.status_code != 200:
    logger.error(f'Account Manager: List API keys: {response.status_code}\n{response.content}')
    exit(1)
else:
    logger.debug(f'Account Manager: List API keys: {response.status_code}\n{response.content}')

meter_list = json.loads(response.content.decode('utf-8'))

# InfluxDB: Write data
for meter in meter_list:
    logger.info(f'Writing data for meter {meter}...')
    
    data = []
    influx_time = datetime.now(timezone.utc).replace(second=0, minute=0, hour=0)
    for step in range(STEPS):
        data.append(Point(meter).field("meterPowerImported", round(uniform(0.0, 3.0), 1)).time(influx_time.strftime('%Y-%m-%dT%H:%M:%S%z')))
        influx_time += timedelta(minutes=15)
    
    write_api.write(
        bucket=Config.INFLUX_BUCKET,
        org=Config.INFLUX_ORG,
        record=data
    )
    logger.debug(f"Wrote {len(data)} records for dongle {meter}")
