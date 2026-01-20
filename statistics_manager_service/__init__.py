import connexion, logging, coloredlogs, influxdb_client
from datetime import datetime, timezone

from flask_sqlalchemy import SQLAlchemy

from pythonjsonlogger import jsonlogger

from prometheus_flask_exporter import ConnexionPrometheusMetrics
from opencensus.ext.flask.flask_middleware import FlaskMiddleware
from opencensus.trace import config_integration, samplers
from opencensus.ext.ocagent.trace_exporter import TraceExporter

from statistics_manager_service import encoder
from statistics_manager_service.config import Config

from hems_auth.auth import Auth


INFLUX_DB_DATE_FORMAT = "%Y-%m-%dT%H:%M:%SZ"


class CustomJsonFormatter(jsonlogger.JsonFormatter):
    def add_fields(self, log_record, record, message_dict):
        """
        Override this method to implement custom logic for adding fields.
        """
        for field in self._required_fields:
            if field in self.rename_fields:
                log_record[self.rename_fields[field]
                           ] = record.__dict__.get(field)
            else:
                log_record[field] = record.__dict__.get(field)
        log_record.update(self.static_fields)
        log_record.update(message_dict)
        jsonlogger.merge_record_extra(
            record, log_record, reserved=self._skip_fields)

        if self.timestamp:
            key = self.timestamp if type(
                self.timestamp) == str else 'timestamp'
            log_record[key] = datetime.fromtimestamp(
                record.created, tz=timezone.utc).isoformat(timespec='milliseconds')


# Configure opencensus tracing integrations (plugins)
config_integration.trace_integrations(['logging'])
config_integration.trace_integrations(['sqlalchemy'])
config_integration.trace_integrations(['requests'])

# Setup Flask app
connexionApp = connexion.App(__name__,
                             specification_dir='./openapi/',
                             options={"swagger_ui": False})
connexionApp.app.json_encoder = encoder.JSONEncoder

app = connexionApp.app
app.config.from_object(Config)

# Setup Flask SQLAlchemy
db = SQLAlchemy(app)


# Setup logger
if Config.LOG_FORMAT == "json":
    generalLogFormat = '%(asctime)s | %(name)s | %(threadName)s | %(levelname)s | %(module)s.%(funcName)s:%(lineno)d — %(message)s'
    appLogFormat = '%(asctime)s | %(name)s | %(threadName)s | %(levelname)s | %(module)s.%(funcName)s:%(lineno)d — X-Correlation-ID=%(X-Correlation-ID)s — traceId=%(traceId)s — spanId=%(spanId)s — %(message)s'

    generalFormatter = CustomJsonFormatter(generalLogFormat, timestamp=True)
    generalLogHandler = logging.StreamHandler()
    generalLogHandler.setFormatter(generalFormatter)

    # Set log config for all modules
    logging.basicConfig(level=logging.INFO, handlers=[generalLogHandler])

    # Set log config for our app
    logger = logging.getLogger(__name__ + "_logger")

    appFormatter = CustomJsonFormatter(appLogFormat, timestamp=True)
    appLogHandler = logging.StreamHandler()
    appLogHandler.setFormatter(appFormatter)

    logger.setLevel(Config.LOG_LEVEL)
    logger.addHandler(appLogHandler)
else:
    # Format for all modules except our app (e.g., Flask logs, Waitress logs, etc.)
    generalLogFormat = '%(asctime)s | %(name)s | %(threadName)s | %(levelname)s | %(module)s.%(funcName)s:%(lineno)d — %(message)s'
    # Format for our app, which includes the X-Correlation-ID string as required
    appLogFormat = '%(asctime)s | %(name)s | %(threadName)s | %(levelname)s | %(module)s.%(funcName)s:%(lineno)d — X-Correlation-ID=%(X-Correlation-ID)s — traceId=%(traceId)s — spanId=%(spanId)s — %(message)s'

    # Set log config for our app
    logger = logging.getLogger(__name__ + "_logger")

    coloredlogs.install(
        level=Config.LOG_LEVEL,
        fmt=appLogFormat,
        datefmt='%Y-%m-%dT%H:%M:%S',
        logger=logger,
        isatty=True,
        )


# Do not propagate (app log handler -> root handler)
# Without this, the logs of our app are printed twice
logger.propagate = False

generalLogger = logging.getLogger(__name__)
generalLogger.propagate = False
coloredlogs.install(
    level=Config.LOG_LEVEL,
    fmt=generalLogFormat,
    datefmt='%Y-%m-%dT%H:%M:%S',
    logger=generalLogger,
    isatty=True
)


# GRAB LOGS FROM LIBRARIES USED BY THE SERVICE

sqlalchemy_engine_logger = logging.getLogger("sqlalchemy.engine")
sqlalchemy_engine_logger.propagate = False
coloredlogs.install(
    level=Config.SQLALCHEMY_ENGINE_LOG_LEVEL,
    fmt=generalLogFormat,
    datefmt='%Y-%m-%dT%H:%M:%S',
    logger=sqlalchemy_engine_logger,
    isatty=True
)

sqlalchemy_pool_logger = logging.getLogger("sqlalchemy.pool")
sqlalchemy_pool_logger.propagate = False
coloredlogs.install(
    level=Config.SQLALCHEMY_POOL_LOG_LEVEL,
    fmt=generalLogFormat,
    datefmt='%Y-%m-%dT%H:%M:%S',
    logger=sqlalchemy_pool_logger,
    isatty=True
)

kafka_logger = logging.getLogger("kafka")  # NOTE: We can detail which kafka module we want to log, by using its like, p. e. 'kafka.conn' or 'kafka.coordinator'
kafka_logger.propagate = False
coloredlogs.install(
    level=Config.KAFKA_LOG_LEVEL,
    fmt=generalLogFormat,
    datefmt='%Y-%m-%dT%H:%M:%S',
    logger=kafka_logger,
    isatty=True
)

coloredlogs.install(
    level=logging.INFO,
    fmt=generalLogFormat,
    datefmt='%Y-%m-%dT%H:%M:%S',
    # logger=generalLogger
    isatty=True,
    )



# Setup Prometheus metrics
metrics = ConnexionPrometheusMetrics(connexionApp, group_by='url_rule')

metrics.info('app_info', 'Statistics Manager Service', version='1.2.0')

# OpenCencus tracing
exporter = TraceExporter(
    service_name='Statistics Manager Service',
    endpoint=Config.OC_AGENT_ENDPOINT,
)

sampler = samplers.AlwaysOnSampler()

middleware = FlaskMiddleware(app, exporter=exporter, sampler=sampler)


auth = Auth(
    jwt_sign_key=Config.JWT_SIGN_KEY,
    jwt_sign_algorithm=Config.JWT_SIGN_ALGORITHM,
    DATABASE_IP=Config.DATABASE_IP,
    DATABASE_PORT=Config.DATABASE_PORT,
    DATABASE_USER=Config.AUTH_DATABASE_USER,
    DATABASE_PASSWORD=Config.AUTH_DATABASE_PASSWORD
)

# Instantiate influxdb client and query api
client = influxdb_client.InfluxDBClient(
    url=Config.INFLUX_URL,
    token=Config.INFLUX_TOKEN,
    org=Config.INFLUX_ORG
)
query_api = client.query_api()
