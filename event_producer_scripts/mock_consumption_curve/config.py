import os
from datetime import datetime


class Config:

    # ENDPOINTS #

    ACCOUNT_MANAGER_ENDPOINT = os.environ.get('USER_ACCOUNT_ENDPOINT', 'http://localhost:8081/api/account')
    STATISTICS_MANAGER_ENDPOINT = os.environ.get('STATISTICS_MANAGER_ENDPOINT', 'http://localhost:8080/api/statistics')

    # FORECAST CONFIG #

    DELIVERY_TIME = int(os.environ.get("DELIVERY_TIME", "60"))

    if "FORECAST_DATE" in os.environ:
        FORECAST_DATE = datetime.strptime(os.environ.get("FORECAST_DATE"), "%Y-%m-%d")
    else:
        FORECAST_DATE = datetime.now().date()