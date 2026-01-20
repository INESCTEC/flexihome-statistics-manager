import uuid

from statistics_manager_service import Config, generalLogger, db

from statistics_manager_service.event_consumer.events.events import ForecastComputedSchema, ForecastComputedEvent
from statistics_manager_service.models.database.db_models import DBEvent

from statistics_manager_service.exception_handling_utils.requests import request_with_exception, decode_request_response


def forecast_consumption_users_event_producer(user_id, forecast_date):

    generalLogger.info("Forecast Consumption Event Producer Begin")

    ### /user request ###
    url = f"{Config.ACCOUNT_MANAGER_ENDPOINT}/user"
    headers = {
        "X-Correlation-ID": str(uuid.uuid4())
    }
    query_parameters = {
        "user-ids": [user_id]
    }

    request_error_msg = "/user request failed"
    response = request_with_exception(url, request_error_msg, headers, query_parameters)

    ### /user-list decode request response ###
    decode_error_msg = "Error decoding /user response content"
    decoded_content = decode_request_response(response, decode_error_msg)

    try:
        user_info = decoded_content[0]

    except Exception as e:
        generalLogger.debug(decoded_content)
        generalLogger.error(repr(e))

        raise Exception("Response body with unexpected format")


    ### produce forecast computed event ###
    forecast_schema = {
        "user_id": user_id,
        "forecast_date": forecast_date
    }

    forecast_computed_schema = ForecastComputedSchema()
    payload = forecast_computed_schema.dump(forecast_schema)
    generalLogger.debug(payload)

    event = DBEvent(
        aggregateid=uuid.uuid4(), type=ForecastComputedEvent, payload=payload
    )
    
    db.session.add(event)
    db.session.commit()
    
    generalLogger.info("Forecast Consumption Event Produced Successfully!")
