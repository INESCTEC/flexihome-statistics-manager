import requests, uuid, json
from datetime import datetime, timedelta, timezone

from config import Config


print("Started get users dongle data producer")

url = f"{Config.ACCOUNT_MANAGER_ENDPOINT}/user-list"
headers = {
    "X-Correlation-ID": str(uuid.uuid4())
}

response = requests.get(url, headers=headers)
response.raise_for_status()  # Raise exception when http error

user_list = json.loads(response.content)

url = f"{Config.STATISTICS_MANAGER_ENDPOINT}/users-get-real-data-producer"

for user_id in user_list:

    query_parameters = {
        "user_id": user_id,
        "start_datetime": datetime.now(timezone.utc) - timedelta(minutes=Config.LOOKBACK_PERIOD_MINUTES),
        "end_datetime": datetime.now(timezone.utc)
    }
    stats_response = requests.post(url, headers=headers, params=query_parameters)
    
    if stats_response.status_code != 201:
        print(f"ERROR {stats_response.status_code} GETTING COMPUTED FORECAST OF USER {user_id}!")
    else:
        print(f"Successfully fetched computed forecast for user {user_id}")

print("Computed forecast producer done!")
