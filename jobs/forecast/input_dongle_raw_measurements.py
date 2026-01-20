import requests, json, uuid
from datetime import datetime, timedelta
from typing import List

from init import logger, query_api, Config


INFLUX_DB_DATE_FORMAT = "%Y-%m-%dT%H:%M:%SZ"
FORECAST_DATE_FORMAT = "%Y-%m-%dT%H:%M:%SZ"


def input_dongle_raw_measurements():
    
    # List dongles
    logger.info("List dongles from account manager...")
    headers =  {
        "X-Correlation-ID": str(uuid.uuid4())
    }

    response = requests.get(f"{Config.ACCOUNT_MANAGER_ENDPOINT}/list-dongles", headers=headers)
    response.raise_for_status()

    json_response = json.loads(response.content.decode('utf-8'))
    logger.info("List dongles from account manager... OK")
    logger.debug(json.dumps(json_response, indent=4))


    for user_dongle_pair in json_response:
        
        # Check if installation code exists
        installation_code = f"{user_dongle_pair['user_id']}_consumption"
        
        logger.info(f"Cheking if installation code {installation_code} exists...")
        
        headers = {
            "Authorization": ""
        }
        query_parameters = {
            "installation_code": installation_code
        }
        response = requests.get(f"{Config.FORECAST_SERVICE_ENDPOINT}/installations/info", params=query_parameters, headers=headers)
        response.raise_for_status()
        
        json_response = json.loads(response.content.decode('utf-8'))
        logger.debug(json.dumps(json_response, indent=4))
        
        logger.info(f"Cheking if installation code {installation_code} exists... OK")
        
        
        # If installation code exists, query dongle bucket and POST raw measurements to forecast service
        if json_response["code"] == 1 and len(json_response["data"]) > 0:
        
            logger.info(f"Querying dongle {user_dongle_pair['api_key']} from influxdb...")
            
            # Query dongle bucket
            start_date = datetime.now() - timedelta(days=1)
            formatted_start_date = start_date.strftime(INFLUX_DB_DATE_FORMAT)
            formatted_end_date = datetime.now().strftime(INFLUX_DB_DATE_FORMAT)
            
            logger.debug(f"Start date: {formatted_start_date}")
            logger.debug(f"End date: {formatted_end_date}\n")

            query = f"""from(bucket: "{Config.INFLUX_BUCKET}") 
            |> range(start: {formatted_start_date}, stop: {formatted_end_date}) 
            |> filter(fn: (r) => r["_measurement"] == "{user_dongle_pair['api_key']}") 
            |> filter(fn: (r) => r["_field"] == "powerImported")"""

            logger.debug(f"Query: {query}\n")

            result = query_api.query(query=query)
            logger.info("Querying dongle from influxdb... OK")
            logger.debug(f"Result: {result}\n")
            
            
            if len(result) != 0:
                records = result[0].records
                
                power_consumed : List[float] = [round(record.get_value() / 1000, 2) for record in records]  # convert W to kW (forecast service expects kW)
                timestamps : List[datetime] = [record.get_time() for record in records]

                # logger.debug(f"Power consumed: {power_consumed}")
                
                # POST raw measurements to forecast service
                values = []
                for power, timestamp in zip(power_consumed, timestamps):
                    # q: How to convert timestamp to local timezone?
                    # a: https://stackoverflow.com/a/4770297/10930878
                    # from_zone = tz.tzutc()  # timestamp is in utc (not naive)
                    # to_zone = tz.tzlocal()
                    # timestamp_local = timestamp.astimezone(to_zone)
                    
                    # Forecast expects timestamp in UTC
                    value = {
                        "timestamp": timestamp.strftime(FORECAST_DATE_FORMAT),
                        "units": "kW",
                        "value": power,
                        "variable_name": "A+"
                    }
                    values.append(value)
                
                data = {
                    "measurements": [
                        {
                            "installation_code": f"{user_dongle_pair['user_id']}_consumption",
                            "values": values
                        }
                    ]
                }
                headers = {
                    "X-Correlation-ID": str(uuid.uuid4()),
                    "Authorization": ""
                }
                
                response = requests.post(f"{Config.FORECAST_SERVICE_ENDPOINT}/forecast/measurements", json=data, headers=headers)
                response.raise_for_status()
                
                json_response = json.loads(response.content.decode('utf-8'))
                logger.debug(json.dumps(json_response, indent=4))
                
                # Check if forecast measurements POST was successful
                if json_response["code"] == 1:
                    logger.info(f"POSTed raw measurements to forecast service: {len(values)}\n")
                
                else:
                    logger.error(f"Failed to POST raw measurements for installation code {user_dongle_pair['user_id']}_consumption")
                    logger.error(f"{json_response['message']}\n")
            
            else:
                logger.warning(f"No results found for dongle with API key {user_dongle_pair['api_key']} from user {user_dongle_pair['user_id']}\n")
        
        else:
            logger.error(f"Failed to get installation info for installation code {installation_code}\n")
            

# Run the script
input_dongle_raw_measurements()
