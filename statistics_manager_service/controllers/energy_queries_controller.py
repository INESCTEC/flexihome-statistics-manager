import connexion

from statistics_manager_service.models.forecast_vs_real import ForecastVsReal as FVR
from statistics_manager_service.models.energy_time_series import EnergyTimeSeries, EnergyUnits
from statistics_manager_service.models.database.db_models import (
    DBMetricsDaily,
    DBMetricsHourly,
    DBMetricsMonthly,
    ForecastVsReal
)
from statistics_manager_service.models.error import Error
from statistics_manager_service.config import Config
from statistics_manager_service import auth, logger, db, app, util
from statistics_manager_service.controllers.utils import get_values_influxdb_energy, logResponse, logErrorResponse

from datetime import datetime, timezone


def energy_consumption_get(user_ids, start_date, group_by=None, end_date=None):  # noqa: E501
    """Retrieve the energy consumption for several userssss. The \&quot;group_by\&quot; variable is used to compute energy spent on that interval

     # noqa: E501

    :param x_correlation_id: 
    :type x_correlation_id: str
    :type x_correlation_id: str
    :param user_ids: 
    :type user_ids: List[str]
    :param start_date: 
    :type start_date: str
    :param authorization: 
    :type authorization: str
    :param group_by: 
    :type group_by: str
    :param end_date: 
    :type end_date: str

    :rtype: Union[List[EnergyMetrics], Tuple[List[EnergyMetrics], int], Tuple[List[EnergyMetrics], int, Dict[str, str]]
    """
    corId = {"X-Correlation-ID": connexion.request.headers["X-Correlation-ID"]}

    logger.info("Processing GET /energy-consumption request", extra=corId)
    endText = "Processed GET /energy-consumption request"

    auth_response, auth_response_code = auth.verify_basic_authorization(
        connexion.request.headers
    )

    if auth_response_code != 200:
        if auth_response_code == 402:
            logger.error(f"Blacklisted token {auth_response}", extra=corId)
        else:
            logger.error(
                f"Could not decode authorization token {auth_response}", extra=corId)

        message = "invalid credentials"
        response = Error(message)
        logErrorResponse(message, endText, response, corId)
        return response, 401, corId

    start_date = util.deserialize_datetime(start_date)
    if end_date is None:
        end_date = datetime.now(timezone.utc).strftime("%d-%m-%YT%H:%M:%S%z")
    end_date = util.deserialize_datetime(end_date)

    logger.debug(f"start: {start_date} \t end: {end_date}", extra=corId)
    logger.debug(f"user_ids: {user_ids}", extra=corId)
    logger.debug(f"group_by: {group_by}", extra=corId)

    if auth_response is not None:
        for uId in user_ids:
            if uId != auth_response:
                logger.error(
                    f"User {auth_response} does not have permission to see user {uId}",
                    extra=corId,
                )
                message = "no permission"
                response = Error(message)

                logErrorResponse(message, endText, response, corId)
                return response, 403, corId

    if group_by == None:
        group_by = "daily"

    response, code, error_message = get_values_influxdb_energy(
        user_ids, "energyImported", False, corId, start_date, end_date, group_by)

    if code != 200:
        logResponse(endText, response, corId)
    else:
        logErrorResponse(error_message, endText, response, corId)

    return response, code, corId


def energy_consumption_last_get(user_ids):  # noqa: E501
    """Retrieve the last value of the energy consumption for several users.

     # noqa: E501

    :param x_correlation_id: 
    :type x_correlation_id: str
    :type x_correlation_id: str
    :param user_ids: 
    :type user_ids: List[str]
    :param authorization: 
    :type authorization: str

    :rtype: Union[List[InstantEnergyMetric], Tuple[List[InstantEnergyMetric], int], Tuple[List[InstantEnergyMetric], int, Dict[str, str]]
    """
    corId = {"X-Correlation-ID": connexion.request.headers["X-Correlation-ID"]}

    logger.info("Processing GET /energy-consumption-last request", extra=corId)
    endText = "Processed GET /energy-consumption-last request"

    auth_response, auth_response_code = auth.verify_basic_authorization(
        connexion.request.headers
    )

    if auth_response_code != 200:
        if auth_response_code == 402:
            logger.error(f"Blacklisted token {auth_response}", extra=corId)
        else:
            logger.error(
                f"Could not decode authorization token {auth_response}", extra=corId)

        message = "invalid credentials"
        response = Error(message)
        logErrorResponse(message, endText, response, corId)
        return response, 401, corId

    logger.debug(f"user_ids: {user_ids}", extra=corId)

    if auth_response is not None:
        for uId in user_ids:
            if uId != auth_response:
                logger.error(
                    f"User {auth_response} does not have permission to see user {uId}",
                    extra=corId,
                )
                message = "no permission"
                response = Error(message)

                logErrorResponse(message, endText, response, corId)
                return response, 403, corId

    response, code, error_message = get_values_influxdb_energy(
        user_ids, "energyImported", True, corId)

    if code != 200:
        logResponse(endText, response, corId)
    else:
        logErrorResponse(error_message, endText, response, corId)

    return response, code, corId


