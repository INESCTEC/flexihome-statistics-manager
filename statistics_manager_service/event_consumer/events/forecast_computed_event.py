from datetime import datetime
from marshmallow import ValidationError
from sqlalchemy import extract

from statistics_manager_service import generalLogger, Config, db
from statistics_manager_service.event_consumer.events.events import ForecastComputedSchema
from statistics_manager_service.models.database.db_models import ForecastVsReal, DBProcessedEvent

from statistics_manager_service.exception_handling_utils.requests import request_with_exception, decode_request_response


FORECAST_DATE_FORMAT = "%Y-%m-%dT%H:%M:%SZ"


def process_forecast_computed_event(session, event_id, event_type, payload):

    # -------------------------- Load Event Schema to JSON -------------------------- #

    forecast_computed_schema = ForecastComputedSchema()
    try:
        payload = forecast_computed_schema.loads(payload)
    except ValidationError as e:
        generalLogger.error(e.messages)

        raise ValidationError("Error validating forecast computed schema")


    # ---------------------------- Process Event Payload ---------------------------- #

    user_id = payload["user_id"]
    forecast_day = payload["forecast_date"].day
    forecast_month = payload["forecast_date"].month
    forecast_year = payload["forecast_date"].year

    generalLogger.info(f"Getting forecast for user: {user_id}")

    ### Process /get-forecast request parameters ###
    start_date = datetime(forecast_year, forecast_month, forecast_day, 0, 0, 0).isoformat()
    end_date = datetime(forecast_year, forecast_month, forecast_day, 23, 59, 00).isoformat()
    installation_code = f"{user_id}_consumption"

    generalLogger.debug(
        "Forecast Request Parameters:\n" \
        f"start_date: {start_date}\n" \
        f"end_date: {end_date}\n" \
        f"installation_code: {installation_code}"
    )

    ### /get-forecast request ###
    url = f"{Config.FORECAST_API_URL}/get-forecast"
    query_parameters = {
        "start_date": start_date,
        "end_date": end_date,
        "installation_code": installation_code
    }

    request_error_msg = f"Error getting the forecast of user {user_id}\n"
    response = request_with_exception(url, request_error_msg, query_parameters=query_parameters)
    
    
    ### Handle /get-forecast response content ###
    decode_error_msg = "Error decoding /get-forecast response content"
    decoded_content = decode_request_response(response, decode_error_msg)
    
    try:
        user_forecast = decoded_content['data'][0]

    except Exception as e:
        generalLogger.debug(decoded_content)
        generalLogger.error(repr(e))

        raise Exception("Response body with unexpected format")
    
    generalLogger.debug(user_forecast)


    ### Save user's forecast values in database ###
    
    for forecast_value in user_forecast["values"]:
        timestamp = forecast_value["timestamp"]
        timestamp = datetime.strptime(timestamp, FORECAST_DATE_FORMAT)

        power_unit = user_forecast["units_p"]
        if power_unit == "W":
            power_value = round(forecast_value["value_p"] / 1000, 1) # Transform in kW
            power_unit = "kW"
        else:
            power_value = round(forecast_value["value_p"], 1)

        # Check if forecast metric for this user already exists
        existing_metric = session.query(ForecastVsReal).filter(
            ForecastVsReal.user_id == user_id,
            extract("month", ForecastVsReal.timestamp) == timestamp.month,
            extract("year", ForecastVsReal.timestamp) == timestamp.year,
            extract("day", ForecastVsReal.timestamp) == timestamp.day,
            extract("hour", ForecastVsReal.timestamp) == timestamp.hour,
        ).first()

        if existing_metric is not None:
            if existing_metric.forecast is None:
                existing_metric.forecast = power_value
        
        else:
            forecast_db_obj = ForecastVsReal(
                user_id=user_id, timestamp=timestamp, forecast=power_value, units=power_unit
            )
            session.add(forecast_db_obj)
        

    # ---------------------------- Save Processed Event ---------------------------- #

    processed_event = DBProcessedEvent(event_type=event_type, event_id=event_id)
    session.add(processed_event)
    session.commit()


    generalLogger.info(f"Successfully process event with type {event_type} and id {event_id}")
    
    return
