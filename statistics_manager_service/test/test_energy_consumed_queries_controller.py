# # coding: utf-8

# from __future__ import absolute_import
# import unittest

# from flask import json
# from six import BytesIO

# from statistics_manager_service.models.consumption_metrics import (
#     ConsumptionMetrics,
# )  # noqa: E501
# from statistics_manager_service.models.error import Error  # noqa: E501
# from statistics_manager_service.test import BaseTestCase
# from statistics_manager_service.config import Config
# from statistics_manager_service import logger

# import uuid

# import requests

# TEST_EMAIL = "andre.f.coelho@inesctec.pt"
# TEST_PASSWORD = "12345678"
# TEST_USER_ID = "amicj06h7u"


# def get_login_token(user_email, user_password):
#     x_correlation_id = str(uuid.uuid4())

#     headers = {
#         "accept": "*/*",
#         "X-Correlation-ID": x_correlation_id,
#         # Already added when you pass json= but not when you pass data=
#         # 'Content-Type': 'application/json',
#     }

#     json_data = {
#         "email": user_email,
#         "password": user_password,
#     }
    
#     try:
#         response = requests.post(
#             "http://" + Config.ACCOUNT_MANAGER_ENDPOINT + "/login",
#             headers=headers,
#             json=json_data,
#         )

#         """Obtains the Access Token from the Authorization Header
#         """
#         auth = response.headers.get("Authorization", None)
#         if not auth:
#             logger.error(401, "Authorization header is expected")

#         parts = auth.split()

#         if parts[0].lower() != "bearer":
#             message = "One or more users in user_ids parameter were not found."
#             response = Error(message)
#             logger.error(message + "\n", extra=x_correlation_id)
#             return response, 401, x_correlation_id
#         elif len(parts) == 1:
#             message = "Invalid header, token not found"
#             response = Error(message)
#             logger.error(message + "\n", extra=x_correlation_id)
#             return response, 401, x_correlation_id
#         elif len(parts) > 2:
#             message = 'Authorization header must be in the form of "Bearer token"'
#             response = Error(message)
#             logger.error(message + "\n", extra=x_correlation_id)
#             return response, 401, x_correlation_id
#         return auth
#     except:
#         message = (
#             "Exception caught when calling account manager login to get auth token."
#         )
#         response = Error(message)
#         logger.error(message + "\n", extra=x_correlation_id)
#         return response, 404, x_correlation_id


# class TestEnergyConsumedQueriesController(BaseTestCase):
#     """EnergyConsumedQueriesController integration test stubs"""

#     '''def test_energy_usage_cost_get(self):
#         """Test case for energy_usage_cost_get

#         Retrieve the energy consumption cost for several users.
#         """
#         query_string = [('user_ids', TEST_USER_ID),
#                         ('group_by', 'daily'),
#                         ('start_date', '2022-04-20T19:20:30+01:00'),
#                         ('end_date', '2022-04-22T19:20:30+01:00')]
#         token=get_login_token(TEST_EMAIL,TEST_PASSWORD)
#         headers = { 
#             'Accept': 'application/json',
#             'x_correlation_id': uuid.uuid4(),
#             'authorization': token,
#         }
#         response = self.client.open(
#             '/api/statistics/energy-usage-cost',
#             method='GET',
#             headers=headers,
#             query_string=query_string)
#         self.assert200(response,
#                        'Response body is : ' + response.data.decode('utf-8'))'''

#     def test_energy_usage_get(self):
#         """Test case for energy_usage_get

#         Retrieve the energy consumption for several users.
#         """
#         query_string = [
#             ("user_ids", TEST_USER_ID),
#             ("group_by", "daily"),
#             ("start_date", "2022-04-20T19:20:30+01:00"),
#             ("end_date", "2022-04-21T19:20:30+01:00"),
#         ]
#         token = get_login_token(TEST_EMAIL, TEST_PASSWORD)
#         headers = {
#             "Accept": "application/json",
#             "x_correlation_id": uuid.uuid4(),
#             "authorization": token,
#         }

#         response = self.client.open(
#             "/api/statistics/energy-usage",
#             method="GET",
#             headers=headers,
#             query_string=query_string,
#         )
#         self.assert200(response, "Response body is : " + response.data.decode("utf-8"))


# if __name__ == "__main__":
#     unittest.main()

# coding: utf-8

from __future__ import absolute_import
import unittest

from flask import json
from six import BytesIO

from statistics_manager_service.models.error import Error  # noqa: E501
from statistics_manager_service.models.forecast_vs_real import ForecastVsReal  # noqa: E501
from statistics_manager_service.test import BaseTestCase


# class TestEnergyConsumedQueriesController(BaseTestCase):
#     """EnergyConsumedQueriesController integration test stubs"""

#     def test_energy_consumed_forecast_vs_real_get(self):
#         """Test case for energy_consumed_forecast_vs_real_get

#         List of user's forecasted energy consumption vs. real consumption
#         """
#         query_string = [('user_ids', ['[\"userId1\",\"userId2\"]']),
#                         ('group_by', 'daily'),
#                         ('start_date', '2013-10-20'),
#                         ('end_date', '2013-10-20')]
#         headers = { 
#             'Accept': 'application/json',
#             'x_correlation_id': 'x_correlation_id_example',
#             'authorization': 'authorization_example',
#             'Authorization': 'Bearer special-key',
#         }
#         response = self.client.open(
#             '/api/statistics/energy-consumed-forecast-vs-real',
#             method='GET',
#             headers=headers,
#             query_string=query_string)
#         self.assert200(response,
#                        'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    unittest.main()