def energy_injection_get(user_ids, start_date, group_by=None, end_date=None):  # noqa: E501
    """Retrieve the energy injection for several users. The \&quot;group_by\&quot; variable is used to compute energy spent on that interval

     # noqa: E501

    :param x_correlation_id: 
    :type x_correlation_id: str
    :type x_correlation_id: str
    :param user_ids: 
    :type user_ids: List[str]
    :param start_date: 
    :type start_date: str
    :param authorization: 
    :type authorization: str
    :param group_by: 
    :type group_by: str
    :param end_date: 
    :type end_date: str

    :rtype: Union[List[EnergyMetrics], Tuple[List[EnergyMetrics], int], Tuple[List[EnergyMetrics], int, Dict[str, str]]
    """
    corId = {"X-Correlation-ID": connexion.request.headers["X-Correlation-ID"]}

    logger.info("Processing GET /energy-injection request", extra=corId)
    endText = "Processed GET /energy-injection request"

    auth_response, auth_response_code = auth.verify_basic_authorization(
        connexion.request.headers
    )

    if auth_response_code != 200:
        if auth_response_code == 402:
            logger.error(f"Blacklisted token {auth_response}", extra=corId)
        else:
            logger.error(
                f"Could not decode authorization token {auth_response}", extra=corId)

        message = "invalid credentials"
        response = Error(message)
        logErrorResponse(message, endText, response, corId)
        return response, 401, corId

    start_date = util.deserialize_datetime(start_date)
    if end_date is None:
        end_date = datetime.now(timezone.utc).strftime("%d-%m-%YT%H:%M:%S%z")
    end_date = util.deserialize_datetime(end_date)

    logger.debug(f"start: {start_date} \t end: {end_date}", extra=corId)
    logger.debug(f"user_ids: {user_ids}", extra=corId)
    logger.debug(f"group_by: {group_by}", extra=corId)

    if auth_response is not None:
        for uId in user_ids:
            if uId != auth_response:
                logger.error(
                    f"User {auth_response} does not have permission to see user {uId}",
                    extra=corId,
                )
                message = "no permission"
                response = Error(message)

                logErrorResponse(message, endText, response, corId)
                return response, 403, corId

    if group_by == None:
        group_by = "daily"

    response, code, error_message = get_values_influxdb_energy(
        user_ids, "energyExported", False, corId, start_date, end_date, group_by)

    if code != 200:
        logResponse(endText, response, corId)
    else:
        logErrorResponse(error_message, endText, response, corId)

    return response, code, corId


def energy_injection_last_get(user_ids):  # noqa: E501
    """Retrieve the last value of the energy injection for several users.

     # noqa: E501

    :param x_correlation_id: 
    :type x_correlation_id: str
    :type x_correlation_id: str
    :param user_ids: 
    :type user_ids: List[str]
    :param authorization: 
    :type authorization: str

    :rtype: Union[List[InstantEnergyMetric], Tuple[List[InstantEnergyMetric], int], Tuple[List[InstantEnergyMetric], int, Dict[str, str]]
    """
    corId = {"X-Correlation-ID": connexion.request.headers["X-Correlation-ID"]}

    logger.info("Processing GET /energy-injection-last request", extra=corId)
    endText = "Processed GET /energy-injection-last request"

    auth_response, auth_response_code = auth.verify_basic_authorization(
        connexion.request.headers
    )

    if auth_response_code != 200:
        if auth_response_code == 402:
            logger.error(f"Blacklisted token {auth_response}", extra=corId)
        else:
            logger.error(
                f"Could not decode authorization token {auth_response}", extra=corId)

        message = "invalid credentials"
        response = Error(message)
        logErrorResponse(message, endText, response, corId)
        return response, 401, corId

    logger.debug(f"user_ids: {user_ids}", extra=corId)

    if auth_response is not None:
        for uId in user_ids:
            if uId != auth_response:
                logger.error(
                    f"User {auth_response} does not have permission to see user {uId}",
                    extra=corId,
                )
                message = "no permission"
                response = Error(message)

                logErrorResponse(message, endText, response, corId)
                return response, 403, corId

    response, code, error_message = get_values_influxdb_energy(
        user_ids, "energyExported", True, corId)

    if code != 200:
        logResponse(endText, response, corId)
    else:
        logErrorResponse(error_message, endText, response, corId)

    return response, code, corId


