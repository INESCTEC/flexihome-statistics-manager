import uuid

from statistics_manager_service import generalLogger, db, Config

from statistics_manager_service.event_consumer.events.events import MockConsumptionCurveSchema, ComputeMockConsumptionCurveEvent
from statistics_manager_service.models.database.db_models import DBEvent

from statistics_manager_service.exception_handling_utils.requests import request_with_exception, decode_request_response


def consumption_curve_mock_producer(user_id, start_date, delivery_time):

    generalLogger.info("Mock Consumption Curve Event Producer Begin")

    ### /user-list request ###
    url = f"{Config.ACCOUNT_MANAGER_ENDPOINT}/user"
    headers = {
        "X-Correlation-ID": str(uuid.uuid4())
    }
    query_parameters = {
        "user-ids": [user_id]
    }

    request_error_msg = "/user request failed"
    response = request_with_exception(url, request_error_msg, headers, query_parameters)

    ### /user decode request response ###
    decode_error_msg = "Error decoding /user-list response content"
    decoded_content = decode_request_response(response, decode_error_msg)

    try:
        user_info = decoded_content[0]

    except Exception as e:
        generalLogger.debug(decoded_content)
        generalLogger.error(repr(e))

        raise Exception("Response body with unexpected format")
    
    generalLogger.debug(user_info)


    ### produce mock consumption curve event ###
    mock_consumption_payload = {
        "user_id": user_id,
        "start_date": start_date,
        "delivery_time": delivery_time,
        "contracted_power": float(user_info['contracted_power'].split(" ")[0])
    }

    mock_consumption_curve_schema = MockConsumptionCurveSchema()
    payload = mock_consumption_curve_schema.dump(mock_consumption_payload)
    generalLogger.debug(payload)

    event = DBEvent(
        aggregateid=uuid.uuid4(), type=ComputeMockConsumptionCurveEvent, payload=payload
    )
    
    db.session.add(event)
    db.session.commit()
    
    
    generalLogger.info("Forecast Consumption Event Produced Successfully!")