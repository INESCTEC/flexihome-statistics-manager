# coding: utf-8

from __future__ import absolute_import
import unittest

from flask import json
from six import BytesIO

from statistics_manager_service.models.error import Error  # noqa: E501
from statistics_manager_service.test import BaseTestCase


class TestEventProducersController(BaseTestCase):
    """EventProducersController integration test stubs"""

    # def test_mock_consumption_curve_producer_post(self):
    #     """Test case for mock_consumption_curve_producer_post

    #     Trigger the service into saving a mock consumption curve (forecast + real) for a user
    #     """
    #     query_string = [('user_id', 'user_id_example'),
    #                     ('start_date', '2013-10-20'),
    #                     ('delivery_time', 60)]
    #     headers = { 
    #         'Accept': 'application/json',
    #         'x_correlation_id': 'x_correlation_id_example',
    #         'authorization': 'authorization_example',
    #         'Authorization': 'Bearer special-key',
    #     }
    #     response = self.client.open(
    #         '/api/statistics/mock-consumption-curve-producer',
    #         method='POST',
    #         headers=headers,
    #         query_string=query_string)
    #     self.assert200(response,
    #                    'Response body is : ' + response.data.decode('utf-8'))

    # def test_trigger_computed_forecast_producer_post(self):
    #     """Test case for trigger_computed_forecast_producer_post

    #     Trigger the service into saving a user's forecast data for a single day
    #     """
    #     query_string = [('user_id', 'user_id_example'),
    #                     ('forecast_day', '2013-10-20')]
    #     headers = { 
    #         'Accept': 'application/json',
    #         'x_correlation_id': 'x_correlation_id_example',
    #         'authorization': 'authorization_example',
    #         'Authorization': 'Bearer special-key',
    #     }
    #     response = self.client.open(
    #         '/api/statistics/trigger-computed-forecast-producer',
    #         method='POST',
    #         headers=headers,
    #         query_string=query_string)
    #     self.assert200(response,
    #                    'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    unittest.main()
