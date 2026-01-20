import os
from datetime import datetime, timedelta


class Config:

    # ENDPOINTS #

    ACCOUNT_MANAGER_ENDPOINT = os.environ.get('USER_ACCOUNT_ENDPOINT', 'http://account-manager.default.svc.cluster.local:8080/api/account')
    STATISTICS_MANAGER_ENDPOINT = os.environ.get('STATISTICS_MANAGER_ENDPOINT', 'http://localhost:8080/api/statistics')

    # FORECAST CONFIG #

    if "FORECAST_DATE" in os.environ:
        FORECAST_DATE = datetime.strptime(os.environ.get("FORECAST_DATE"), "%Y-%m-%d")
    else:
        FORECAST_DATE = datetime.now().date()
