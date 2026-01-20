import uuid
from datetime import datetime, timezone

from statistics_manager_service import Config, generalLogger, db
from statistics_manager_service.exception_handling_utils.requests import request_with_exception, decode_request_response

from statistics_manager_service.event_consumer.events.events import GetUserRealDataEvent, GetUserRealDataSchema
from statistics_manager_service.models.database.db_models import DBEvent


def produce_user_real_data_signal(user_id, start_date : datetime, end_date : datetime):
    
    
    # ---------------------------- Check if user exists ---------------------------- #
    
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
    
    
    start_date = start_date.replace(minute=0, second=0)
    if end_date > datetime.now(timezone.utc):
        end_date = datetime.now(timezone.utc)
    
    generalLogger.info(f"Producing signal to get user {user_id} real data from {start_date} to {end_date}...")

    
    # -------------------------------- Produce event -------------------------------- #
    
    get_user_real_data_payload = {
        "user_id": user_id,
        "start_date": start_date,
        "end_date": end_date
    }

    get_user_real_data_schema = GetUserRealDataSchema()
    payload = get_user_real_data_schema.dump(get_user_real_data_payload)
    generalLogger.debug(payload)

    event = DBEvent(
        aggregateid=uuid.uuid4(), type=GetUserRealDataEvent, payload=payload
    )
    
    db.session.add(event)
    db.session.commit()
    
    generalLogger.info("Get User Real Data Event Produced Successfully!\n")
