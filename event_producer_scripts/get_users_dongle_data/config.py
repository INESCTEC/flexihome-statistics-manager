import os


class Config:

    # ENDPOINTS #

    ACCOUNT_MANAGER_ENDPOINT = os.environ.get('USER_ACCOUNT_ENDPOINT', 'http://account-manager.default.svc.cluster.local:8080/api/account')
    STATISTICS_MANAGER_ENDPOINT = os.environ.get('STATISTICS_MANAGER_ENDPOINT', 'http://localhost:8080/api/statistics')

    LOOKBACK_PERIOD_MINUTES = int(os.environ.get('LOOKBACK_PERIOD_MINUTES', "15"))
