from statistics_manager_service import logger, db, app
from statistics_manager_service.models.database.db_models import DBMetricsHourly

@app.route('/health')
def healthy():
    corId = {'X-Correlation-ID': 'health'}

    user = DBMetricsHourly.query.first()

    logger.info("Heath endpoint OK", extra=corId)

    return ''
