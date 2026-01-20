import connexion, traceback

from statistics_manager_service import logger, util
from statistics_manager_service.event_producers.forecast_consumption_users_producer import forecast_consumption_users_event_producer
from statistics_manager_service.event_producers.consumption_curve_mock_producer import consumption_curve_mock_producer
from statistics_manager_service.event_producers.get_user_real_data_producer import produce_user_real_data_signal

from statistics_manager_service.models.error import Error
from statistics_manager_service.exception_handling_utils.auth import verify_hems_auth

from datetime import datetime, timezone

def mock_consumption_curve_producer_post(user_id, start_date, delivery_time):  # noqa: E501
    """Trigger the service into saving a mock consumption curve (forecast + real) for a user

    Mocks a user&#39;s &lt;user_id&gt; consumption curve for a single day &lt;start_date&gt;. The curve consists of the energy consumption forecast and the real energy consumption. The curve&#39;s interval between values is given by &lt;delivery_time&gt; minutes. # noqa: E501

    :param x_correlation_id: 
    :type x_correlation_id: str
    :type x_correlation_id: str
    :param user_id: 
    :type user_id: str
    :param start_date: 
    :type start_date: str
    :param delivery_time: 
    :type delivery_time: int
    :param authorization: 
    :type authorization: str

    :rtype: Union[None, Tuple[None, int], Tuple[None, int, Dict[str, str]]
    """
    cor_id = {"X-Correlation-ID": connexion.request.headers["X-Correlation-ID"]}

    end_text = "Processed POST /mock-consumption-curve-producer request"
    operation_text = f"Produce a message to mock the consumption curve for user {user_id}"
    logger.info(operation_text, extra=cor_id)

    start_date = util.deserialize_date(start_date)

    logger.debug(f"user id: {user_id}", extra=cor_id)
    logger.debug(f"start_date: {start_date}", extra=cor_id)
    logger.debug(f"delivery time: {delivery_time}", extra=cor_id)

    response = Error("Unknown Server Error. Check logs for more information.")
    response_code = 500


    # -------------------------- Verify request permissions -------------------------- #

    response, response_code, _ = verify_hems_auth(
        connexion.request.headers, user_ids=None, 
        end_text=end_text, cor_id=cor_id, internal_request=True
    )

    if response_code == 200:
        try:
            consumption_curve_mock_producer(user_id, start_date, delivery_time)
            response = ""
            response_code = 201
        
        except Exception as e:
            logger.error(repr(e), extra=cor_id)
            traceback.print_exc()
            response = Error(repr(e))
            response_code = 503
   
   
    return response, response_code, cor_id


def trigger_computed_forecast_producer_post(user_id, forecast_day):  # noqa: E501
    """Trigger the service into saving a user&#39;s forecast data for a single day

     # noqa: E501

    :param x_correlation_id: 
    :type x_correlation_id: str
    :type x_correlation_id: str
    :param user_id: 
    :type user_id: str
    :param forecast_day: 
    :type forecast_day: str
    :param authorization: 
    :type authorization: str

    :rtype: Union[None, Tuple[None, int], Tuple[None, int, Dict[str, str]]
    """
    cor_id = {"X-Correlation-ID": connexion.request.headers["X-Correlation-ID"]}

    end_text = "Processed POST /all-users-forecast-producer request"
    operation_text = "Produce a message with all HEMS users to save their forecast in the statistics database"
    logger.info(operation_text, extra=cor_id)

    forecast_day = util.deserialize_date(forecast_day)

    logger.debug(f"user id: {user_id}", extra=cor_id)
    logger.debug(f"start_date: {forecast_day}", extra=cor_id)

    response = Error("Unknown Server Error. Check logs for more information.")
    response_code = 500


    # -------------------------- Verify request permissions -------------------------- #

    response, response_code, _ = verify_hems_auth(
        connexion.request.headers, user_ids=None, 
        end_text=end_text, cor_id=cor_id, internal_request=True
    )

    # Produce the event
    if response_code == 200:
        try:
            forecast_consumption_users_event_producer(user_id, forecast_day)
            response = ""
            response_code = 201
        
        except Exception as e:
            logger.error(repr(e), extra=cor_id)
            traceback.print_exc()
            response = Error(repr(e))
            response_code = 503


    return response, response_code, cor_id


def users_get_real_data_producer_post(user_id, start_datetime, end_datetime):
    """
    Example: curl -X 'POST' 'http://localhost:8080/api/statistics/users-get-real-data-producer?user_id=clv6vzenep&start_date=2023-05-18T10:20:00&end_date=2023-05-19T10:30:00' -H 'X-Correlation-ID: 264a562c-6dc0-4cf6-80f5-aeeb22f131d5' -d ''
    """
    cor_id = {"X-Correlation-ID": connexion.request.headers["X-Correlation-ID"]}
    
    end_text = "Processed POST /all-users-forecast-producer request"
    logger.info(
        f"Produce a signal to input the user {user_id} real data into the statistics manager database",
        extra=cor_id
    )
    
    start_datetime = util.deserialize_datetime(start_datetime)
    if end_datetime is None:
        end_datetime = datetime.now(timezone.utc).strftime("%d-%m-%YT%H:%M:%S%z")
    end_datetime = util.deserialize_datetime(end_datetime)
    
    logger.debug(f"user id: {user_id}", extra=cor_id)
    logger.debug(f"start_date: {start_datetime}", extra=cor_id)
    logger.debug(f"end_date: {end_datetime}", extra=cor_id)
    
    response = Error("Unknown Server Error. Check logs for more information.")
    response_code = 500
    
    
    # -------------------------- Verify request permissions -------------------------- #
    
    response, response_code, _ = verify_hems_auth(
        connexion.request.headers, user_ids=None, 
        end_text=end_text, cor_id=cor_id, internal_request=True
    )
    
    if start_datetime > end_datetime:
        response = Error("Start date must be before end date")
        response_code = 400
    
    
    # Produce the event
    if response_code == 200:
        try:
            produce_user_real_data_signal(user_id, start_datetime, end_datetime)
            response = ""
            response_code = 201
        
        except Exception as e:
            logger.error(repr(e), extra=cor_id)
            traceback.print_exc()
            response = Error(repr(e))
            response_code = 503
    
    
    return response, response_code, cor_id
