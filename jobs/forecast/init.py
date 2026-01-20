import coloredlogs, logging
import influxdb_client

from config import Config


log_format = '%(asctime)s | %(name)s | %(threadName)s | %(levelname)s | %(module)s.%(funcName)s:%(lineno)d — %(message)s'

# Set log config for our app
logger = logging.getLogger(__name__ + "_logger")
logger.setLevel(Config.LOG_LEVEL)

coloredlogs.install(
    level=Config.LOG_LEVEL,
    fmt=log_format,
    datefmt='%Y-%m-%dT%H:%M:%S',
    logger=logger,
    isatty=True
)

# Do not propagate (app log handler -> root handler)
# Without this, the logs of our app are printed twice
logger.propagate = False


# Instantiate influxdb client and query api
client = influxdb_client.InfluxDBClient(
    url=Config.INFLUX_URL,
    token=Config.INFLUX_TOKEN,
    org=Config.INFLUX_ORG
)
query_api = client.query_api()
