from datetime import datetime, timedelta
import connexion, json, requests, os

from statistics_manager_service.models.error import Error
from statistics_manager_service.models.co2_forecast import CO2Forecast
from statistics_manager_service import util, logger, auth
from statistics_manager_service.config import Config
from statistics_manager_service.controllers.utils import logErrorResponse


TIMESTAMP_FORMAT = os.environ.get( 'TIMESTAMP_FORMAT', str("%Y-%m-%dT%H:%M:%SZ") )


def co2_intensity_get(forecast_day):
    forecast_day = util.deserialize_date(forecast_day)
    start_datetime = datetime(forecast_day.year, forecast_day.month, forecast_day.day, 0, 0, 0)
    end_datetime = start_datetime.replace(hour=23, minute=59, second=59)

    cor_id = {"X-Correlation-ID": connexion.request.headers["X-Correlation-ID"]}

    end_text = "/ecosignal-forecast request processed with errors"
    logger.info(
        f"Precessing /ecosignal-forecast request starting " \
        f"at {start_datetime} and ending at {end_datetime}",
        extra=cor_id
    )


    # ----------------- Verify request permissions ----------------- #

    auth_response, auth_code = auth.verify_basic_authorization(
        connexion.request.headers
    )

    if auth_code != 200:

        logger.error(auth_response, extra=cor_id)
        msg = "Invalid credentials. Check logger for more info."
        response = Error(msg)

        logErrorResponse(msg, end_text, response, cor_id)
        return response, auth_code, cor_id

    elif auth_code == 200 and auth_response is not None:

        logger.info(
            f"User {auth_response} accessing from API Gateway...",
            extra=cor_id
            )

    else:
        logger.info(
            f"Request is made by an internal service. Proceeding...",
            extra=cor_id
            )
    
    
    sentinel_response = sentinel_co2_intensity_request(start_datetime, end_datetime)
    logger.debug(sentinel_response.content.decode('utf-8'), extra=cor_id)
    sentinel_response, status_code = process_sentinel_co2_intensity_response(sentinel_response, cor_id)
    
    if status_code != 200:
        start_datetime = start_datetime - timedelta(hours=24)
        end_datetime = end_datetime - timedelta(hours=24)
        
        logger.warning(
            "First attempt to get data from sentinel failed. Trying again with previous day's data.",
            extra=cor_id
        )
        sentinel_response = sentinel_co2_intensity_request(start_datetime, end_datetime)
        logger.debug(sentinel_response, extra=cor_id)
        sentinel_response, status_code = process_sentinel_co2_intensity_response(sentinel_response, cor_id)
        
        if status_code != 200:
            return sentinel_response, status_code, cor_id
    
    
    co2_emissions = []
    for co2 in sentinel_response:
        co2_emissions.append(
            CO2Forecast(
                datetime=co2['datetime'],
                request=co2['request'],
                value=co2['value'],
                unit=co2['unit'],
                quality=co2['quality'],
                updated_at=co2['updated_at']
            )
        )
    
    return co2_emissions, status_code, cor_id


def sentinel_co2_intensity_request(start_datetime: datetime, end_datetime: datetime):
    headers = {
        'accept': 'application/json', 
        'Authorization': Config.SENTINEL_TOKEN,
        'X-CSRFToken': Config.X_CSRFTOKEN
        } 
    query_params = {
        "geo_id": 1,
        'start_date' : start_datetime.strftime(TIMESTAMP_FORMAT),
        'end_date' : end_datetime.strftime(TIMESTAMP_FORMAT)
        }
    sentinel_response = requests.get(
        f"{Config.HOST_SENTINEL}/forecast/co2-intensity", 
        headers = headers, 
        params = query_params
    )
    
    return sentinel_response


def process_sentinel_co2_intensity_response(sentinel_response, cor_id):
    if 300 <= sentinel_response.status_code < 600:
        logger.error(
            "Error in sentinel eco signal request. Check debug logs for more info.",
            extra=cor_id
        )
        status_code = sentinel_response.status_code
        response = Error("Error in sentinel eco signal request.")
    
    else:

        try:
            sentinel_response = json.loads(sentinel_response.content.decode('utf-8'))
            
            if sentinel_response['rc'] != 0:
                logger.error(
                    f"Error code {str(sentinel_response['rc'])} in sentinel eco signal request. " \
                    "Check debug logs for more info.",
                    extra=cor_id
                )
                status_code = 500
                response = Error(f"Error code {str(sentinel_response['rc'])} in sentinel eco signal request.")
            
            elif len(sentinel_response['data']) == 0:
                logger.error(
                    "No data in sentinel eco signal request. Check debug logs for more info.",
                    extra=cor_id
                )
                status_code = 404
                response = Error("No data in sentinel eco signal request.")
            
            elif len(sentinel_response['data']) != 24:
                logger.warning(
                    "Sentinel eco signal request did not return data with 24 periods. " \
                    "Check debug logs for more info.",
                    extra=cor_id
                )
                logger.debug(f"Eco signal request periods: {len(sentinel_response['data'])}", extra=cor_id)
                
                # Deal with different request times
                logger.info("Getting latest request time periods.", extra=cor_id)
                max_request_time = max(
                    sentinel_response['data'],
                    key=lambda x:datetime.strptime(x['request'], TIMESTAMP_FORMAT)
                )['request']
                latest_data = [d for d in sentinel_response['data'] if d['request'] == max_request_time]
                
                if len(latest_data) != 24:
                    logger.error(
                        f"Sentinel eco signal request did not return 24 periods. " \
                        "Check debug logs for more info.",
                        extra=cor_id
                    )
                    logger.debug(f"Eco signal request periods: {len(latest_data)}", extra=cor_id)
                    status_code = 500
                    response = Error("Sentinel eco signal request returned less than 24 periods.")
                
                else:
                    logger.info(f"Sentinel data returned with correct values: {len(latest_data)}", extra=cor_id)
                    status_code = 200
                    response = latest_data

            else:
                status_code = 200
                response = sentinel_response['data']
        
        except Exception as e:
            logger.error(
                f"Sentinel response has an unexpected format. Error: {repr(e)}",
                extra=cor_id
            )
            status_code = 500
            response = Error("Sentinel response has an unexpected format.")
        
    
    return response, status_code
