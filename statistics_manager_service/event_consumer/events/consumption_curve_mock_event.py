import random
import datetime as dtime

from marshmallow import ValidationError

from statistics_manager_service import generalLogger, db
from statistics_manager_service.models.database.db_models import ForecastVsReal, DBProcessedEvent

from statistics_manager_service.event_consumer.events.events import MockConsumptionCurveSchema


#==============================================================================
DELTA_MAX        = 0.5 # Max deviation between Measurement and Forecast
#==============================================================================
TIMESTAMP_FORMAT = str("%Y-%m-%dT%H:%M:%SZ")
DELTA_DV  = 0.05
LOAD_VALUE_PU = [
    0.20832,
    0.1056,
    0.09792,
    0.08736,
    0.09696,
    0.22176,
    0.36672,
    0.5808,
    0.54432,
    0.45408,
    0.3744,
    0.38688,
    0.44064,
    0.44448,
    0.30144,
    0.28608,
    0.40504,
    0.4944,
    0.60096,
    0.5856,
    0.5136,
    0.42048,
    0.27936,
    0.25152
]


def process_consumption_curve_mock_event(session, event_id, event_type, payload):

    # -------------------------- Load Event Schema to JSON -------------------------- #

    mock_consumption_curve_schema = MockConsumptionCurveSchema()
    try:
        payload = mock_consumption_curve_schema.loads(payload)
    except ValidationError as e:
        generalLogger.error(e.messages)

        raise ValidationError("Error validating mock consumption curve schema")


    contracted_power = payload["contracted_power"]
    delivery_time = int(payload["delivery_time"])
    periods = int(24 * 60 / delivery_time)
    start_datetime = dtime.datetime(
        payload["start_date"].year, payload["start_date"].month, payload["start_date"].day, 0, 0, 0
    )

    consumption_base = []
    for dt in range(len(LOAD_VALUE_PU)): 
        consumption_base.extend([LOAD_VALUE_PU[dt] * contracted_power ] * int(60 / delivery_time))
    

        #==============================================================================
        # loop X periods for a single day
    for row in range(periods):
        
        #==============================================================================
        # datetime
        timestamp = start_datetime + dtime.timedelta(minutes=row*delivery_time)
        
        #==============================================================================
        # curve_forecast
        forecast_c = consumption_base[row] * (1 + random.uniform(-DELTA_DV, DELTA_DV) )
        if (forecast_c > contracted_power * (1-DELTA_DV)):
            forecast_c = contracted_power * (1-DELTA_DV)
        
        #==============================================================================
        # curve_measurement
        measurement_c = forecast_c * (1 + random.uniform(-DELTA_MAX, DELTA_MAX) )
        
        #==============================================================================
        # save values to db        
        existing_db_row = session.query(ForecastVsReal).filter(
            ForecastVsReal.user_id==payload["user_id"], ForecastVsReal.timestamp==timestamp
        ).first()

        # If metric is not found in DB, then save the whole row
        if existing_db_row is None:
            db_row = ForecastVsReal(
                user_id=payload["user_id"], timestamp=timestamp, 
                forecast=forecast_c, smart_meter=measurement_c, units="kW"
            )
            session.add(db_row)
        
        # If the metric already exists in the DB, save the missing measurement
        elif existing_db_row.forecast == None:
            existing_db_row.forecast = forecast_c
        
        elif existing_db_row.smart_meter == None:
            existing_db_row.smart_meter = measurement_c
        
        # In case all the measurements are already saved in the DB
        else:
            generalLogger.warning(f"User {payload['user_id']} already has energy values for {timestamp}")
    

        # ---------------------------- Save Processed Event ---------------------------- #

        # Processed event is saved under the same session as the forecast
        processed_event = DBProcessedEvent(event_type=event_type, event_id=event_id)
        session.add(processed_event)
        session.commit()


    generalLogger.info(f"Successfully process event with type {event_type} and id {event_id}")

    return
