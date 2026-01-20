import connexion

from statistics_manager_service.models.error import Error
from statistics_manager_service.config import Config
from statistics_manager_service import auth, logger, db, app, util
from statistics_manager_service.controllers.utils import get_values_influxdb_voltage, logResponse, logErrorResponse

from datetime import datetime, timezone

def voltage_get(user_ids, start_date, group_by=None, end_date=None):  # noqa: E501
    """Retrieve the voltage values for several users. The \&quot;group_by\&quot; variable is used to compute the average value between that interval

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

    :rtype: Union[List[VoltageMetrics], Tuple[List[VoltageMetrics], int], Tuple[List[VoltageMetrics], int, Dict[str, str]]
    """
    corId = {"X-Correlation-ID": connexion.request.headers["X-Correlation-ID"]}

    logger.info("Processing GET /voltage request", extra=corId)
    endText = "Processed GET /voltage request"

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

    response, code, error_message = get_values_influxdb_voltage(
        user_ids, "voltage", False, corId, start_date, end_date, group_by)

    if code != 200:
        logResponse(endText, response, corId)
    else:
        logErrorResponse(error_message, endText, response, corId)

    return response, code, corId


def voltage_last_get(user_ids):  # noqa: E501
    """Retrieve the last voltage value for several users.

     # noqa: E501

    :param x_correlation_id: 
    :type x_correlation_id: str
    :type x_correlation_id: str
    :param user_ids: 
    :type user_ids: List[str]
    :param authorization: 
    :type authorization: str

    :rtype: Union[List[InstantVoltageMetric], Tuple[List[InstantVoltageMetric], int], Tuple[List[InstantVoltageMetric], int, Dict[str, str]]
    """
    corId = {"X-Correlation-ID": connexion.request.headers["X-Correlation-ID"]}

    logger.info("Processing GET /voltage-last request", extra=corId)
    endText = "Processed GET /voltage-last request"

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

    response, code, error_message = get_values_influxdb_voltage(
        user_ids, "voltage", True, corId)

    if code != 200:
        logResponse(endText, response, corId)
    else:
        logErrorResponse(error_message, endText, response, corId)

    return response, code, corId