# def _save_consumption_metric(
#     user_id, consumed_energy, metrics, fixed_timestamp, slot_number, group_by, corId
# ):
#     metric = EnergyMetric(
#         timestamp=fixed_timestamp,
#         value=consumed_energy,
#         # TODO: All data must be saved hourly and the grouped by accordingly. The measure is always kWh.
#         units="kWh",
#         slot_number=slot_number,
#     )

#     metrics.append(metric)

#     # Verificar se a métrica já existe na bd e guardar ou dar replace
#     if group_by == "monthly":
#         existing_metric = db.session.query(DBMetricsMonthly).filter(
#             extract("month", DBMetricsMonthly.timestamp) == fixed_timestamp.month,
#             extract("year", DBMetricsMonthly.timestamp) == fixed_timestamp.year,
#         ).first()

#         metric_db_obj = DBMetricsMonthly(
#             timestamp=metric.timestamp,
#             consumed_value=metric.value,
#             units=metric.units,
#             slot_number=metric.slot_number,
#             user_id=user_id,
#         )

#         if existing_metric is None:
#             logger.info(
#                 f"Metric for time - {metric.timestamp} - is not in DB. Saving....\n",
#                 extra=corId,
#             )

#             db.session.add(metric_db_obj)

#         else:
#             logger.debug(
#                 f"ID existing metric: {existing_metric.id}", extra=corId)
#             db.session.query(DBMetricsMonthly).filter_by(
#                 id=existing_metric.id).delete()
#             db.session.add(metric_db_obj)

#     elif group_by == "daily":
#         existing_metric = db.session.query(DBMetricsDaily).filter(
#             extract("month", DBMetricsDaily.timestamp) == fixed_timestamp.month,
#             extract("year", DBMetricsDaily.timestamp) == fixed_timestamp.year,
#             extract("day", DBMetricsDaily.timestamp) == fixed_timestamp.day,
#         ).first()

#         metric_db_obj = DBMetricsDaily(
#             timestamp=metric.timestamp,
#             consumed_value=metric.value,
#             units=metric.units,
#             slot_number=metric.slot_number,
#             user_id=user_id,
#         )

#         if existing_metric is None:
#             logger.info(
#                 f"Metric for time - {metric.timestamp} - is not in DB. Saving....\n",
#                 extra=corId,
#             )

#             db.session.add(metric_db_obj)

#         else:
#             logger.debug(
#                 f"ID existing metric: {existing_metric.id}", extra=corId)
#             db.session.query(DBMetricsDaily).filter_by(
#                 id=existing_metric.id).delete()
#             db.session.add(metric_db_obj)

#     elif group_by == "hourly":
#         existing_metric = db.session.query(DBMetricsHourly).filter(
#             extract("month", DBMetricsHourly.timestamp) == fixed_timestamp.month,
#             extract("year", DBMetricsHourly.timestamp) == fixed_timestamp.year,
#             extract("day", DBMetricsHourly.timestamp) == fixed_timestamp.day,
#             extract("hour", DBMetricsHourly.timestamp) == fixed_timestamp.hour,
#         ).first()

#         metric_db_obj = DBMetricsHourly(
#             timestamp=metric.timestamp,
#             consumed_value=metric.value,
#             units=metric.units,
#             slot_number=metric.slot_number,
#             user_id=user_id,
#         )

#         if existing_metric is None:
#             logger.info(
#                 f"Metric for time - {metric.timestamp} - is not in DB. Saving....\n",
#                 extra=corId,
#             )

#             db.session.add(metric_db_obj)

#         else:
#             logger.debug(
#                 f"ID existing metric: {existing_metric.id}", extra=corId)
#             db.session.query(DBMetricsHourly).filter_by(
#                 id=existing_metric.id).delete()
#             db.session.add(metric_db_obj)

#     db.session.commit()
