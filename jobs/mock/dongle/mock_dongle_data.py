import requests, uuid, json
from random import uniform
from datetime import datetime, timezone, timedelta
from influxdb_client import Point

from init import logger, query_api, write_api, Config

INFLUX_DB_DATE_FORMAT = "%Y-%m-%dT%H:%M:%SZ"
STEPS = 96
FIELDS = ['powerImported', 'powerExported', 'voltage', 'powerDifference', 'energyExported', 'energyImported']

# Account Manager: List API keys
headers = {
    "X-Correlation-ID": str(uuid.uuid4())
}
response = requests.get(
    url=Config.ACCOUNT_MANAGER_ENDPOINT + '/list-dongles',
    headers=headers
)
if response.status_code != 200:
    logger.error(f'Account Manager: List API keys: {response.status_code}\n{response.content}')
    exit(1)
else:
    logger.debug(f'Account Manager: List API keys: {response.status_code}\n{response.content}')

dongle_list = json.loads(response.content.decode('utf-8'))

# InfluxDB: Write data
for user_key_pair in dongle_list:
    logger.info(f'Writing data for dongle {user_key_pair["api_key"]}...')
    
    data = []
    for field in FIELDS:
        logger.debug(f'Writing data for field {field}...')
        influx_time = datetime.now(timezone.utc).replace(second=0, minute=0, hour=0)

        if field == "energyImported" or field == "energyExported":
            query = f"""from(bucket: "{Config.INFLUX_BUCKET}")
            |> range(start: 0, stop: {datetime.now(timezone.utc).strftime(INFLUX_DB_DATE_FORMAT)})
            |> filter(fn: (r) => r["_measurement"] == "{user_key_pair['api_key']}")
            |> filter(fn: (r) => r["_field"] == "{field}")
            |> last()"""
            result = query_api.query(query=query)
            logger.debug(f"Query: {query}\nResult: {result}")
            if len(result) == 0:
                last_value = 0.0
            else:
                last_value = result[0].records
                last_value = float(last_value[0].get_value())
            for step in range(STEPS):
                data.append(Point(user_key_pair['api_key']).field(field, round(last_value, 1)).time(influx_time.strftime('%Y-%m-%dT%H:%M:%S%z')))
                last_value += round(uniform(0.01, 0.4), 1)
                influx_time += timedelta(minutes=15)
        else:
            for step in range(STEPS):
                data.append(Point(user_key_pair['api_key']).field(field, round(uniform(0.0, 3.0), 1)).time(influx_time.strftime('%Y-%m-%dT%H:%M:%S%z')))
                influx_time += timedelta(minutes=15)
    
    write_api.write(
        bucket=Config.INFLUX_BUCKET,
        org=Config.INFLUX_ORG,
        record=data
    )
    logger.debug(f"Wrote {len(data)} records for dongle {user_key_pair['api_key']}")
