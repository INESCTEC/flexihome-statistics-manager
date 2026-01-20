import requests, uuid, statistics
from datetime import datetime
from marshmallow import ValidationError
from sqlalchemy import extract

from typing import List

from statistics_manager_service import generalLogger, query_api, db, Config, INFLUX_DB_DATE_FORMAT
from statistics_manager_service.models.database.db_models import ForecastVsReal
from statistics_manager_service.event_consumer.events.events import GetUserRealDataSchema
from statistics_manager_service.models.database.db_models import DBProcessedEvent


def process_hourly_values(data, second_timestamp : datetime):
    """
    Processes a list of values and timestamps, calculating the mean value for each hour change.

    Args:
        data (list): A list of tuples containing values and corresponding timestamps.
        second_timestamp (str): The timestamp of the second value in the data list.

    Returns:
        tuple: A tuple containing two lists - mean_values and timestamps.

    Raises:
        ValueError: If the timestamp format is incorrect.

    """
    mean_values = []
    timestamps = []
    
    values = []
    next_hour = second_timestamp.hour
    for i in range(len(data)):
        value, timestamp = data[i]
        values.append(value)
        
        if i < len(data) - 1:
            _, next_timestamp = data[i + 1]
            next_hour = next_timestamp.hour
        else:
            # If it's the last value, assume the next hour is different
            next_hour = None
        
        current_hour = timestamp.hour

        if current_hour != next_hour:
            # Process the value since the hour will change
            mean_value = statistics.mean(values)
            values = []
            
            generalLogger.debug(f"Processing value {mean_value} at timestamp {timestamp}")
            
            mean_values.append(mean_value)
            timestamps.append(timestamp.replace(minute=0, second=0))
    
    return mean_values, timestamps


def process_get_user_real_data_event(session, event_id, event_type, payload):
    """
    Process the event payload. Get the user's (user_id) data from influx db on the requested date interval (start_date, end_date).
    Save the data from the influxDB on the statistics_manager_service database.
    """

    # -------------------------- Load Event Schema to JSON -------------------------- #

    get_user_real_data_schema = GetUserRealDataSchema()
    try:
        payload = get_user_real_data_schema.loads(payload)
    except ValidationError as e:
        generalLogger.error(e.messages)

        raise ValidationError("Error validating forecast computed schema")


    # ---------------------------- Process Event Payload ---------------------------- #
    
    formatted_start_date = payload["start_date"].strftime(INFLUX_DB_DATE_FORMAT)
    formatted_end_date = payload["end_date"].strftime(INFLUX_DB_DATE_FORMAT)
    
    
    # --------------------------- Get user dongle API Key --------------------------- #
    
    generalLogger.info(f"Getting user {payload['user_id']} info...")
    
    headers = {
        "X-Correlation-ID": str(uuid.uuid4())
    }
    query_parameters = {
        "user-ids": [payload["user_id"]]
    }
    response = requests.get(
        f"{Config.ACCOUNT_MANAGER_ENDPOINT}/user", headers=headers, params=query_parameters
    )
    response.raise_for_status()
    response = response.json()
    dongle_api_key = response[0]["api_key"]  # Throw exception if user does not have dongle api key
    generalLogger.debug(f"User {payload['user_id']} has dongle api key: {dongle_api_key}")
    
    # TODO: If user does not have dongle api key, get data ONLY from smart meters
    
    generalLogger.info(f"Getting user {payload['user_id']} info... OK")
    
    
    # --------------------- Query InfluxDB for user dongle data --------------------- #
    
    generalLogger.info("Querying dongle from influxdb...")
    
    query = f"""from(bucket: "{Config.INFLUX_BUCKET}") 
            |> range(start: {formatted_start_date}, stop: {formatted_end_date}) 
            |> filter(fn: (r) => r["_measurement"] == "{dongle_api_key}") 
            |> filter(fn: (r) => r["_field"] == "powerImported")"""
    generalLogger.debug(f"Query: {query}")

    result = query_api.query(query=query)
    
    generalLogger.info("Querying dongle from influxdb... OK")
    generalLogger.debug(f"Query result: {result}")
    
    
    # --------- Save user dongle data to statistics_manager_service database --------- #
    
    if len(result) != 0:
        records = result[0].records
        
        power_consumed : List[float] = [record.get_value() for record in records]
        timestamps : List[datetime] = [record.get_time() for record in records]
        
        data = list(zip(power_consumed, timestamps))
        power_consumed, timestamps = process_hourly_values(data, timestamps[1])
        
        # Loop influx query results and save them to the database
        for power, timestamp in zip(power_consumed, timestamps):
            
            power_value = round(power / 1000, 1) # Transform in kW
            power_unit = "kW"
            
            # Check if forecast metric for this user already exists
            existing_metric = session.query(ForecastVsReal).filter(
                ForecastVsReal.user_id == payload["user_id"],
                extract("month", ForecastVsReal.timestamp) == timestamp.month,
                extract("year", ForecastVsReal.timestamp) == timestamp.year,
                extract("day", ForecastVsReal.timestamp) == timestamp.day,
                extract("hour", ForecastVsReal.timestamp) == timestamp.hour,
            ).first()

            if existing_metric is not None:
                if existing_metric.dongle is None:
                    existing_metric.dongle = power_value
            
            else:
                dongle_db_obj = ForecastVsReal(
                    user_id=payload["user_id"], timestamp=timestamp, dongle=power_value, units=power_unit
                )
                session.add(dongle_db_obj)
    
    
    # ---------------------------- Save Processed Event ---------------------------- #

    processed_event = DBProcessedEvent(event_type=event_type, event_id=event_id)
    session.add(processed_event)
    session.commit()


    generalLogger.info(f"Successfully process event with type {event_type} and id {event_id}\n")
    
    return
