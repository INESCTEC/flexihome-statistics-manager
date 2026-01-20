import os, logging


class Config:
    # ACCOUNT_MANAGER_ENDPOINT = os.environ.get('ACCOUNT_MANAGER_ENDPOINT', 'http://localhost:8081/api/account')
    ACCOUNT_MANAGER_ENDPOINT = os.environ.get('ACCOUNT_MANAGER_ENDPOINT', 'http://account-manager.default.svc.cluster.local:8080/api/account')
    
    
    INFLUX_URL = os.environ.get('INFLUX_URL', 'http://influxdb-influxdb2.default.svc.cluster.local:80')
    INFLUX_TOKEN = os.environ.get('INFLUX_TOKEN', 'uP52lRIgI5x0lbZ2Bx8MCo404459AIwx')
    INFLUX_ORG = os.environ.get('INFLUX_ORG', 'influxdata')
    INFLUX_BUCKET = os.environ.get('INFLUX_BUCKET', 'interconnect-eot-meters')
    
    
    FORECAST_SERVICE_ENDPOINT = os.environ.get('FORECAST_API_URL', 'http://forecast-rest-api.default.svc.cluster.local:8080/api')
    
    
    LOG_LEVEL = logging.getLevelName(os.environ.get('FORECAST_LOG_LEVEL', 'DEBUG'))
