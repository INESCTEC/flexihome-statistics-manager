import json, traceback

from statistics_manager_service import generalLogger

from statistics_manager_service.event_consumer.events.events import ForecastComputedEvent, ComputeMockConsumptionCurveEvent, GetUserRealDataEvent
from statistics_manager_service.models.database.db_models import DBProcessedEvent
from statistics_manager_service.event_consumer.events.forecast_computed_event import process_forecast_computed_event
from statistics_manager_service.event_consumer.events.consumption_curve_mock_event import process_consumption_curve_mock_event
from statistics_manager_service.event_consumer.events.get_user_real_data_event import process_get_user_real_data_event


def process_events(session, message):

    # Convert bytes to json and retrieve the "payload" field
    event = json.loads(message.value)
    event_id = event["payload"]["eventId"]
    event_type = event["payload"]["eventType"]
    payload = event["payload"]["payload"]

    # Check if event has already been processed
    processedEvent = session.query(DBProcessedEvent).filter_by(event_type=event_type, event_id=event_id).first()

    if (processedEvent != None):
        generalLogger.error(f"Event {event_type} / {event_id} already processed")
        return

    
    generalLogger.info(f"Processing event {event_id} / {event_type}")
    
    try:
        if event_type == ForecastComputedEvent:
            process_forecast_computed_event(session, event_id, event_type, payload)
        
        elif event_type == ComputeMockConsumptionCurveEvent:
            process_consumption_curve_mock_event(session, event_id, event_type, payload)
            
        elif event_type == GetUserRealDataEvent:
            process_get_user_real_data_event(session, event_id, event_type, payload)
    
    except Exception as e:
        generalLogger.error(f"Failed to process event with type {event_type} and id {event_id}\n")
        traceback.print_exc()
        generalLogger.error(repr(e))
