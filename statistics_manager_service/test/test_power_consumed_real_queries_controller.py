import unittest

from flask import json

from datetime import datetime, timezone
import uuid

from statistics_manager_service.models.error import Error  # noqa: E501
from statistics_manager_service.models.instant_power_metric import InstantPowerMetric  # noqa: E501
from statistics_manager_service.models.power_metrics import PowerMetrics  # noqa: E501
from statistics_manager_service.test import BaseTestCase

from statistics_manager_service.test.helper_functions import (
    clean_account,
    clean_influxdb,
    populate_influxdb_power_meter_imported,
    populate_influxdb_energy_imported,
    mock_register,
    superuser_login,
)


class TestPowerQueriesControllerConsumptionReal(BaseTestCase):
    """PowerQueriesController integration test stubs"""

    # editing dongles test
    def test_power_consumption_get_daily(self):
        """Test case for power_consumption_get

        Retrieve the power consumption for one user. The \"group_by\" variable is used to compute the average value between that interval
        """
        clean_account()

        clean_influxdb()

        populate_influxdb_energy_imported()  # energyImported dongles
        user_key, user_id, second_user_key, second_user_id = mock_register()

        authorization = superuser_login(id=user_key)

        query_string = [('user_id', user_id),
                        ('group_by', 'daily'),
                        ('start_date', '2022-04-26T00:00:00+00:00'),
                        ('end_date', '2022-05-08T23:59:00+00:00')]
        headers = {
            'Accept': 'application/json',
            'x_correlation_id': str(uuid.uuid4()),
            'Authorization': authorization,
        }
        response = self.client.open(
            '/api/statistics/power-consumed-real',
            method='GET',
            headers=headers,
            query_string=query_string,
        )
        
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

        metrics = json.loads(response.data.decode("utf-8"))

        metrics_dict = {}
        for metric in metrics[0]['real']:
            metrics_dict[str(metric["slot_number"])] = {
                "timestamp": metric["timestamp"], "energy": metric["energy"], "units": metric["units"]}

        self.assertEqual(metrics[0]["user_id"], user_id)

        self.assertEqual(datetime.fromisoformat(metrics_dict["1"]["timestamp"]),
                         datetime(2022, 4, 28, 0, 0, tzinfo=timezone.utc))
        self.assertEqual(metrics_dict["1"]["units"], 'kWh')
        self.assertEqual(metrics_dict["1"]["energy"], 0)

        self.assertEqual(datetime.fromisoformat(metrics_dict["9"]["timestamp"]),
                         datetime(2022, 5, 6, 0, 0, tzinfo=timezone.utc))
        self.assertEqual(metrics_dict["9"]["units"], 'kWh')

        self.assertGreaterEqual(metrics_dict["9"]["energy"], 45.5-43.9)
        self.assertLessEqual(metrics_dict["9"]["energy"], 46.3-38.3)

        self.assertEqual(datetime.fromisoformat(metrics_dict["12"]["timestamp"]),
                         datetime(2022, 5, 8, 23, 59, tzinfo=timezone.utc))
        self.assertEqual(metrics_dict["12"]["units"], 'kWh')
        self.assertEqual(metrics_dict["12"]["energy"], 0)

    # editing dongles test

    def test_power_consumption_get_hourly(self):
        """Test case for power_consumption_last_get

        Retrieve the last power value of the consumption for one user.
        """
        clean_account()

        clean_influxdb()

        populate_influxdb_energy_imported()  # energyImported dongles
        user_key, user_id, second_user_key, second_user_id = mock_register()

        authorization = superuser_login(id=user_key)

        query_string = [('user_id', user_id),
                        ('group_by', 'hourly'),
                        ('start_date', '2022-06-01T00:00:00+00:00'),
                        ('end_date', '2022-06-02T23:59:00+00:00')]

        headers = {
            'Accept': 'application/json',
            'x_correlation_id': str(uuid.uuid4()),
            'Authorization': authorization,
        }

        response = self.client.open(
            '/api/statistics/power-consumed-real',
            method='GET',
            headers=headers,
            query_string=query_string,
        )

        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

        metrics = json.loads(response.data.decode("utf-8"))

        metrics_dict = {}
        for metric in metrics[0]['real']:
            metrics_dict[str(metric["slot_number"])] = {
                "timestamp": metric["timestamp"], "energy": metric["energy"], "units": metric["units"]}

        self.assertEqual(metrics[0]["user_id"], user_id)

        self.assertEqual(datetime.fromisoformat(metrics_dict["1"]["timestamp"]),
                         datetime(2022, 6, 1, 2, 0, tzinfo=timezone.utc))
        self.assertEqual(metrics_dict["1"]["units"], 'kWh')
        self.assertEqual(metrics_dict["1"]["energy"], 0)

        self.assertEqual(datetime.fromisoformat(metrics_dict["26"]["timestamp"]),
                         datetime(2022, 6, 2, 3, 0, tzinfo=timezone.utc))
        self.assertEqual(metrics_dict["26"]["units"], 'kWh')
        self.assertGreaterEqual(metrics_dict["26"]["energy"], 38.3-30.3)
        self.assertLessEqual(metrics_dict["26"]["energy"], 40.1-26.3)
        # self.assertAlmostEqual(metrics_dict["26"]["energy"], (round(
        #     40.1 - ((33.3+30.3+28.9) / 3), 1) * 10 ) / 10)

        self.assertEqual(datetime.fromisoformat(metrics_dict["35"]["timestamp"]),
                         datetime(2022, 6, 2, 12, 0, tzinfo=timezone.utc))
        self.assertEqual(metrics_dict["35"]["units"], 'kWh')
        self.assertEqual(metrics_dict["35"]["energy"], 0)


    # editing smart_meters test

    def test_power_consumption_smart_meter_get_daily(self):
        """Test case for power_consumption_smart_meter_get

        Retrieve the power consumption for one user. The \"group_by\" variable is used to compute the average value between that interval
        """
        clean_account()

        clean_influxdb()

        populate_influxdb_power_meter_imported()  # meterPowerImported smart_meters

        user_key, user_id, second_user_key, second_user_id = mock_register()

        authorization = superuser_login(id=second_user_key)

        query_string = [('user_id', second_user_id),
                        ('group_by', 'daily'),
                        ('start_date', '2022-04-26T00:00:00+00:00'),
                        ('end_date', '2022-05-08T23:59:00+00:00')]
        headers = {
            'Accept': 'application/json',
            'x_correlation_id': str(uuid.uuid4()),
            'Authorization': authorization,
        }
        response = self.client.open(
            '/api/statistics/power-consumed-real',
            method='GET',
            headers=headers,
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

        metrics = json.loads(response.data.decode("utf-8"))

        metrics_dict = {}
        for metric in metrics[0]['real']:
            metrics_dict[str(metric["slot_number"])] = {
                "timestamp": metric["timestamp"], "energy": metric["energy"], "units": metric["units"]}

        self.assertEqual(metrics[0]["user_id"], second_user_id)

        self.assertEqual(datetime.fromisoformat(metrics_dict["1"]["timestamp"]),
                         datetime(2022, 4, 27, 0, 0, tzinfo=timezone.utc))
        self.assertEqual(metrics_dict["1"]["units"], 'kWh')
        self.assertEqual(metrics_dict["1"]["energy"], 0)

        self.assertEqual(datetime.fromisoformat(metrics_dict["10"]["timestamp"]),
                         datetime(2022, 5, 6, 0, 0, tzinfo=timezone.utc))
        self.assertEqual(metrics_dict["10"]["units"], 'kWh')

        self.assertGreaterEqual(metrics_dict["10"]["energy"], 45.5-43.9)
        self.assertLessEqual(metrics_dict["10"]["energy"], 43.9+45.5)

        self.assertEqual(datetime.fromisoformat(metrics_dict["13"]["timestamp"]),
                         datetime(2022, 5, 8, 23, 59, tzinfo=timezone.utc))
        self.assertEqual(metrics_dict["13"]["units"], 'kWh')
        self.assertEqual(metrics_dict["13"]["energy"], 0)

    # editing smart_meters test
    def test_power_consumption_smart_meter_get_hourly(self):
        """Test case for power_consumption_smart_meter_last_get

        Retrieve the last power value of the consumption for one user.
        """
        clean_account()

        clean_influxdb()

        populate_influxdb_power_meter_imported()  # meterPowerImported smart_meters

        user_key, user_id, second_user_key, second_user_id = mock_register()

        authorization = superuser_login(id=second_user_key)

        query_string = [('user_id', second_user_id),
                        ('group_by', 'hourly'),
                        ('start_date', '2022-06-01T00:00:00+00:00'),
                        ('end_date', '2022-06-02T23:59:00+00:00')]
        headers = {
            'Accept': 'application/json',
            'x_correlation_id': str(uuid.uuid4()),
            'Authorization': authorization,
        }
        response = self.client.open(
            '/api/statistics/power-consumed-real',
            method='GET',
            headers=headers,
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

        metrics = json.loads(response.data.decode("utf-8"))

        metrics_dict = {}
        for metric in metrics[0]['real']:
            metrics_dict[str(metric["slot_number"])] = {
                "timestamp": metric["timestamp"], "energy": metric["energy"], "units": metric["units"]}

        self.assertEqual(metrics[0]["user_id"], second_user_id)

        self.assertEqual(datetime.fromisoformat(metrics_dict["1"]["timestamp"]),
                         datetime(2022, 6, 1, 1, 0, tzinfo=timezone.utc))
        self.assertEqual(metrics_dict["1"]["units"], 'kWh')
        self.assertEqual(metrics_dict["1"]["energy"], 0)

        self.assertEqual(datetime.fromisoformat(metrics_dict["26"]["timestamp"]),
                         datetime(2022, 6, 2, 2, 0, tzinfo=timezone.utc))
        self.assertEqual(metrics_dict["26"]["units"], 'kWh')
        self.assertGreaterEqual(metrics_dict["26"]["energy"], 28.9+30.3+33.3)
        self.assertLessEqual(metrics_dict["26"]["energy"], 28.9+30.3+33.3+40.1)
        
        self.assertEqual(datetime.fromisoformat(metrics_dict["31"]["timestamp"]),
                         datetime(2022, 6, 2, 7, 0, tzinfo=timezone.utc))
        self.assertEqual(metrics_dict["31"]["units"], 'kWh')
        self.assertGreaterEqual(metrics_dict["31"]["energy"], 63.2+62.4+58.9)

        self.assertEqual(datetime.fromisoformat(metrics_dict["38"]["timestamp"]),
                         datetime(2022, 6, 2, 14, 0, tzinfo=timezone.utc))
        self.assertEqual(metrics_dict["38"]["units"], 'kWh')
        self.assertEqual(metrics_dict["38"]["energy"], 0)
        
    def test_power_consumption_all_nulls(self):
        """Test case for power_consumption_get

        Retrieve the power consumption for one user. The \"group_by\" variable is used to compute the average value between that interval
        """
        clean_account()

        clean_influxdb()

        populate_influxdb_energy_imported()

        user_key, user_id, second_user_key, second_user_id = mock_register()

        authorization = superuser_login(id=user_key)

        query_string = [('user_id', user_id),
                        ('group_by', 'daily'),
                        ('start_date', '2022-04-01T00:00:00+00:00'),
                        ('end_date', '2022-05-01T23:59:00+00:00')]

        headers = {
            'Accept': 'application/json',
            'x_correlation_id': str(uuid.uuid4()),
            'Authorization': authorization,
        }
        response = self.client.open(
            '/api/statistics/power-consumed-real',
            method='GET',
            headers=headers,
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

        metrics = json.loads(response.data.decode("utf-8"))

        metrics_dict = {}
        for metric in metrics[0]['real']:
            metrics_dict[str(metric["slot_number"])] = {
                "timestamp": metric["timestamp"], "energy": metric["energy"], "units": metric["units"]}
        
        self.assertEqual(metrics[0]["user_id"], user_id)
        
        self.assertEqual(metrics[0]["real"], [])

    # def test_power_injection_get(self):
    #     """Test case for power_injection_get

    #     Retrieve the power injection for several users. The \"group_by\" variable is used to compute the average value between that interval
    #     """
    #     query_string = [('user_ids', ['[\"userId1\",\"userId2\"]']),
    #                     ('group_by', 'daily'),
    #                     ('start_date', '2013-10-20T19:20:30+01:00'),
    #                     ('end_date', '2013-10-20T19:20:30+01:00')]
    #     headers = {
    #         'Accept': 'application/json',
    #         'x_correlation_id': 'x_correlation_id_example',
    #         'authorization': 'authorization_example',
    #         'Authorization': 'Bearer special-key',
    #     }
    #     response = self.client.open(
    #         '/api/statistics/power-injection',
    #         method='GET',
    #         headers=headers,
    #         query_string=query_string)
    #     self.assert200(response,
    #                    'Response body is : ' + response.data.decode('utf-8'))

    # def test_power_injection_last_get(self):
    #     """Test case for power_injection_last_get

    #     Retrieve the last power value of the injection for several users.
    #     """
    #     query_string = [('user_ids', ['[\"userId1\",\"userId2\"]'])]
    #     headers = {
    #         'Accept': 'application/json',
    #         'x_correlation_id': 'x_correlation_id_example',
    #         'authorization': 'authorization_example',
    #         'Authorization': 'Bearer special-key',
    #     }
    #     response = self.client.open(
    #         '/api/statistics/power-injection-last',
    #         method='GET',
    #         headers=headers,
    #         query_string=query_string)
    #     self.assert200(response,
    #                    'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    unittest.main()
