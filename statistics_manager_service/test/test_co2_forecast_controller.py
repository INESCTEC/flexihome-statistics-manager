# coding: utf-8

from __future__ import absolute_import
import unittest, uuid
from datetime import datetime

from statistics_manager_service.test import BaseTestCase


TIMESTAMP_FORMAT = "%Y-%m-%dT%H:%M:%SZ"


# NOTE: Only works with VPN for now

# class TestCO2ForecastController(BaseTestCase):
#     """CO2ForecastController integration test stubs"""

#     def test_co2_intensity_get(self):
#         """Test case for co2_intensity_get

#         Retrieve CO2 intensity forecast from sentinel
#         """
        
#         start_datetime = datetime.now().date()
#         query_string = [('forecast_day', start_datetime.strftime(TIMESTAMP_FORMAT))]
#         headers = { 
#             'Accept': 'application/json',
#             'x_correlation_id': str(uuid.uuid4())
#         }
#         response = self.client.open(
#             '/api/statistics/ecosignal-forecast',
#             method='GET',
#             headers=headers,
#             query_string=query_string
#         )
#         self.assert200(response, 'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    unittest.main()
