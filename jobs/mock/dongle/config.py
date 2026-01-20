import os, logging


class Config:
    ACCOUNT_MANAGER_ENDPOINT = os.environ.get('ACCOUNT_MANAGER_ENDPOINT', 'http://localhost:8082/api/account')
    # ACCOUNT_MANAGER_ENDPOINT = os.environ.get('ACCOUNT_MANAGER_ENDPOINT', 'http://account-manager.default.svc.cluster.local:8080/api/account')
    
    INFLUX_URL = os.environ.get('INFLUX_URL', 'http://localhost:8086')
    # INFLUX_URL = os.environ.get('INFLUX_URL', 'http://influxdb-influxdb2.default.svc.cluster.local:80')
    INFLUX_TOKEN = os.environ.get('INFLUX_TOKEN', 'influx-token')
    INFLUX_ORG = os.environ.get('INFLUX_ORG', 'inesctec')
    INFLUX_BUCKET = os.environ.get('INFLUX_BUCKET', 'interconnect-eot-meters')
    
    LOG_LEVEL = logging.getLevelName(os.environ.get('FORECAST_LOG_LEVEL', 'DEBUG'))
