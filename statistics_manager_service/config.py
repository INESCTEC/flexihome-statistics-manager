import os
import logging


class Config:
    TESTING = os.environ.get("TESTING", "False")

    ### DATABASE ###

    # STATISTICS
    DATABASE_IP = os.environ.get('DATABASE_IP', '127.0.0.1')
    DATABASE_PORT = os.environ.get('DATABASE_PORT', '5432')
    DATABASE_USER = os.environ.get('DATABASE_USER', 'postgres')
    DATABASE_PASSWORD = os.environ.get('DATABASE_PASSWORD', 'mysecretpassword')

    # AUTH
    AUTH_DATABASE_USER = os.environ.get('AUTH_DATABASE_USER', 'postgres')
    AUTH_DATABASE_PASSWORD = os.environ.get(
        'AUTH_DATABASE_PASSWORD', 'mysecretpassword')

    # ACCOUNT MANAGER (TESTS)
    DATABASE_IP_ACCOUNT = os.environ.get('DATABASE_IP_ACCOUNT', '127.0.0.1')
    DATABASE_PORT_ACCOUNT = os.environ.get('DATABASE_PORT_ACCOUNT', '5432')
    DATABASE_USER_ACCOUNT = os.environ.get('DATABASE_USER_ACCOUNT', 'postgres')
    DATABASE_PASSWORD_ACCOUNT = os.environ.get(
        'DATABASE_PASSWORD_ACCOUNT', 'mysecretpassword')

    # SQLALCHEMY
    SQLALCHEMY_DATABASE_URI = f'postgresql+psycopg2://{DATABASE_USER}:{DATABASE_PASSWORD}@{DATABASE_IP}:{DATABASE_PORT}/statisticsmanager'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    if TESTING == "True":
        SQLALCHEMY_BINDS = {
            'account_manager': f'postgresql+psycopg2://{DATABASE_USER_ACCOUNT}:{DATABASE_PASSWORD_ACCOUNT}@{DATABASE_IP_ACCOUNT}:{DATABASE_PORT_ACCOUNT}/account_manager',
        }


    SQLALCHEMY_ENGINE_OPTIONS = {
        "pool_pre_ping": True if os.environ.get("SQLALCHEMY_POOL_PRE_PING", "True").lower() == "true" else False,
        "pool_logging_name": os.environ.get("SQLALCHEMY_POOL_LOGGING_NAME", "pool_log"),
        'connect_args': {
            "keepalives": 1,
            "keepalives_idle": 60,
            "keepalives_interval": 30,
            "keepalives_count": 5,
        }
    }

    SQLALCHEMY_ENGINE_LOG_LEVEL = logging.getLevelName(
        os.environ.get('SQLALCHEMY_ENGINE_LOG_LEVEL', 'WARN'))
    SQLALCHEMY_POOL_LOG_LEVEL = logging.getLevelName(
        os.environ.get('SQLALCHEMY_POOL_LOG_LEVEL', 'WARN'))

    ### METRICS ###

    LOG_LEVEL = logging.getLevelName(os.environ.get('LOG_LEVEL', 'DEBUG'))
    LOG_FORMAT = logging.getLevelName(os.environ.get('LOG_FORMAT', 'text'))
    OC_AGENT_ENDPOINT = os.environ.get('OC_AGENT_ENDPOINT', '127.0.0.1:6831')

    ### KAFKA + DEBEZIUM ###

    KAFKA_BROKER_ENDPOINT = os.environ.get(
        'KAFKA_BROKER_ENDPOINT', '127.0.0.1:9092')
    KAFKA_TOPIC_PREFIX = os.environ.get('KAFKA_TOPIC_PREFIX', 'hems.')
    KAFKA_TOPIC_SUFFIX = 'statistics'
    KAFKA_TOPIC = KAFKA_TOPIC_PREFIX + KAFKA_TOPIC_SUFFIX
    KAFKA_GROUP_ID = 'StatisticsManagerService'
    # How many seconds to wait for an exit event
    KAFKA_WAIT_FOR_EVENT_SECONDS = 0.01
    KAFKA_CONSUMER_TIMEOUT_MS = 100
    KAFKA_RECONNECT_SLEEP_SECONDS = 5

    KAFKA_LOG_LEVEL = logging.getLevelName(
        os.environ.get('KAFKA_LOG_LEVEL', 'INFO'))

    ### SUPPORT SERVICES ###

    # INFLUX Testing
    INFLUX_URL = os.environ.get('INFLUX_URL', '127.0.0.1')
    INFLUX_PORT = os.environ.get('INFLUX_PORT', '8086')
    INFLUX_TOKEN = os.environ.get('INFLUX_TOKEN', 'influx_token')
    INFLUX_ORG = os.environ.get('INFLUX_ORG', 'inesctec')
    INFLUX_BUCKET = os.environ.get('INFLUX_BUCKET', 'interconnect-eot-meters')

    # ACCOUNT MANAGER
    ACCOUNT_MANAGER_ENDPOINT = os.environ.get(
        'ACCOUNT_MANAGER_ENDPOINT', 'http://127.0.0.1:8081/api/account')
    JWT_SIGN_KEY = os.environ.get('JWT_SIGN_KEY', 'my_jwt_signing_secret_key')
    JWT_SIGN_ALGORITHM = 'HS512'
    USER_ID_SIZE = 10
    DEFAULT_SCHEDULE_TYPE = "economic"

    # FORECAST
    FORECAST_API_URL = os.environ.get(
        'FORECAST_API_URL', 'http://forecast-rest-api.default.svc.cluster.local:8080/api/forecast')
    REQUEST_TIMEOUT_SECONDS = int(
        os.environ.get('REQUEST_TIMEOUT_SECONDS', '10'))

    HOST_SENTINEL = os.environ.get(
        'HOST_SENTINEL', "http://vcpes08.inesctec.pt:8000/data/inesctec")
    SENTINEL_TOKEN = os.environ.get('SENTINEL_TOKEN', "sentinel_token")
    X_CSRFTOKEN = os.environ.get('X_CSRFTOKEN', "csrf_token")
