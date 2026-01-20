# coding: utf-8

from __future__ import absolute_import
import unittest

from flask import json
from six import BytesIO

from datetime import datetime, timezone
import uuid
import math

from statistics_manager_service.models.error import Error  # noqa: E501
from statistics_manager_service.models.instant_power_metric import InstantPowerMetric  # noqa: E501
from statistics_manager_service.models.power_metrics import PowerMetrics  # noqa: E501
from statistics_manager_service.test import BaseTestCase

from statistics_manager_service.test.helper_functions import (
    clean_influxdb,
    populate_influxdb_power_imported,
    clean_account,
    superuser_login,
    mock_register,
    mock_change_settings,
)


class TestPowerQueriesControllerConsumptionHistoric(BaseTestCase):
    """PowerQueriesController for consumption historic values integration test stubs"""

    def test_power_consumption_get_daily(self):
        """Test case for power_consumption_get using group_by daily

        Retrieve the power consumption for a user grouped by daily
        """
        clean_account()

        clean_influxdb()
        populate_influxdb_power_imported()

        user_key, user_id, second_user_key, second_user_id = mock_register()

        query_string = {"user_ids": f"{user_id}", "group_by": "daily", "start_date": datetime(
            2022, 5, 1, 0, 0, 0, tzinfo=timezone.utc), "end_date": datetime(2022, 5, 11, 1, 0, 30, tzinfo=timezone.utc)}

        headers = {
            "Accept": "application/json",
            "x_correlation_id": str(uuid.uuid4()),
        }

        response = self.client.open(
            "/api/statistics/power-consumption",
            method="GET",
            headers=headers,
            query_string=query_string,
        )
        self.assert200(response, "Response body is : " +
                       response.data.decode("utf-8"))

        metrics = json.loads(response.data.decode("utf-8"))

        metrics_dict = {}

        for metric in metrics[0]["metrics"]:
            metrics_dict[str(metric["slot_number"])] = {
                "timestamp": metric["timestamp"], "value": metric["value"], "units": metric["units"]}

        self.assertEqual(metrics[0]["user_id"], user_id)

        self.assertEqual(datetime.fromisoformat(metrics_dict["1"]["timestamp"]), datetime(
            2022, 5, 1, 0, 0, tzinfo=timezone.utc))
        self.assertEqual(metrics_dict["1"]["units"], "W")
        self.assertAlmostEqual(metrics_dict["1"]["value"], round((164.6 + 2687.5 + 2060.0) / 3, 2), delta=0.01)

        self.assertEqual(datetime.fromisoformat(metrics_dict["2"]["timestamp"]), datetime(
            2022, 5, 2, 0, 0, tzinfo=timezone.utc))
        self.assertEqual(metrics_dict["2"]["units"], "W")
        self.assertAlmostEqual(metrics_dict["2"]["value"], round((827.8 + 1150.0 + 2120.0) / 3, 2), delta=0.01)

        self.assertEqual(datetime.fromisoformat(metrics_dict["3"]["timestamp"]), datetime(
            2022, 5, 3, 0, 0, tzinfo=timezone.utc))
        self.assertEqual(metrics_dict["3"]["units"], "W")
        self.assertAlmostEqual(metrics_dict["3"]["value"], round((1615.1 + 712.2 + 1006.9 + 1633.1) / 4, 2), delta=0.01)

        self.assertEqual(datetime.fromisoformat(metrics_dict["4"]["timestamp"]), datetime(
            2022, 5, 4, 0, 0, tzinfo=timezone.utc))
        self.assertEqual(metrics_dict["4"]["units"], "W")
        self.assertAlmostEqual(metrics_dict["4"]["value"], round((290.2 + 488.4 + 400.3 + 1541.9 + 1835.3) / 5, 2), delta=0.01)

        self.assertEqual(datetime.fromisoformat(metrics_dict["5"]["timestamp"]), datetime(
            2022, 5, 5, 0, 0, tzinfo=timezone.utc))
        self.assertEqual(metrics_dict["5"]["units"], "W")
        self.assertAlmostEqual(metrics_dict["5"]["value"], round((814.5 + 2789.0 + 84.7 + 717.5 + 3395.8) / 5, 2), delta=0.01)

        self.assertEqual(datetime.fromisoformat(metrics_dict["6"]["timestamp"]), datetime(
            2022, 5, 6, 0, 0, tzinfo=timezone.utc))
        self.assertEqual(metrics_dict["6"]["units"], "W")
        self.assertAlmostEqual(metrics_dict["6"]["value"], round((1910.0 + 1409.1 + 768.9) / 3, 2), delta=0.01)

        self.assertEqual(datetime.fromisoformat(metrics_dict["7"]["timestamp"]), datetime(
            2022, 5, 7, 0, 0, tzinfo=timezone.utc))
        self.assertEqual(metrics_dict["7"]["units"], "W")
        self.assertAlmostEqual(metrics_dict["7"]["value"], round((2016.3 + 1851.4 + 2999.7 + 2360.7 + 504.5) / 5, 2), delta=0.01)

        self.assertEqual(datetime.fromisoformat(metrics_dict["8"]["timestamp"]), datetime(
            2022, 5, 8, 0, 0, tzinfo=timezone.utc))
        self.assertEqual(metrics_dict["8"]["units"], "W")
        self.assertAlmostEqual(metrics_dict["8"]["value"], round((3350.9 + 512.2 + 422.1) / 3, 2), delta=0.01)

        self.assertEqual(datetime.fromisoformat(metrics_dict["9"]["timestamp"]), datetime(
            2022, 5, 9, 0, 0, tzinfo=timezone.utc))
        self.assertEqual(metrics_dict["9"]["units"], "W")
        self.assertAlmostEqual(metrics_dict["9"]["value"], round((2111.4 + 890.3 + 881.8 + 248.4 + 2580.6) / 5, 2), delta=0.01)

        self.assertEqual(datetime.fromisoformat(metrics_dict["10"]["timestamp"]), datetime(
            2022, 5, 10, 0, 0, tzinfo=timezone.utc))
        self.assertEqual(metrics_dict["10"]["units"], "W")
        self.assertAlmostEqual(metrics_dict["10"]["value"], round((471.4 + 3323.3 + 2925.0 + 84.4) / 4, 2), delta=0.01)

        self.assertEqual(datetime.fromisoformat(metrics_dict["11"]["timestamp"]), datetime(
            2022, 5, 11, 0, 0, tzinfo=timezone.utc))
        self.assertEqual(metrics_dict["11"]["units"], "W")
        self.assertTrue(math.isnan(metrics_dict["11"]["value"]))

    def test_power_consumption_get_hourly(self):
        """Test case for power_consumption_get using group_by hourly

        Retrieve the power consumption for a user grouped by hourly
        """
        clean_account()

        clean_influxdb()
        populate_influxdb_power_imported()

        user_key, user_id, second_user_key, second_user_id = mock_register()

        query_string = {"user_ids": f"{user_id}", "group_by": "hourly",
                        "start_date": datetime(2022, 6, 1, 1, 0, 0, tzinfo=timezone.utc),
                        "end_date": datetime(2022, 6, 1, 19, 59, 0, tzinfo=timezone.utc)}

        headers = {
            "Accept": "application/json",
            "x_correlation_id": str(uuid.uuid4()),
        }

        response = self.client.open(
            "/api/statistics/power-consumption",
            method="GET",
            headers=headers,
            query_string=query_string,
        )
        self.assert200(response, "Response body is : " +
                       response.data.decode("utf-8"))

        metrics = json.loads(response.data.decode("utf-8"))

        metrics_dict = {}

        for metric in metrics[0]["metrics"]:
            metrics_dict[str(metric["slot_number"])] = {
                "timestamp": metric["timestamp"], "value": metric["value"], "units": metric["units"]}

        self.assertEqual(metrics[0]["user_id"], user_id)

        self.assertEqual(datetime.fromisoformat(metrics_dict["1"]["timestamp"]), datetime(
            2022, 6, 1, 1, 0, tzinfo=timezone.utc))
        self.assertEqual(metrics_dict["1"]["units"], "W")
        self.assertAlmostEqual(metrics_dict["1"]["value"], round((1489.6 + 829.5) / 2, 2), delta=0.01)

        self.assertEqual(datetime.fromisoformat(metrics_dict["2"]["timestamp"]), datetime(
            2022, 6, 1, 2, 0, tzinfo=timezone.utc))
        self.assertEqual(metrics_dict["2"]["units"], "W")
        self.assertAlmostEqual(metrics_dict["2"]["value"], round((3285.8 + 2941.2) / 2, 2), delta=0.01)

        self.assertEqual(datetime.fromisoformat(metrics_dict["3"]["timestamp"]), datetime(
            2022, 6, 1, 3, 0, tzinfo=timezone.utc))
        self.assertEqual(metrics_dict["3"]["units"], "W")
        self.assertAlmostEqual(metrics_dict["3"]["value"], round(423.5, 2), delta=0.01)

        self.assertEqual(datetime.fromisoformat(metrics_dict["4"]["timestamp"]), datetime(
            2022, 6, 1, 4, 0, tzinfo=timezone.utc))
        self.assertEqual(metrics_dict["4"]["units"], "W")
        self.assertAlmostEqual(metrics_dict["4"]["value"], round((2632.8 + 3290.2) / 2, 2), delta=0.01)

        self.assertEqual(datetime.fromisoformat(metrics_dict["5"]["timestamp"]), datetime(
            2022, 6, 1, 5, 0, tzinfo=timezone.utc))
        self.assertEqual(metrics_dict["5"]["units"], "W")
        self.assertAlmostEqual(metrics_dict["5"]["value"], round((1984.4 + 2502.4 + 1008.9) / 3, 2), delta=0.01)

        self.assertEqual(datetime.fromisoformat(metrics_dict["6"]["timestamp"]), datetime(
            2022, 6, 1, 6, 0, tzinfo=timezone.utc))
        self.assertEqual(metrics_dict["6"]["units"], "W")
        self.assertAlmostEqual(metrics_dict["6"]["value"], round((2070.1 + 3015.3 + 165.3) / 3, 2), delta=0.01)

        self.assertEqual(datetime.fromisoformat(metrics_dict["7"]["timestamp"]), datetime(
            2022, 6, 1, 7, 0, tzinfo=timezone.utc))
        self.assertEqual(metrics_dict["7"]["units"], "W")
        self.assertAlmostEqual(metrics_dict["7"]["value"], round((1375.1 + 2633.1 + 1792.8) / 3, 2), delta=0.01)

        self.assertEqual(datetime.fromisoformat(metrics_dict["8"]["timestamp"]), datetime(
            2022, 6, 1, 8, 0, tzinfo=timezone.utc))
        self.assertEqual(metrics_dict["8"]["units"], "W")
        self.assertAlmostEqual(metrics_dict["8"]["value"], round(3317.3, 2), delta=0.01)

        self.assertEqual(datetime.fromisoformat(metrics_dict["9"]["timestamp"]), datetime(
            2022, 6, 1, 9, 0, tzinfo=timezone.utc))
        self.assertEqual(metrics_dict["9"]["units"], "W")
        self.assertAlmostEqual(metrics_dict["9"]["value"], round((3447.5 + 1046.9) / 2, 2), delta=0.01)

        self.assertEqual(datetime.fromisoformat(metrics_dict["10"]["timestamp"]), datetime(
            2022, 6, 1, 10, 0, tzinfo=timezone.utc))
        self.assertEqual(metrics_dict["10"]["units"], "W")
        self.assertAlmostEqual(metrics_dict["10"]["value"], round((1887.8 + 2708.9 + 2895.2) / 3, 2), delta=0.01)

        self.assertEqual(datetime.fromisoformat(metrics_dict["11"]["timestamp"]), datetime(
            2022, 6, 1, 11, 0, tzinfo=timezone.utc))
        self.assertEqual(metrics_dict["11"]["units"], "W")
        self.assertAlmostEqual(metrics_dict["11"]["value"], round((1963.6 + 3378.1 + 2939.6) / 3, 2), delta=0.01)

        self.assertEqual(datetime.fromisoformat(metrics_dict["12"]["timestamp"]), datetime(
            2022, 6, 1, 12, 0, tzinfo=timezone.utc))
        self.assertEqual(metrics_dict["12"]["units"], "W")
        self.assertAlmostEqual(metrics_dict["12"]["value"], round((3021.9 + 1295.1) / 2, 2), delta=0.01)

        self.assertEqual(datetime.fromisoformat(metrics_dict["13"]["timestamp"]), datetime(
            2022, 6, 1, 13, 0, tzinfo=timezone.utc))
        self.assertEqual(metrics_dict["13"]["units"], "W")
        self.assertAlmostEqual(metrics_dict["13"]["value"], round((1565.2 + 1793.2) / 2, 2), delta=0.01)

        self.assertEqual(datetime.fromisoformat(metrics_dict["14"]["timestamp"]), datetime(
            2022, 6, 1, 14, 0, tzinfo=timezone.utc))
        self.assertEqual(metrics_dict["14"]["units"], "W")
        self.assertAlmostEqual(metrics_dict["14"]["value"], round(2069.6, 2), delta=0.01)

        self.assertEqual(datetime.fromisoformat(metrics_dict["15"]["timestamp"]), datetime(
            2022, 6, 1, 15, 0, tzinfo=timezone.utc))
        self.assertEqual(metrics_dict["15"]["units"], "W")
        self.assertAlmostEqual(metrics_dict["15"]["value"], round((655.2 + 1521.8) / 2, 2), delta=0.01)

        self.assertEqual(datetime.fromisoformat(metrics_dict["16"]["timestamp"]), datetime(
            2022, 6, 1, 16, 0, tzinfo=timezone.utc))
        self.assertEqual(metrics_dict["16"]["units"], "W")
        self.assertAlmostEqual(metrics_dict["16"]["value"], round(1069.6, 2), delta=0.01)

        self.assertEqual(datetime.fromisoformat(metrics_dict["17"]["timestamp"]), datetime(
            2022, 6, 1, 17, 0, tzinfo=timezone.utc))
        self.assertEqual(metrics_dict["17"]["units"], "W")
        self.assertAlmostEqual(metrics_dict["17"]["value"], round(189.1, 2), delta=0.01)

        self.assertEqual(datetime.fromisoformat(metrics_dict["18"]["timestamp"]), datetime(
            2022, 6, 1, 18, 0, tzinfo=timezone.utc))
        self.assertEqual(metrics_dict["18"]["units"], "W")
        self.assertAlmostEqual(metrics_dict["18"]["value"], round((3094.9 + 1278.0 + 2182.7 + 657.5) / 4, 2), delta=0.01)

        self.assertEqual(datetime.fromisoformat(metrics_dict["19"]["timestamp"]), datetime(
            2022, 6, 1, 19, 0, tzinfo=timezone.utc))
        self.assertEqual(metrics_dict["19"]["units"], "W")
        self.assertAlmostEqual(metrics_dict["19"]["value"], round((2632.2 + 1401.2) / 2, 2), delta=0.01)

    def test_power_consumption_get_15min(self):
        """Test case for power_consumption_get using group_by 15min

        Retrieve the power consumption for a user grouped by 15min
        """
        clean_account()

        clean_influxdb()
        populate_influxdb_power_imported()

        user_key, user_id, second_user_key, second_user_id = mock_register()

        query_string = {"user_ids": f"{user_id}", "group_by": "15_mins",
                        "start_date": datetime(2022, 7, 1, 1, 0, 0, tzinfo=timezone.utc),
                        "end_date": datetime(2022, 7, 1, 5, 38, 0, tzinfo=timezone.utc)}

        headers = {
            "Accept": "application/json",
            "x_correlation_id": str(uuid.uuid4()),
        }

        response = self.client.open(
            "/api/statistics/power-consumption",
            method="GET",
            headers=headers,
            query_string=query_string,
        )
        self.assert200(response, "Response body is : " +
                       response.data.decode("utf-8"))

        metrics = json.loads(response.data.decode("utf-8"))

        metrics_dict = {}

        for metric in metrics[0]["metrics"]:
            metrics_dict[str(metric["slot_number"])] = {
                "timestamp": metric["timestamp"], "value": metric["value"], "units": metric["units"]}

        self.assertEqual(metrics[0]["user_id"], user_id)

        self.assertEqual(datetime.fromisoformat(metrics_dict["1"]["timestamp"]), datetime(
            2022, 7, 1, 1, 0, tzinfo=timezone.utc))
        self.assertEqual(metrics_dict["1"]["units"], "W")
        self.assertAlmostEqual(metrics_dict["1"]["value"], round((2730.3 + 2292.7 + 248.8) / 3, 2), delta=0.01)

        self.assertEqual(datetime.fromisoformat(metrics_dict["2"]["timestamp"]), datetime(
            2022, 7, 1, 1, 15, tzinfo=timezone.utc))
        self.assertEqual(metrics_dict["2"]["units"], "W")
        self.assertAlmostEqual(metrics_dict["2"]["value"], round((549.4 + 2124.0) / 2, 2), delta=0.01)

        self.assertEqual(datetime.fromisoformat(metrics_dict["3"]["timestamp"]), datetime(
            2022, 7, 1, 1, 30, tzinfo=timezone.utc))
        self.assertEqual(metrics_dict["3"]["units"], "W")
        self.assertAlmostEqual(metrics_dict["3"]["value"], round((1110.5 + 2161.7) / 2, 2), delta=0.01)

        self.assertEqual(datetime.fromisoformat(metrics_dict["4"]["timestamp"]), datetime(
            2022, 7, 1, 1, 45, tzinfo=timezone.utc))
        self.assertEqual(metrics_dict["4"]["units"], "W")
        self.assertAlmostEqual(metrics_dict["4"]["value"], round(714.7, 2), delta=0.01)

        self.assertEqual(datetime.fromisoformat(metrics_dict["5"]["timestamp"]), datetime(
            2022, 7, 1, 2, 0, tzinfo=timezone.utc))
        self.assertEqual(metrics_dict["5"]["units"], "W")
        self.assertAlmostEqual(metrics_dict["5"]["value"], round((2877.1 + 1202.5 + 3116.8) / 3, 2), delta=0.01)

        self.assertEqual(datetime.fromisoformat(metrics_dict["6"]["timestamp"]), datetime(
            2022, 7, 1, 2, 15, tzinfo=timezone.utc))
        self.assertEqual(metrics_dict["6"]["units"], "W")
        self.assertAlmostEqual(metrics_dict["6"]["value"], round((293.6 + 2485.2 + 3115.8) / 3, 2), delta=0.01)

        self.assertEqual(datetime.fromisoformat(metrics_dict["7"]["timestamp"]), datetime(
            2022, 7, 1, 2, 30, tzinfo=timezone.utc))
        self.assertEqual(metrics_dict["7"]["units"], "W")
        self.assertAlmostEqual(metrics_dict["7"]["value"], round((1658.6 + 2119.7) / 2, 2), delta=0.01)

        self.assertEqual(datetime.fromisoformat(metrics_dict["8"]["timestamp"]), datetime(
            2022, 7, 1, 2, 45, tzinfo=timezone.utc))
        self.assertEqual(metrics_dict["8"]["units"], "W")
        self.assertAlmostEqual(metrics_dict["8"]["value"], round(1742.1, 2), delta=0.01)

        self.assertEqual(datetime.fromisoformat(metrics_dict["9"]["timestamp"]), datetime(
            2022, 7, 1, 3, 0, tzinfo=timezone.utc))
        self.assertEqual(metrics_dict["9"]["units"], "W")
        self.assertAlmostEqual(metrics_dict["9"]["value"], round((2380.8 + 2137.7 + 1611.8) / 3, 2), delta=0.01)

        self.assertEqual(datetime.fromisoformat(metrics_dict["10"]["timestamp"]), datetime(
            2022, 7, 1, 3, 15, tzinfo=timezone.utc))
        self.assertEqual(metrics_dict["10"]["units"], "W")
        self.assertAlmostEqual(metrics_dict["10"]["value"], round((3127.4 + 1911.4 + 2743.1) / 3, 2), delta=0.01)

        self.assertEqual(datetime.fromisoformat(metrics_dict["11"]["timestamp"]), datetime(
            2022, 7, 1, 3, 30, tzinfo=timezone.utc))
        self.assertEqual(metrics_dict["11"]["units"], "W")
        self.assertAlmostEqual(metrics_dict["11"]["value"], round((1160.3 + 2924.9) / 2, 2), delta=0.01)

        self.assertEqual(datetime.fromisoformat(metrics_dict["12"]["timestamp"]), datetime(
            2022, 7, 1, 3, 45, tzinfo=timezone.utc))
        self.assertEqual(metrics_dict["12"]["units"], "W")
        self.assertAlmostEqual(metrics_dict["12"]["value"], round((1384.4 + 1744.5 + 3479.8) / 3, 2), delta=0.01)

        self.assertEqual(datetime.fromisoformat(metrics_dict["13"]["timestamp"]), datetime(
            2022, 7, 1, 4, 0, tzinfo=timezone.utc))
        self.assertEqual(metrics_dict["13"]["units"], "W")
        self.assertAlmostEqual(metrics_dict["13"]["value"], round((846.6 + 2240.7) / 2, 2), delta=0.01)

        self.assertEqual(datetime.fromisoformat(metrics_dict["14"]["timestamp"]), datetime(
            2022, 7, 1, 4, 15, tzinfo=timezone.utc))
        self.assertEqual(metrics_dict["14"]["units"], "W")
        self.assertAlmostEqual(metrics_dict["14"]["value"], round((2532.1 + 3015.2 + 1435.8 + 3079.5) / 4, 2), delta=0.01)

        self.assertEqual(datetime.fromisoformat(metrics_dict["15"]["timestamp"]), datetime(
            2022, 7, 1, 4, 30, tzinfo=timezone.utc))
        self.assertEqual(metrics_dict["15"]["units"], "W")
        self.assertAlmostEqual(metrics_dict["15"]["value"], round((459.5 + 1343.1) / 2, 2), delta=0.01)

        self.assertEqual(datetime.fromisoformat(metrics_dict["16"]["timestamp"]), datetime(
            2022, 7, 1, 4, 45, tzinfo=timezone.utc))
        self.assertEqual(metrics_dict["16"]["units"], "W")
        self.assertAlmostEqual(metrics_dict["16"]["value"], round((2138.4 + 212.9) / 2, 2), delta=0.01)

        self.assertEqual(datetime.fromisoformat(metrics_dict["17"]["timestamp"]), datetime(
            2022, 7, 1, 5, 0, tzinfo=timezone.utc))
        self.assertEqual(metrics_dict["17"]["units"], "W")
        self.assertAlmostEqual(metrics_dict["17"]["value"], round((340.6 + 200.4) / 2, 2), delta=0.01)

        self.assertEqual(datetime.fromisoformat(metrics_dict["18"]["timestamp"]), datetime(
            2022, 7, 1, 5, 15, tzinfo=timezone.utc))
        self.assertEqual(metrics_dict["18"]["units"], "W")
        self.assertTrue(math.isnan(metrics_dict["18"]["value"]))

        self.assertEqual(datetime.fromisoformat(metrics_dict["19"]["timestamp"]), datetime(
            2022, 7, 1, 5, 30, tzinfo=timezone.utc))
        self.assertEqual(metrics_dict["19"]["units"], "W")
        self.assertTrue(math.isnan(metrics_dict["19"]["value"]))

    def test_power_consumption_get_monthly(self):
        """Test case for power_consumption_get using group_by monthly

        Retrieve the power consumption for a user grouped by monthly
        """
        clean_account()

        clean_influxdb()
        populate_influxdb_power_imported()

        user_key, user_id, second_user_key, second_user_id = mock_register()

        query_string = {"user_ids": f"{user_id}", "group_by": "monthly",
                        "start_date": datetime(2021, 1, 1, 0, 0, 0, tzinfo=timezone.utc),
                        "end_date": datetime(2021, 12, 31, 23, 59, 59, tzinfo=timezone.utc)}

        headers = {
            "Accept": "application/json",
            "x_correlation_id": str(uuid.uuid4()),
        }

        response = self.client.open(
            "/api/statistics/power-consumption",
            method="GET",
            headers=headers,
            query_string=query_string,
        )
        self.assert200(response, "Response body is : " +
                       response.data.decode("utf-8"))

        metrics = json.loads(response.data.decode("utf-8"))

        metrics_dict = {}

        for metric in metrics[0]["metrics"]:
            metrics_dict[str(metric["slot_number"])] = {
                "timestamp": metric["timestamp"], "value": metric["value"], "units": metric["units"]}

        self.assertEqual(metrics[0]["user_id"], user_id)

        self.assertEqual(datetime.fromisoformat(metrics_dict["1"]["timestamp"]), datetime(
            2021, 1, 1, 0, 0, tzinfo=timezone.utc))
        self.assertEqual(metrics_dict["1"]["units"], "W")
        self.assertAlmostEqual(metrics_dict["1"]["value"], round((2274.2 + 2002.1 + 471.7 + 1979.6) / 4, 2), delta=0.01)

        self.assertEqual(datetime.fromisoformat(metrics_dict["2"]["timestamp"]), datetime(
            2021, 2, 1, 0, 0, tzinfo=timezone.utc))
        self.assertEqual(metrics_dict["2"]["units"], "W")
        self.assertAlmostEqual(metrics_dict["2"]["value"], round((3326.4 + 2570.8 + 2168.8 + 159.9) / 4, 2), delta=0.01)

        self.assertEqual(datetime.fromisoformat(metrics_dict["3"]["timestamp"]), datetime(
            2021, 3, 1, 0, 0, tzinfo=timezone.utc))
        self.assertEqual(metrics_dict["3"]["units"], "W")
        self.assertAlmostEqual(metrics_dict["3"]["value"], round((2643.2 + 1290.0 + 3361.7) / 3, 2), delta=0.01)

        self.assertEqual(datetime.fromisoformat(metrics_dict["4"]["timestamp"]), datetime(
            2021, 4, 1, 0, 0, tzinfo=timezone.utc))
        self.assertEqual(metrics_dict["4"]["units"], "W")
        self.assertAlmostEqual(metrics_dict["4"]["value"], round((2454.5 + 3134.5 + 3137.0 + 1217.1) / 4, 2), delta=0.01)

        self.assertEqual(datetime.fromisoformat(metrics_dict["5"]["timestamp"]), datetime(
            2021, 5, 1, 0, 0, tzinfo=timezone.utc))
        self.assertEqual(metrics_dict["5"]["units"], "W")
        self.assertAlmostEqual(metrics_dict["5"]["value"], round((2238.7 + 1736.9 + 1855.1) / 3, 2), delta=0.01)

        self.assertEqual(datetime.fromisoformat(metrics_dict["6"]["timestamp"]), datetime(
            2021, 6, 1, 0, 0, tzinfo=timezone.utc))
        self.assertEqual(metrics_dict["6"]["units"], "W")
        self.assertAlmostEqual(metrics_dict["6"]["value"], round((409.6 + 111.2 + 3273.7) / 3, 2), delta=0.01)

        self.assertEqual(datetime.fromisoformat(metrics_dict["7"]["timestamp"]), datetime(
            2021, 7, 1, 0, 0, tzinfo=timezone.utc))
        self.assertEqual(metrics_dict["7"]["units"], "W")
        self.assertAlmostEqual(metrics_dict["7"]["value"], round((1258.8 + 568.6 + 1244.5) / 3, 2), delta=0.01)

        self.assertEqual(datetime.fromisoformat(metrics_dict["8"]["timestamp"]), datetime(
            2021, 8, 1, 0, 0, tzinfo=timezone.utc))
        self.assertEqual(metrics_dict["8"]["units"], "W")
        self.assertAlmostEqual(metrics_dict["8"]["value"], round((623.6 + 168.4 + 418.3 + 1254.6) / 4, 2), delta=0.01)

        self.assertEqual(datetime.fromisoformat(metrics_dict["9"]["timestamp"]), datetime(
            2021, 9, 1, 0, 0, tzinfo=timezone.utc))
        self.assertEqual(metrics_dict["9"]["units"], "W")
        self.assertAlmostEqual(metrics_dict["9"]["value"], round((729.5 + 2895.0 + 1964.4) / 3, 2), delta=0.01)

        self.assertEqual(datetime.fromisoformat(metrics_dict["10"]["timestamp"]), datetime(
            2021, 10, 1, 0, 0, tzinfo=timezone.utc))
        self.assertEqual(metrics_dict["10"]["units"], "W")
        self.assertAlmostEqual(metrics_dict["10"]["value"], round((2086.6 + 3485.0 + 2868.9) / 3, 2), delta=0.01)

        self.assertEqual(datetime.fromisoformat(metrics_dict["11"]["timestamp"]), datetime(
            2021, 11, 1, 0, 0, tzinfo=timezone.utc))
        self.assertEqual(metrics_dict["11"]["units"], "W")
        self.assertAlmostEqual(metrics_dict["11"]["value"], round((2172.0 + 3450.1 + 217.3 + 1106.3) / 4, 2), delta=0.01)

        self.assertEqual(datetime.fromisoformat(metrics_dict["12"]["timestamp"]), datetime(
            2021, 12, 1, 0, 0, tzinfo=timezone.utc))
        self.assertEqual(metrics_dict["12"]["units"], "W")
        self.assertAlmostEqual(metrics_dict["12"]["value"], round((243.7 + 1726.7) / 2, 2), delta=0.01)

    def test_power_consumption_get_weekly(self):
        """Test case for power_consumption_get using group_by weekly

        Retrieve the power consumption for a user grouped by weekly
        """
        clean_account()

        clean_influxdb()
        populate_influxdb_power_imported()

        user_key, user_id, second_user_key, second_user_id = mock_register()

        query_string = {"user_ids": f"{user_id}", "group_by": "weekly",
                        "start_date": datetime(2022, 8, 6, 0, 0, 0, tzinfo=timezone.utc),
                        "end_date": datetime(2022, 12, 24, 0, 0, 0, tzinfo=timezone.utc)}

        headers = {
            "Accept": "application/json",
            "x_correlation_id": str(uuid.uuid4()),
        }

        response = self.client.open(
            "/api/statistics/power-consumption",
            method="GET",
            headers=headers,
            query_string=query_string,
        )
        self.assert200(response, "Response body is : " +
                       response.data.decode("utf-8"))

        metrics = json.loads(response.data.decode("utf-8"))

        metrics_dict = {}

        for metric in metrics[0]["metrics"]:
            metrics_dict[str(metric["slot_number"])] = {
                "timestamp": metric["timestamp"], "value": metric["value"], "units": metric["units"]}

        self.assertEqual(metrics[0]["user_id"], user_id)

        self.assertEqual(datetime.fromisoformat(metrics_dict["1"]["timestamp"]), datetime(
            2022, 8, 6, 0, 0, tzinfo=timezone.utc))
        self.assertEqual(metrics_dict["1"]["units"], "W")
        self.assertAlmostEqual(metrics_dict["1"]["value"], round((2779.4 + 809.3) / 2, 2), delta=0.01)

        self.assertEqual(datetime.fromisoformat(metrics_dict["2"]["timestamp"]), datetime(
            2022, 8, 13, 0, 0, tzinfo=timezone.utc))
        self.assertEqual(metrics_dict["2"]["units"], "W")
        self.assertAlmostEqual(metrics_dict["2"]["value"], round((3094.6 + 742.7) / 2, 2), delta=0.01)

        self.assertEqual(datetime.fromisoformat(metrics_dict["3"]["timestamp"]), datetime(
            2022, 8, 20, 0, 0, tzinfo=timezone.utc))
        self.assertEqual(metrics_dict["3"]["units"], "W")
        self.assertAlmostEqual(metrics_dict["3"]["value"], round((1203.7 + 3341.3) / 2, 2), delta=0.01)

        self.assertEqual(datetime.fromisoformat(metrics_dict["4"]["timestamp"]), datetime(
            2022, 8, 27, 0, 0, tzinfo=timezone.utc))
        self.assertEqual(metrics_dict["4"]["units"], "W")
        self.assertAlmostEqual(metrics_dict["4"]["value"], round((520.2 + 2793.2) / 2, 2), delta=0.01)

        self.assertEqual(datetime.fromisoformat(metrics_dict["5"]["timestamp"]), datetime(
            2022, 9, 3, 0, 0, tzinfo=timezone.utc))
        self.assertEqual(metrics_dict["5"]["units"], "W")
        self.assertAlmostEqual(metrics_dict["5"]["value"], round((2209.1 + 183.0) / 2, 2), delta=0.01)

        self.assertEqual(datetime.fromisoformat(metrics_dict["6"]["timestamp"]), datetime(
            2022, 9, 10, 0, 0, tzinfo=timezone.utc))
        self.assertEqual(metrics_dict["6"]["units"], "W")
        self.assertAlmostEqual(metrics_dict["6"]["value"], round((3421.0 + 422.4) / 2, 2), delta=0.01)

        self.assertEqual(datetime.fromisoformat(metrics_dict["7"]["timestamp"]), datetime(
            2022, 9, 17, 0, 0, tzinfo=timezone.utc))
        self.assertEqual(metrics_dict["7"]["units"], "W")
        self.assertAlmostEqual(metrics_dict["7"]["value"], round((1255.3 + 2059.8) / 2, 2), delta=0.01)

        self.assertEqual(datetime.fromisoformat(metrics_dict["8"]["timestamp"]), datetime(
            2022, 9, 24, 0, 0, tzinfo=timezone.utc))
        self.assertEqual(metrics_dict["8"]["units"], "W")
        self.assertAlmostEqual(metrics_dict["8"]["value"], round((2099.6 + 435.0) / 2, 2), delta=0.01)

        self.assertEqual(datetime.fromisoformat(metrics_dict["9"]["timestamp"]), datetime(
            2022, 10, 1, 0, 0, tzinfo=timezone.utc))
        self.assertEqual(metrics_dict["9"]["units"], "W")
        self.assertAlmostEqual(metrics_dict["9"]["value"], round((1278.1 + 2671.4) / 2, 2), delta=0.01)

        self.assertEqual(datetime.fromisoformat(metrics_dict["10"]["timestamp"]), datetime(
            2022, 10, 8, 0, 0, tzinfo=timezone.utc))
        self.assertEqual(metrics_dict["10"]["units"], "W")
        self.assertAlmostEqual(metrics_dict["10"]["value"], round((3402.2 + 1922.4) / 2, 2), delta=0.01)

        self.assertEqual(datetime.fromisoformat(metrics_dict["11"]["timestamp"]), datetime(
            2022, 10, 15, 0, 0, tzinfo=timezone.utc))
        self.assertEqual(metrics_dict["11"]["units"], "W")
        self.assertAlmostEqual(metrics_dict["11"]["value"], round((3336.8 + 2333.1) / 2, 2), delta=0.01)

        self.assertEqual(datetime.fromisoformat(metrics_dict["12"]["timestamp"]), datetime(
            2022, 10, 22, 0, 0, tzinfo=timezone.utc))
        self.assertEqual(metrics_dict["12"]["units"], "W")
        self.assertAlmostEqual(metrics_dict["12"]["value"], round((3405.0 + 1921.9) / 2, 2), delta=0.01)

        self.assertEqual(datetime.fromisoformat(metrics_dict["13"]["timestamp"]), datetime(
            2022, 10, 29, 0, 0, tzinfo=timezone.utc))
        self.assertEqual(metrics_dict["13"]["units"], "W")
        self.assertAlmostEqual(metrics_dict["13"]["value"], round((1232.4 + 905.1 + 218.1) / 3, 2), delta=0.01)

        self.assertEqual(datetime.fromisoformat(metrics_dict["14"]["timestamp"]), datetime(
            2022, 11, 5, 0, 0, tzinfo=timezone.utc))
        self.assertEqual(metrics_dict["14"]["units"], "W")
        self.assertAlmostEqual(metrics_dict["14"]["value"], round((1144.3 + 633.0) / 2, 2), delta=0.01)

        self.assertEqual(datetime.fromisoformat(metrics_dict["15"]["timestamp"]), datetime(
            2022, 11, 12, 0, 0, tzinfo=timezone.utc))
        self.assertEqual(metrics_dict["15"]["units"], "W")
        self.assertAlmostEqual(metrics_dict["15"]["value"], round((2478.2 + 2043.5) / 2, 2), delta=0.01)

        self.assertEqual(datetime.fromisoformat(metrics_dict["16"]["timestamp"]), datetime(
            2022, 11, 19, 0, 0, tzinfo=timezone.utc))
        self.assertEqual(metrics_dict["16"]["units"], "W")
        self.assertAlmostEqual(metrics_dict["16"]["value"], round(3337.8, 2), delta=0.01)

        self.assertEqual(datetime.fromisoformat(metrics_dict["17"]["timestamp"]), datetime(
            2022, 11, 26, 0, 0, tzinfo=timezone.utc))
        self.assertEqual(metrics_dict["17"]["units"], "W")
        self.assertAlmostEqual(metrics_dict["17"]["value"], round((1521.7 + 2611.8) / 2, 2), delta=0.01)

        self.assertEqual(datetime.fromisoformat(metrics_dict["18"]["timestamp"]), datetime(
            2022, 12, 3, 0, 0, tzinfo=timezone.utc))
        self.assertEqual(metrics_dict["18"]["units"], "W")
        self.assertAlmostEqual(metrics_dict["18"]["value"], round((338.3 + 1988.3) / 2, 2), delta=0.01)

        self.assertEqual(datetime.fromisoformat(metrics_dict["19"]["timestamp"]), datetime(
            2022, 12, 10, 0, 0, tzinfo=timezone.utc))
        self.assertEqual(metrics_dict["19"]["units"], "W")
        self.assertAlmostEqual(metrics_dict["19"]["value"], round(3247.6, 2), delta=0.01)

        self.assertEqual(datetime.fromisoformat(metrics_dict["20"]["timestamp"]), datetime(
            2022, 12, 17, 0, 0, tzinfo=timezone.utc))
        self.assertEqual(metrics_dict["20"]["units"], "W")
        self.assertAlmostEqual(metrics_dict["20"]["value"], round((3274.1 + 2094.7 + 879.4) / 3, 2), delta=0.01)

        self.assertEqual(datetime.fromisoformat(metrics_dict["21"]["timestamp"]), datetime(
            2022, 12, 24, 0, 0, tzinfo=timezone.utc))
        self.assertEqual(metrics_dict["21"]["units"], "W")
        self.assertTrue(math.isnan(metrics_dict["21"]["value"]))

    def test_power_consumption_get_several_users_and_no_api_key(self):
        """Test case for power_consumption_get using group_by weekly for several users

        Retrieve the power consumption for several users grouped by weekly
        One of the users does not have an API Key
        """
        clean_account()

        clean_influxdb()
        populate_influxdb_power_imported()

        user_key, user_id, second_user_key, second_user_id = mock_register()

        query_string = {"user_ids": f"{user_id},{second_user_id}", "group_by": "weekly",
                        "start_date": datetime(2022, 8, 6, 0, 0, 0, tzinfo=timezone.utc),
                        "end_date": datetime(2022, 12, 24, 0, 0, 0, tzinfo=timezone.utc)}

        headers = {
            "Accept": "application/json",
            "x_correlation_id": str(uuid.uuid4()),
        }

        response = self.client.open(
            "/api/statistics/power-consumption",
            method="GET",
            headers=headers,
            query_string=query_string,
        )
        self.assert200(response, "Response body is : " +
                       response.data.decode("utf-8"))

        metrics = json.loads(response.data.decode("utf-8"))

        metrics_dict = {}

        if metrics[0]["user_id"] == user_id:
            for metric in metrics[0]["metrics"]:
                metrics_dict[str(metric["slot_number"])] = {
                    "timestamp": metric["timestamp"], "value": metric["value"], "units": metric["units"]}

            self.assertEqual(metrics[0]["user_id"], user_id)
            self.assertEqual(metrics[1]["user_id"], second_user_id)
            self.assertEqual(len(metrics[1]["metrics"]), 0)
        else:
            for metric in metrics[1]["metrics"]:
                metrics_dict[str(metric["slot_number"])] = {
                    "timestamp": metric["timestamp"], "value": metric["value"], "units": metric["units"]}

            self.assertEqual(metrics[1]["user_id"], user_id)
            self.assertEqual(metrics[0]["user_id"], second_user_id)
            self.assertEqual(len(metrics[0]["metrics"]), 0)

        self.assertEqual(datetime.fromisoformat(metrics_dict["1"]["timestamp"]), datetime(
            2022, 8, 6, 0, 0, tzinfo=timezone.utc))
        self.assertEqual(metrics_dict["1"]["units"], "W")
        self.assertAlmostEqual(metrics_dict["1"]["value"], round((2779.4 + 809.3) / 2, 2), delta=0.01)

        self.assertEqual(datetime.fromisoformat(metrics_dict["2"]["timestamp"]), datetime(
            2022, 8, 13, 0, 0, tzinfo=timezone.utc))
        self.assertEqual(metrics_dict["2"]["units"], "W")
        self.assertAlmostEqual(metrics_dict["2"]["value"], round((3094.6 + 742.7) / 2, 2), delta=0.01)

        self.assertEqual(datetime.fromisoformat(metrics_dict["3"]["timestamp"]), datetime(
            2022, 8, 20, 0, 0, tzinfo=timezone.utc))
        self.assertEqual(metrics_dict["3"]["units"], "W")
        self.assertAlmostEqual(metrics_dict["3"]["value"], round((1203.7 + 3341.3) / 2, 2), delta=0.01)

        self.assertEqual(datetime.fromisoformat(metrics_dict["4"]["timestamp"]), datetime(
            2022, 8, 27, 0, 0, tzinfo=timezone.utc))
        self.assertEqual(metrics_dict["4"]["units"], "W")
        self.assertAlmostEqual(metrics_dict["4"]["value"], round((520.2 + 2793.2) / 2, 2), delta=0.01)

        self.assertEqual(datetime.fromisoformat(metrics_dict["5"]["timestamp"]), datetime(
            2022, 9, 3, 0, 0, tzinfo=timezone.utc))
        self.assertEqual(metrics_dict["5"]["units"], "W")
        self.assertAlmostEqual(metrics_dict["5"]["value"], round((2209.1 + 183.0) / 2, 2), delta=0.01)

        self.assertEqual(datetime.fromisoformat(metrics_dict["6"]["timestamp"]), datetime(
            2022, 9, 10, 0, 0, tzinfo=timezone.utc))
        self.assertEqual(metrics_dict["6"]["units"], "W")
        self.assertAlmostEqual(metrics_dict["6"]["value"], round((3421.0 + 422.4) / 2, 2), delta=0.01)

        self.assertEqual(datetime.fromisoformat(metrics_dict["7"]["timestamp"]), datetime(
            2022, 9, 17, 0, 0, tzinfo=timezone.utc))
        self.assertEqual(metrics_dict["7"]["units"], "W")
        self.assertAlmostEqual(metrics_dict["7"]["value"], round((1255.3 + 2059.8) / 2, 2), delta=0.01)

        self.assertEqual(datetime.fromisoformat(metrics_dict["8"]["timestamp"]), datetime(
            2022, 9, 24, 0, 0, tzinfo=timezone.utc))
        self.assertEqual(metrics_dict["8"]["units"], "W")
        self.assertAlmostEqual(metrics_dict["8"]["value"], round((2099.6 + 435.0) / 2, 2), delta=0.01)

        self.assertEqual(datetime.fromisoformat(metrics_dict["9"]["timestamp"]), datetime(
            2022, 10, 1, 0, 0, tzinfo=timezone.utc))
        self.assertEqual(metrics_dict["9"]["units"], "W")
        self.assertAlmostEqual(metrics_dict["9"]["value"], round((1278.1 + 2671.4) / 2, 2), delta=0.01)

        self.assertEqual(datetime.fromisoformat(metrics_dict["10"]["timestamp"]), datetime(
            2022, 10, 8, 0, 0, tzinfo=timezone.utc))
        self.assertEqual(metrics_dict["10"]["units"], "W")
        self.assertAlmostEqual(metrics_dict["10"]["value"], round((3402.2 + 1922.4) / 2, 2), delta=0.01)

        self.assertEqual(datetime.fromisoformat(metrics_dict["11"]["timestamp"]), datetime(
            2022, 10, 15, 0, 0, tzinfo=timezone.utc))
        self.assertEqual(metrics_dict["11"]["units"], "W")
        self.assertAlmostEqual(metrics_dict["11"]["value"], round((3336.8 + 2333.1) / 2, 2), delta=0.01)

        self.assertEqual(datetime.fromisoformat(metrics_dict["12"]["timestamp"]), datetime(
            2022, 10, 22, 0, 0, tzinfo=timezone.utc))
        self.assertEqual(metrics_dict["12"]["units"], "W")
        self.assertAlmostEqual(metrics_dict["12"]["value"], round((3405.0 + 1921.9) / 2, 2), delta=0.01)

        self.assertEqual(datetime.fromisoformat(metrics_dict["13"]["timestamp"]), datetime(
            2022, 10, 29, 0, 0, tzinfo=timezone.utc))
        self.assertEqual(metrics_dict["13"]["units"], "W")
        self.assertAlmostEqual(metrics_dict["13"]["value"], round((1232.4 + 905.1 + 218.1) / 3, 2), delta=0.01)

        self.assertEqual(datetime.fromisoformat(metrics_dict["14"]["timestamp"]), datetime(
            2022, 11, 5, 0, 0, tzinfo=timezone.utc))
        self.assertEqual(metrics_dict["14"]["units"], "W")
        self.assertAlmostEqual(metrics_dict["14"]["value"], round((1144.3 + 633.0) / 2, 2), delta=0.01)

        self.assertEqual(datetime.fromisoformat(metrics_dict["15"]["timestamp"]), datetime(
            2022, 11, 12, 0, 0, tzinfo=timezone.utc))
        self.assertEqual(metrics_dict["15"]["units"], "W")
        self.assertAlmostEqual(metrics_dict["15"]["value"], round((2478.2 + 2043.5) / 2, 2), delta=0.01)

        self.assertEqual(datetime.fromisoformat(metrics_dict["16"]["timestamp"]), datetime(
            2022, 11, 19, 0, 0, tzinfo=timezone.utc))
        self.assertEqual(metrics_dict["16"]["units"], "W")
        self.assertAlmostEqual(metrics_dict["16"]["value"], round(3337.8, 2), delta=0.01)

        self.assertEqual(datetime.fromisoformat(metrics_dict["17"]["timestamp"]), datetime(
            2022, 11, 26, 0, 0, tzinfo=timezone.utc))
        self.assertEqual(metrics_dict["17"]["units"], "W")
        self.assertAlmostEqual(metrics_dict["17"]["value"], round((1521.7 + 2611.8) / 2, 2), delta=0.01)

        self.assertEqual(datetime.fromisoformat(metrics_dict["18"]["timestamp"]), datetime(
            2022, 12, 3, 0, 0, tzinfo=timezone.utc))
        self.assertEqual(metrics_dict["18"]["units"], "W")
        self.assertAlmostEqual(metrics_dict["18"]["value"], round((338.3 + 1988.3) / 2, 2), delta=0.01)

        self.assertEqual(datetime.fromisoformat(metrics_dict["19"]["timestamp"]), datetime(
            2022, 12, 10, 0, 0, tzinfo=timezone.utc))
        self.assertEqual(metrics_dict["19"]["units"], "W")
        self.assertAlmostEqual(metrics_dict["19"]["value"], round(3247.6, 2), delta=0.01)

        self.assertEqual(datetime.fromisoformat(metrics_dict["20"]["timestamp"]), datetime(
            2022, 12, 17, 0, 0, tzinfo=timezone.utc))
        self.assertEqual(metrics_dict["20"]["units"], "W")
        self.assertAlmostEqual(metrics_dict["20"]["value"], round((3274.1 + 2094.7 + 879.4) / 3, 2), delta=0.01)

        self.assertEqual(datetime.fromisoformat(metrics_dict["21"]["timestamp"]), datetime(
            2022, 12, 24, 0, 0, tzinfo=timezone.utc))
        self.assertEqual(metrics_dict["21"]["units"], "W")
        self.assertTrue(math.isnan(metrics_dict["21"]["value"]))

    def test_power_consumption_get_empty(self):
        """Test case for power_consumption_get using group_by weekly for one user with no data on DB.

        Retrieve the power consumption for one user grouped by weekly, but with no data on DB.
        """
        clean_account()

        clean_influxdb()

        user_key, user_id, second_user_key, second_user_id = mock_register()

        query_string = {"user_ids": f"{user_id}", "group_by": "weekly",
                        "start_date": datetime(2022, 8, 1, 0, 0, 0, tzinfo=timezone.utc),
                        "end_date": datetime(2022, 9, 20, 0, 0, 0, tzinfo=timezone.utc)}

        headers = {
            "Accept": "application/json",
            "x_correlation_id": str(uuid.uuid4()),
        }

        response = self.client.open(
            "/api/statistics/power-consumption",
            method="GET",
            headers=headers,
            query_string=query_string,
        )
        self.assert200(response, "Response body is : " +
                       response.data.decode("utf-8"))

        metrics = json.loads(response.data.decode("utf-8"))

        metrics_dict = metrics[0]

        self.assertEqual(metrics_dict["user_id"], user_id)
        self.assertEqual(len(metrics_dict["metrics"]), 0)

    def test_power_consumption_get_wrong_userid(self):
        """Test case for power_consumption_get using group_by weekly but with a non existing user_id

        Retrieve the power consumption for a user grouped by weekly but with a non existing user_id
        """
        clean_account()

        query_string = {"user_ids": f"1234567890", "group_by": "weekly",
                        "start_date": datetime(2022, 8, 1, 0, 0, 0, tzinfo=timezone.utc),
                        "end_date": datetime(2022, 9, 20, 0, 0, 0, tzinfo=timezone.utc)}

        headers = {
            "Accept": "application/json",
            "x_correlation_id": str(uuid.uuid4()),
        }

        response = self.client.open(
            "/api/statistics/power-consumption",
            method="GET",
            headers=headers,
            query_string=query_string,
        )
        self.assert404(response, "Response body is : " +
                       response.data.decode("utf-8"))

    def test_power_consumption_get_several_users_with_authentication(self):
        """Test case for power_consumption_get using group_by weekly for several users with authentication
        Meaning that the user will not have access to the other user_id

        Retrieve the power consumption for several users grouped by weekly with authentication
        The user does not have access to the second user_id
        """
        clean_account()

        user_key, user_id, second_user_key, second_user_id = mock_register()

        authorization = superuser_login(id=user_key)

        query_string = {"user_ids": f"{user_id},{second_user_id}", "group_by": "weekly",
                        "start_date": datetime(2022, 8, 1, 0, 0, 0, tzinfo=timezone.utc),
                        "end_date": datetime(2022, 9, 20, 0, 0, 0, tzinfo=timezone.utc)}

        headers = {
            "Accept": "application/json",
            "x_correlation_id": str(uuid.uuid4()),
            "Authorization": authorization,
        }

        response = self.client.open(
            "/api/statistics/power-consumption",
            method="GET",
            headers=headers,
            query_string=query_string,
        )
        self.assert403(response, "Response body is : " +
                       response.data.decode("utf-8"))

    def test_power_consumption_get_weekly_without_end_date(self):
        """Test case for power_consumption_get using group_by weekly without end_date parameter

        Retrieve the power consumption for a user grouped by weekly without end_date parameter
        """
        clean_account()

        clean_influxdb()
        populate_influxdb_power_imported()

        user_key, user_id, second_user_key, second_user_id = mock_register()

        query_string = {"user_ids": f"{user_id}", "group_by": "weekly",
                        "start_date": datetime(2022, 8, 6, 0, 0, 0, tzinfo=timezone.utc)}

        headers = {
            "Accept": "application/json",
            "x_correlation_id": str(uuid.uuid4()),
        }

        response = self.client.open(
            "/api/statistics/power-consumption",
            method="GET",
            headers=headers,
            query_string=query_string,
        )
        self.assert200(response, "Response body is : " +
                       response.data.decode("utf-8"))

        metrics = json.loads(response.data.decode("utf-8"))

        metrics_dict = {}

        for metric in metrics[0]["metrics"]:
            metrics_dict[str(metric["slot_number"])] = {
                "timestamp": metric["timestamp"], "value": metric["value"], "units": metric["units"]}

        self.assertEqual(metrics[0]["user_id"], user_id)

        self.assertEqual(datetime.fromisoformat(metrics_dict["1"]["timestamp"]), datetime(
            2022, 8, 6, 0, 0, tzinfo=timezone.utc))
        self.assertEqual(metrics_dict["1"]["units"], "W")
        self.assertAlmostEqual(metrics_dict["1"]["value"], round((2779.4 + 809.3) / 2, 2), delta=0.01)

        self.assertEqual(datetime.fromisoformat(metrics_dict["2"]["timestamp"]), datetime(
            2022, 8, 13, 0, 0, tzinfo=timezone.utc))
        self.assertEqual(metrics_dict["2"]["units"], "W")
        self.assertAlmostEqual(metrics_dict["2"]["value"], round((3094.6 + 742.7) / 2, 2), delta=0.01)

        self.assertEqual(datetime.fromisoformat(metrics_dict["3"]["timestamp"]), datetime(
            2022, 8, 20, 0, 0, tzinfo=timezone.utc))
        self.assertEqual(metrics_dict["3"]["units"], "W")
        self.assertAlmostEqual(metrics_dict["3"]["value"], round((1203.7 + 3341.3) / 2, 2), delta=0.01)

        self.assertEqual(datetime.fromisoformat(metrics_dict["4"]["timestamp"]), datetime(
            2022, 8, 27, 0, 0, tzinfo=timezone.utc))
        self.assertEqual(metrics_dict["4"]["units"], "W")
        self.assertAlmostEqual(metrics_dict["4"]["value"], round((520.2 + 2793.2) / 2, 2), delta=0.01)

        self.assertEqual(datetime.fromisoformat(metrics_dict["5"]["timestamp"]), datetime(
            2022, 9, 3, 0, 0, tzinfo=timezone.utc))
        self.assertEqual(metrics_dict["5"]["units"], "W")
        self.assertAlmostEqual(metrics_dict["5"]["value"], round((2209.1 + 183.0) / 2, 2), delta=0.01)

        self.assertEqual(datetime.fromisoformat(metrics_dict["6"]["timestamp"]), datetime(
            2022, 9, 10, 0, 0, tzinfo=timezone.utc))
        self.assertEqual(metrics_dict["6"]["units"], "W")
        self.assertAlmostEqual(metrics_dict["6"]["value"], round((3421.0 + 422.4) / 2, 2), delta=0.01)

        self.assertEqual(datetime.fromisoformat(metrics_dict["7"]["timestamp"]), datetime(
            2022, 9, 17, 0, 0, tzinfo=timezone.utc))
        self.assertEqual(metrics_dict["7"]["units"], "W")
        self.assertAlmostEqual(metrics_dict["7"]["value"], round((1255.3 + 2059.8) / 2, 2), delta=0.01)

        self.assertEqual(datetime.fromisoformat(metrics_dict["8"]["timestamp"]), datetime(
            2022, 9, 24, 0, 0, tzinfo=timezone.utc))
        self.assertEqual(metrics_dict["8"]["units"], "W")
        self.assertAlmostEqual(metrics_dict["8"]["value"], round((2099.6 + 435.0) / 2, 2), delta=0.01)

        self.assertEqual(datetime.fromisoformat(metrics_dict["9"]["timestamp"]), datetime(
            2022, 10, 1, 0, 0, tzinfo=timezone.utc))
        self.assertEqual(metrics_dict["9"]["units"], "W")
        self.assertAlmostEqual(metrics_dict["9"]["value"], round((1278.1 + 2671.4) / 2, 2), delta=0.01)

        self.assertEqual(datetime.fromisoformat(metrics_dict["10"]["timestamp"]), datetime(
            2022, 10, 8, 0, 0, tzinfo=timezone.utc))
        self.assertEqual(metrics_dict["10"]["units"], "W")
        self.assertAlmostEqual(metrics_dict["10"]["value"], round((3402.2 + 1922.4) / 2, 2), delta=0.01)

        self.assertEqual(datetime.fromisoformat(metrics_dict["11"]["timestamp"]), datetime(
            2022, 10, 15, 0, 0, tzinfo=timezone.utc))
        self.assertEqual(metrics_dict["11"]["units"], "W")
        self.assertAlmostEqual(metrics_dict["11"]["value"], round((3336.8 + 2333.1) / 2, 2), delta=0.01)

        self.assertEqual(datetime.fromisoformat(metrics_dict["12"]["timestamp"]), datetime(
            2022, 10, 22, 0, 0, tzinfo=timezone.utc))
        self.assertEqual(metrics_dict["12"]["units"], "W")
        self.assertAlmostEqual(metrics_dict["12"]["value"], round((3405.0 + 1921.9) / 2, 2), delta=0.01)

        self.assertEqual(datetime.fromisoformat(metrics_dict["13"]["timestamp"]), datetime(
            2022, 10, 29, 0, 0, tzinfo=timezone.utc))
        self.assertEqual(metrics_dict["13"]["units"], "W")
        self.assertAlmostEqual(metrics_dict["13"]["value"], round((1232.4 + 905.1 + 218.1) / 3, 2), delta=0.01)

        self.assertEqual(datetime.fromisoformat(metrics_dict["14"]["timestamp"]), datetime(
            2022, 11, 5, 0, 0, tzinfo=timezone.utc))
        self.assertEqual(metrics_dict["14"]["units"], "W")
        self.assertAlmostEqual(metrics_dict["14"]["value"], round((1144.3 + 633.0) / 2, 2), delta=0.01)

        self.assertEqual(datetime.fromisoformat(metrics_dict["15"]["timestamp"]), datetime(
            2022, 11, 12, 0, 0, tzinfo=timezone.utc))
        self.assertEqual(metrics_dict["15"]["units"], "W")
        self.assertAlmostEqual(metrics_dict["15"]["value"], round((2478.2 + 2043.5) / 2, 2), delta=0.01)

        self.assertEqual(datetime.fromisoformat(metrics_dict["16"]["timestamp"]), datetime(
            2022, 11, 19, 0, 0, tzinfo=timezone.utc))
        self.assertEqual(metrics_dict["16"]["units"], "W")
        self.assertAlmostEqual(metrics_dict["16"]["value"], round(3337.8, 2), delta=0.01)

        self.assertEqual(datetime.fromisoformat(metrics_dict["17"]["timestamp"]), datetime(
            2022, 11, 26, 0, 0, tzinfo=timezone.utc))
        self.assertEqual(metrics_dict["17"]["units"], "W")
        self.assertAlmostEqual(metrics_dict["17"]["value"], round((1521.7 + 2611.8) / 2, 2), delta=0.01)

        self.assertEqual(datetime.fromisoformat(metrics_dict["18"]["timestamp"]), datetime(
            2022, 12, 3, 0, 0, tzinfo=timezone.utc))
        self.assertEqual(metrics_dict["18"]["units"], "W")
        self.assertAlmostEqual(metrics_dict["18"]["value"], round((338.3 + 1988.3) / 2, 2), delta=0.01)

        self.assertEqual(datetime.fromisoformat(metrics_dict["19"]["timestamp"]), datetime(
            2022, 12, 10, 0, 0, tzinfo=timezone.utc))
        self.assertEqual(metrics_dict["19"]["units"], "W")
        self.assertAlmostEqual(metrics_dict["19"]["value"], round(3247.6, 2), delta=0.01)

        self.assertEqual(datetime.fromisoformat(metrics_dict["20"]["timestamp"]), datetime(
            2022, 12, 17, 0, 0, tzinfo=timezone.utc))
        self.assertEqual(metrics_dict["20"]["units"], "W")
        self.assertAlmostEqual(metrics_dict["20"]["value"], round((3274.1 + 2094.7 + 879.4) / 3, 2), delta=0.01)

        self.assertEqual(datetime.fromisoformat(metrics_dict["21"]["timestamp"]), datetime(
            2022, 12, 24, 0, 0, tzinfo=timezone.utc))
        self.assertEqual(metrics_dict["21"]["units"], "W")
        self.assertTrue(math.isnan(metrics_dict["21"]["value"]))


if __name__ == '__main__':
    unittest.main()
