# coding: utf-8

from __future__ import absolute_import
import unittest

from flask import json
from six import BytesIO

from datetime import datetime, timezone
import uuid
import math

from statistics_manager_service.models.energy_metrics import EnergyMetrics  # noqa: E501
from statistics_manager_service.models.error import Error  # noqa: E501
from statistics_manager_service.models.instant_energy_metric import InstantEnergyMetric  # noqa: E501
from statistics_manager_service.test import BaseTestCase

from statistics_manager_service.test.helper_functions import (
    clean_influxdb,
    populate_influxdb_energy_imported,
    clean_account,
    superuser_login,
    mock_register,
    mock_change_settings,
    METER_ID
)


class TestEnergyQueriesControllerConsumptionHistoric(BaseTestCase):
    """EnergyQueriesController for consumption historic values integration test stubs"""

    def test_energy_consumption_get_daily(self):
        """Test case for energy_consumption_get using group_by daily

        Retrieve the energy consumption for a user grouped by daily
        """
        clean_account()

        clean_influxdb()
        populate_influxdb_energy_imported()

        user_key, user_id, second_user_key, second_user_id = mock_register()

        query_string = {"user_ids": f"{user_id}", "group_by": "daily", "start_date": datetime(
            2022, 5, 2, 0, 0, 0, tzinfo=timezone.utc), "end_date": datetime(2022, 5, 7, 1, 0, 30, tzinfo=timezone.utc)}

        headers = {
            "Accept": "application/json",
            "x_correlation_id": str(uuid.uuid4()),
        }

        response = self.client.open(
            "/api/statistics/energy-consumption",
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
            2022, 5, 2, 0, 0, tzinfo=timezone.utc))
        self.assertEqual(metrics_dict["1"]["units"], "Wh")
        self.assertGreaterEqual(metrics_dict["1"]["value"], 26.3-20.3)
        self.assertLessEqual(metrics_dict["1"]["value"], 28.9-20.3)

        self.assertEqual(datetime.fromisoformat(metrics_dict["2"]["timestamp"]), datetime(
            2022, 5, 3, 0, 0, tzinfo=timezone.utc))
        self.assertEqual(metrics_dict["2"]["units"], "Wh")
        self.assertGreaterEqual(metrics_dict["2"]["value"], 30.3-28.9)
        self.assertLessEqual(metrics_dict["2"]["value"], 33.3-26.3)

        self.assertEqual(datetime.fromisoformat(metrics_dict["3"]["timestamp"]), datetime(
            2022, 5, 4, 0, 0, tzinfo=timezone.utc))
        self.assertEqual(metrics_dict["3"]["units"], "Wh")
        # self.assertGreaterEqual(metrics_dict["3"]["value"], 33.3-30.3)
        self.assertLessEqual(metrics_dict["3"]["value"], 34.1-30.3)

        self.assertEqual(datetime.fromisoformat(metrics_dict["4"]["timestamp"]), datetime(
            2022, 5, 5, 0, 0, tzinfo=timezone.utc))
        self.assertEqual(metrics_dict["4"]["units"], "Wh")
        self.assertGreaterEqual(metrics_dict["4"]["value"], 38.3-34.1)
        self.assertLessEqual(metrics_dict["4"]["value"], 43.9-33.3)

        self.assertEqual(datetime.fromisoformat(metrics_dict["5"]["timestamp"]), datetime(
            2022, 5, 6, 0, 0, tzinfo=timezone.utc))
        self.assertEqual(metrics_dict["5"]["units"], "Wh")
        self.assertGreaterEqual(metrics_dict["5"]["value"], 45.5-43.9)
        self.assertLessEqual(metrics_dict["5"]["value"], 46.3-38.3)

        self.assertEqual(datetime.fromisoformat(metrics_dict["6"]["timestamp"]), datetime(
            2022, 5, 7, 0, 0, tzinfo=timezone.utc))
        self.assertEqual(metrics_dict["6"]["units"], "Wh")
        # self.assertGreaterEqual(metrics_dict["6"]["value"], 46.3-45.5)
        self.assertLessEqual(metrics_dict["6"]["value"], 46.3-45.5)

    def test_energy_consumption_get_hourly(self):
        """Test case for energy_consumption_get using group_by hourly

        Retrieve the energy consumption for a user grouped by hourly
        """
        clean_account()

        clean_influxdb()
        populate_influxdb_energy_imported()

        user_key, user_id, second_user_key, second_user_id = mock_register()

        query_string = {"user_ids": f"{user_id}", "group_by": "hourly",
                        "start_date": datetime(2022, 6, 2, 1, 0, 0, tzinfo=timezone.utc),
                        "end_date": datetime(2022, 6, 2, 7, 0, 0, tzinfo=timezone.utc)}

        headers = {
            "Accept": "application/json",
            "x_correlation_id": str(uuid.uuid4()),
        }

        response = self.client.open(
            "/api/statistics/energy-consumption",
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
            2022, 6, 2, 1, 0, tzinfo=timezone.utc))
        self.assertEqual(metrics_dict["1"]["units"], "Wh")
        self.assertTrue(math.isnan(metrics_dict["1"]["value"]))

        self.assertEqual(datetime.fromisoformat(metrics_dict["2"]["timestamp"]), datetime(
            2022, 6, 2, 2, 0, tzinfo=timezone.utc))
        self.assertEqual(metrics_dict["2"]["units"], "Wh")
        self.assertGreaterEqual(metrics_dict["2"]["value"], 38.3-28.9)
        self.assertLessEqual(metrics_dict["2"]["value"], 40.1-26.3)

        self.assertEqual(datetime.fromisoformat(metrics_dict["3"]["timestamp"]), datetime(
            2022, 6, 2, 3, 0, tzinfo=timezone.utc))
        self.assertEqual(metrics_dict["3"]["units"], "Wh")
        # self.assertGreaterEqual(metrics_dict["3"]["value"], 40.1-38.3)
        self.assertLessEqual(metrics_dict["3"]["value"], 42.1-38.3)

        self.assertEqual(datetime.fromisoformat(metrics_dict["4"]["timestamp"]), datetime(
            2022, 6, 2, 4, 0, tzinfo=timezone.utc))
        self.assertEqual(metrics_dict["4"]["units"], "Wh")
        self.assertGreaterEqual(metrics_dict["4"]["value"], 49.1-42.1)
        self.assertLessEqual(metrics_dict["4"]["value"], 52.1-40.1)

        self.assertEqual(datetime.fromisoformat(metrics_dict["5"]["timestamp"]), datetime(
            2022, 6, 2, 5, 0, tzinfo=timezone.utc))
        self.assertEqual(metrics_dict["5"]["units"], "Wh")
        self.assertGreaterEqual(metrics_dict["5"]["value"], 57.5-52.1)
        self.assertLessEqual(metrics_dict["5"]["value"], 58.9-49.1)

        self.assertEqual(datetime.fromisoformat(metrics_dict["6"]["timestamp"]), datetime(
            2022, 6, 2, 6, 0, tzinfo=timezone.utc))
        self.assertEqual(metrics_dict["6"]["units"], "Wh")
        self.assertGreaterEqual(metrics_dict["6"]["value"], 63.2-58.9)
        self.assertLessEqual(metrics_dict["6"]["value"], 63.2-57.5)

    def test_energy_consumption_get_15min(self):
        """Test case for energy_consumption_get using group_by 15min

        Retrieve the energy consumption for a user grouped by 15min
        """
        clean_account()

        clean_influxdb()
        populate_influxdb_energy_imported()

        user_key, user_id, second_user_key, second_user_id = mock_register()

        query_string = {"user_ids": f"{user_id}", "group_by": "15_mins",
                        "start_date": datetime(2022, 7, 2, 2, 0, 0, tzinfo=timezone.utc),
                        "end_date": datetime(2022, 7, 2, 6, 0, 0, tzinfo=timezone.utc)}

        headers = {
            "Accept": "application/json",
            "x_correlation_id": str(uuid.uuid4()),
        }

        response = self.client.open(
            "/api/statistics/energy-consumption",
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
            2022, 7, 2, 2, 0, tzinfo=timezone.utc))
        self.assertEqual(metrics_dict["1"]["units"], "Wh")
        # self.assertGreaterEqual(metrics_dict["1"]["value"], 33.3-30.3)
        self.assertLessEqual(metrics_dict["1"]["value"], 33.3-30.3)

        self.assertEqual(datetime.fromisoformat(metrics_dict["2"]["timestamp"]), datetime(
            2022, 7, 2, 2, 15, tzinfo=timezone.utc))
        self.assertEqual(metrics_dict["2"]["units"], "Wh")
        # self.assertGreaterEqual(metrics_dict["2"]["value"], 38.3-53.4)
        self.assertLessEqual(metrics_dict["2"]["value"], 38.3-30.3)

        self.assertEqual(datetime.fromisoformat(metrics_dict["3"]["timestamp"]), datetime(
            2022, 7, 2, 2, 30, tzinfo=timezone.utc))
        self.assertEqual(metrics_dict["3"]["units"], "Wh")
        # self.assertGreaterEqual(metrics_dict["3"]["value"], 38.3-53.4)
        self.assertLessEqual(metrics_dict["3"]["value"], 38.3-33.3)

        self.assertEqual(datetime.fromisoformat(metrics_dict["4"]["timestamp"]), datetime(
            2022, 7, 2, 2, 45, tzinfo=timezone.utc))
        self.assertEqual(metrics_dict["4"]["units"], "Wh")
        # self.assertGreaterEqual(metrics_dict["4"]["value"], 38.3-53.4)
        self.assertLessEqual(metrics_dict["4"]["value"], 40.1-33.3)

        self.assertEqual(datetime.fromisoformat(metrics_dict["5"]["timestamp"]), datetime(
            2022, 7, 2, 3, 0, tzinfo=timezone.utc))
        self.assertEqual(metrics_dict["5"]["units"], "Wh")
        self.assertGreaterEqual(metrics_dict["5"]["value"], 42.3-40.1)
        self.assertLessEqual(metrics_dict["5"]["value"], 42.3-38.3)

        self.assertEqual(datetime.fromisoformat(metrics_dict["6"]["timestamp"]), datetime(
            2022, 7, 2, 3, 15, tzinfo=timezone.utc))
        self.assertEqual(metrics_dict["6"]["units"], "Wh")
        self.assertGreaterEqual(metrics_dict["6"]["value"], 45.5-42.3)
        self.assertLessEqual(metrics_dict["6"]["value"], 48.2-42.3)

        self.assertEqual(datetime.fromisoformat(metrics_dict["7"]["timestamp"]), datetime(
            2022, 7, 2, 3, 30, tzinfo=timezone.utc))
        self.assertEqual(metrics_dict["7"]["units"], "Wh")
        # self.assertGreaterEqual(metrics_dict["7"]["value"], 51.7-42.3)
        self.assertLessEqual(metrics_dict["7"]["value"], 51.7-48.2)

        self.assertEqual(datetime.fromisoformat(metrics_dict["8"]["timestamp"]), datetime(
            2022, 7, 2, 3, 45, tzinfo=timezone.utc))
        self.assertEqual(metrics_dict["8"]["units"], "Wh")
        self.assertLessEqual(metrics_dict["8"]["value"], 51.7-48.2)
        self.assertLessEqual(metrics_dict["8"]["value"], 53.4-48.2)

        self.assertEqual(datetime.fromisoformat(metrics_dict["9"]["timestamp"]), datetime(
            2022, 7, 2, 4, 0, tzinfo=timezone.utc))
        self.assertEqual(metrics_dict["9"]["units"], "Wh")
        self.assertGreaterEqual(metrics_dict["9"]["value"], 54.2-53.4)
        self.assertLessEqual(metrics_dict["9"]["value"], 54.2-51.7)

        self.assertEqual(datetime.fromisoformat(metrics_dict["10"]["timestamp"]), datetime(
            2022, 7, 2, 4, 15, tzinfo=timezone.utc))
        self.assertEqual(metrics_dict["10"]["units"], "Wh")
        # self.assertGreaterEqual(metrics_dict["10"]["value"], 58.7-53.4)
        self.assertLessEqual(metrics_dict["10"]["value"], 58.7-53.4)

        self.assertEqual(datetime.fromisoformat(metrics_dict["11"]["timestamp"]), datetime(
            2022, 7, 2, 4, 30, tzinfo=timezone.utc))
        self.assertEqual(metrics_dict["11"]["units"], "Wh")
        # self.assertGreaterEqual(metrics_dict["11"]["value"], 61.4-53.4)
        self.assertLessEqual(metrics_dict["11"]["value"], 61.4-54.2)

        self.assertEqual(datetime.fromisoformat(metrics_dict["12"]["timestamp"]), datetime(
            2022, 7, 2, 4, 45, tzinfo=timezone.utc))
        self.assertEqual(metrics_dict["12"]["units"], "Wh")
        # self.assertGreaterEqual(metrics_dict["12"]["value"], 61.4-53.4)
        self.assertLessEqual(metrics_dict["12"]["value"], 61.4-58.7)

        self.assertEqual(datetime.fromisoformat(metrics_dict["13"]["timestamp"]), datetime(
            2022, 7, 2, 5, 0, tzinfo=timezone.utc))
        self.assertEqual(metrics_dict["13"]["units"], "Wh")
        # self.assertGreaterEqual(metrics_dict["13"]["value"], 54.2-53.4)
        self.assertLessEqual(metrics_dict["13"]["value"], 65.6-61.4)

    def test_energy_consumption_get_monthly(self):
        """Test case for energy_consumption_get using group_by monthly

        Retrieve the energy consumption for a user grouped by monthly
        """
        clean_account()

        clean_influxdb()
        populate_influxdb_energy_imported()

        user_key, user_id, second_user_key, second_user_id = mock_register()

        query_string = {"user_ids": f"{user_id}", "group_by": "monthly",
                        "start_date": datetime(2021, 1, 1, 0, 0, 0, tzinfo=timezone.utc),
                        "end_date": datetime(2021, 9, 1, 0, 0, 0, tzinfo=timezone.utc)}

        headers = {
            "Accept": "application/json",
            "x_correlation_id": str(uuid.uuid4()),
        }

        response = self.client.open(
            "/api/statistics/energy-consumption",
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
        self.assertEqual(metrics_dict["1"]["units"], "Wh")
        self.assertTrue(math.isnan(metrics_dict["1"]["value"]))

        self.assertEqual(datetime.fromisoformat(metrics_dict["2"]["timestamp"]), datetime(
            2021, 2, 1, 0, 0, tzinfo=timezone.utc))
        self.assertEqual(metrics_dict["2"]["units"], "Wh")
        self.assertGreaterEqual(metrics_dict["2"]["value"], 25.3-22.3)
        self.assertLessEqual(metrics_dict["2"]["value"], 26.3-20.3)

        self.assertEqual(datetime.fromisoformat(metrics_dict["3"]["timestamp"]), datetime(
            2021, 3, 1, 0, 0, tzinfo=timezone.utc))
        self.assertEqual(metrics_dict["3"]["units"], "Wh")
        self.assertGreaterEqual(metrics_dict["3"]["value"], 28.9-26.3)
        self.assertLessEqual(metrics_dict["3"]["value"], 30.3-25.3)

        self.assertEqual(datetime.fromisoformat(metrics_dict["4"]["timestamp"]), datetime(
            2021, 4, 1, 0, 0, tzinfo=timezone.utc))
        self.assertEqual(metrics_dict["4"]["units"], "Wh")
        self.assertGreaterEqual(metrics_dict["4"]["value"], 33.3-30.3)
        self.assertLessEqual(metrics_dict["4"]["value"], 34.1-28.9)

        self.assertEqual(datetime.fromisoformat(metrics_dict["5"]["timestamp"]), datetime(
            2021, 5, 1, 0, 0, tzinfo=timezone.utc))
        self.assertEqual(metrics_dict["5"]["units"], "Wh")
        self.assertGreaterEqual(metrics_dict["5"]["value"], 38.3-34.1)
        self.assertLessEqual(metrics_dict["5"]["value"], 43.9-33.3)

        self.assertEqual(datetime.fromisoformat(metrics_dict["6"]["timestamp"]), datetime(
            2021, 6, 1, 0, 0, tzinfo=timezone.utc))
        self.assertEqual(metrics_dict["6"]["units"], "Wh")
        self.assertGreaterEqual(metrics_dict["6"]["value"], 45.3-43.9)
        self.assertLessEqual(metrics_dict["6"]["value"], 46.7-38.3)

        self.assertEqual(datetime.fromisoformat(metrics_dict["7"]["timestamp"]), datetime(
            2021, 7, 1, 0, 0, tzinfo=timezone.utc))
        self.assertEqual(metrics_dict["7"]["units"], "Wh")
        self.assertGreaterEqual(metrics_dict["7"]["value"], 48.2-46.7)
        self.assertLessEqual(metrics_dict["7"]["value"], 53.4-45.3)

        self.assertEqual(datetime.fromisoformat(metrics_dict["8"]["timestamp"]), datetime(
            2021, 8, 1, 0, 0, tzinfo=timezone.utc))
        self.assertEqual(metrics_dict["8"]["units"], "Wh")
        self.assertGreaterEqual(metrics_dict["8"]["value"], 55.7-53.4)
        self.assertLessEqual(metrics_dict["8"]["value"], 55.7-48.2)

        self.assertEqual(datetime.fromisoformat(metrics_dict["9"]["timestamp"]), datetime(
            2021, 9, 1, 0, 0, tzinfo=timezone.utc))
        self.assertEqual(metrics_dict["9"]["units"], "Wh")
        # self.assertGreaterEqual(metrics_dict["9"]["value"], 59.5-58.9)
        self.assertLessEqual(metrics_dict["9"]["value"], 59.5-55.7)

    def test_energy_consumption_get_weekly(self):
        """Test case for energy_consumption_get using group_by weekly

        Retrieve the energy consumption for a user grouped by weekly
        """
        clean_account()

        clean_influxdb()
        populate_influxdb_energy_imported()

        user_key, user_id, second_user_key, second_user_id = mock_register()

        query_string = {"user_ids": f"{user_id}", "group_by": "weekly",
                        "start_date": datetime(2022, 8, 1, 0, 0, 0, tzinfo=timezone.utc),
                        "end_date": datetime(2022, 9, 20, 0, 0, 0, tzinfo=timezone.utc)}

        headers = {
            "Accept": "application/json",
            "x_correlation_id": str(uuid.uuid4()),
        }

        response = self.client.open(
            "/api/statistics/energy-consumption",
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
            2022, 8, 1, 0, 0, tzinfo=timezone.utc))
        self.assertEqual(metrics_dict["1"]["units"], "Wh")
        self.assertTrue(math.isnan(metrics_dict["1"]["value"]))

        self.assertEqual(datetime.fromisoformat(metrics_dict["2"]["timestamp"]), datetime(
            2022, 8, 8, 0, 0, tzinfo=timezone.utc))
        self.assertEqual(metrics_dict["2"]["units"], "Wh")
        self.assertGreaterEqual(metrics_dict["2"]["value"], 49.1-38.3)
        self.assertLessEqual(metrics_dict["2"]["value"], 50.7-33.3)

        self.assertEqual(datetime.fromisoformat(metrics_dict["3"]["timestamp"]), datetime(
            2022, 8, 15, 0, 0, tzinfo=timezone.utc))
        self.assertEqual(metrics_dict["3"]["units"], "Wh")
        self.assertGreaterEqual(metrics_dict["3"]["value"], 66.3-50.7)
        self.assertLessEqual(metrics_dict["3"]["value"], 68.5-49.1)

        self.assertEqual(datetime.fromisoformat(metrics_dict["4"]["timestamp"]), datetime(
            2022, 8, 22, 0, 0, tzinfo=timezone.utc))
        self.assertEqual(metrics_dict["4"]["units"], "Wh")
        self.assertGreaterEqual(metrics_dict["4"]["value"], 68.5-79.7)
        self.assertLessEqual(metrics_dict["4"]["value"], 82.2-66.3)

        self.assertEqual(datetime.fromisoformat(metrics_dict["5"]["timestamp"]), datetime(
            2022, 8, 29, 0, 0, tzinfo=timezone.utc))
        self.assertEqual(metrics_dict["5"]["units"], "Wh")
        self.assertGreaterEqual(metrics_dict["5"]["value"], 93.9-82.2)
        self.assertLessEqual(metrics_dict["5"]["value"], 94.2-79.7)

        self.assertEqual(datetime.fromisoformat(metrics_dict["6"]["timestamp"]), datetime(
            2022, 9, 5, 0, 0, tzinfo=timezone.utc))
        self.assertEqual(metrics_dict["6"]["units"], "Wh")
        self.assertGreaterEqual(metrics_dict["6"]["value"], 103.9-93.6)
        self.assertLessEqual(metrics_dict["6"]["value"], 105.4-92.2)

        self.assertEqual(datetime.fromisoformat(metrics_dict["7"]["timestamp"]), datetime(
            2022, 9, 12, 0, 0, tzinfo=timezone.utc))
        self.assertEqual(metrics_dict["7"]["units"], "Wh")
        self.assertGreaterEqual(metrics_dict["7"]["value"], 109.5-105.4)
        self.assertLessEqual(metrics_dict["7"]["value"], 110.8-103.9)

        self.assertEqual(datetime.fromisoformat(metrics_dict["8"]["timestamp"]), datetime(
            2022, 9, 19, 0, 0, tzinfo=timezone.utc))
        self.assertEqual(metrics_dict["8"]["units"], "Wh")
        # self.assertGreaterEqual(metrics_dict["8"]["value"], 59.5-58.9)
        self.assertLessEqual(metrics_dict["8"]["value"], 110.8-109.5)

    def test_energy_consumption_get_several_users_and_no_api_key(self):
        """Test case for energy_consumption_get using group_by weekly for several users

        Retrieve the energy consumption for several users grouped by weekly
        One of the users does not have an API Key
        """
        clean_account()

        clean_influxdb()
        populate_influxdb_energy_imported()

        user_key, user_id, second_user_key, second_user_id = mock_register()

        query_string = {"user_ids": f"{user_id},{second_user_id}", "group_by": "weekly",
                        "start_date": datetime(2022, 8, 1, 0, 0, 0, tzinfo=timezone.utc),
                        "end_date": datetime(2022, 9, 20, 0, 0, 0, tzinfo=timezone.utc)}

        headers = {
            "Accept": "application/json",
            "x_correlation_id": str(uuid.uuid4()),
        }

        response = self.client.open(
            "/api/statistics/energy-consumption",
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
            2022, 8, 1, 0, 0, tzinfo=timezone.utc))
        self.assertEqual(metrics_dict["1"]["units"], "Wh")
        self.assertTrue(math.isnan(metrics_dict["1"]["value"]))

        self.assertEqual(datetime.fromisoformat(metrics_dict["2"]["timestamp"]), datetime(
            2022, 8, 8, 0, 0, tzinfo=timezone.utc))
        self.assertEqual(metrics_dict["2"]["units"], "Wh")
        self.assertGreaterEqual(metrics_dict["2"]["value"], 49.1-38.3)
        self.assertLessEqual(metrics_dict["2"]["value"], 50.7-33.3)

        self.assertEqual(datetime.fromisoformat(metrics_dict["3"]["timestamp"]), datetime(
            2022, 8, 15, 0, 0, tzinfo=timezone.utc))
        self.assertEqual(metrics_dict["3"]["units"], "Wh")
        self.assertGreaterEqual(metrics_dict["3"]["value"], 66.3-50.7)
        self.assertLessEqual(metrics_dict["3"]["value"], 68.5-49.1)

        self.assertEqual(datetime.fromisoformat(metrics_dict["4"]["timestamp"]), datetime(
            2022, 8, 22, 0, 0, tzinfo=timezone.utc))
        self.assertEqual(metrics_dict["4"]["units"], "Wh")
        self.assertGreaterEqual(metrics_dict["4"]["value"], 68.5-79.7)
        self.assertLessEqual(metrics_dict["4"]["value"], 82.2-66.3)

        self.assertEqual(datetime.fromisoformat(metrics_dict["5"]["timestamp"]), datetime(
            2022, 8, 29, 0, 0, tzinfo=timezone.utc))
        self.assertEqual(metrics_dict["5"]["units"], "Wh")
        self.assertGreaterEqual(metrics_dict["5"]["value"], 93.9-82.2)
        self.assertLessEqual(metrics_dict["5"]["value"], 94.2-79.7)

        self.assertEqual(datetime.fromisoformat(metrics_dict["6"]["timestamp"]), datetime(
            2022, 9, 5, 0, 0, tzinfo=timezone.utc))
        self.assertEqual(metrics_dict["6"]["units"], "Wh")
        self.assertGreaterEqual(metrics_dict["6"]["value"], 103.9-93.6)
        self.assertLessEqual(metrics_dict["6"]["value"], 105.4-92.2)

        self.assertEqual(datetime.fromisoformat(metrics_dict["7"]["timestamp"]), datetime(
            2022, 9, 12, 0, 0, tzinfo=timezone.utc))
        self.assertEqual(metrics_dict["7"]["units"], "Wh")
        self.assertGreaterEqual(metrics_dict["7"]["value"], 109.5-105.4)
        self.assertLessEqual(metrics_dict["7"]["value"], 110.8-103.9)

        self.assertEqual(datetime.fromisoformat(metrics_dict["8"]["timestamp"]), datetime(
            2022, 9, 19, 0, 0, tzinfo=timezone.utc))
        self.assertEqual(metrics_dict["8"]["units"], "Wh")
        # self.assertGreaterEqual(metrics_dict["8"]["value"], 59.5-58.9)
        self.assertLessEqual(metrics_dict["8"]["value"], 110.8-109.5)

    def test_energy_consumption_get_empty(self):
        """Test case for energy_consumption_get using group_by weekly for one user with no data on DB.

        Retrieve the energy consumption for one user grouped by weekly, but with no data on DB.
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
            "/api/statistics/energy-consumption",
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

    def test_energy_consumption_get_wrong_userid(self):
        """Test case for energy_consumption_get using group_by weekly but with a non existing user_id

        Retrieve the energy consumption for a user grouped by weekly but with a non existing user_id
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
            "/api/statistics/energy-consumption",
            method="GET",
            headers=headers,
            query_string=query_string,
        )
        self.assert404(response, "Response body is : " +
                       response.data.decode("utf-8"))

    def test_energy_consumption_get_several_users_with_authentication(self):
        """Test case for energy_consumption_get using group_by weekly for several users with authentication
        Meaning that the user will not have access to the other user_id

        Retrieve the energy consumption for several users grouped by weekly with authentication
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
            "/api/statistics/energy-consumption",
            method="GET",
            headers=headers,
            query_string=query_string,
        )
        self.assert403(response, "Response body is : " +
                       response.data.decode("utf-8"))
    
    def test_energy_consumption_get_weekly_without_end_date(self):
        """Test case for energy_consumption_get using group_by weekly without end_date parameter

        Retrieve the energy consumption for a user grouped by weekly without end_date parameter
        """
        clean_account()

        clean_influxdb()
        populate_influxdb_energy_imported()

        user_key, user_id, second_user_key, second_user_id = mock_register()

        query_string = {"user_ids": f"{user_id}", "group_by": "weekly",
                        "start_date": datetime(2022, 8, 1, 0, 0, 0, tzinfo=timezone.utc)}

        headers = {
            "Accept": "application/json",
            "x_correlation_id": str(uuid.uuid4()),
        }

        response = self.client.open(
            "/api/statistics/energy-consumption",
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
            2022, 8, 1, 0, 0, tzinfo=timezone.utc))
        self.assertEqual(metrics_dict["1"]["units"], "Wh")
        self.assertTrue(math.isnan(metrics_dict["1"]["value"]))

        self.assertEqual(datetime.fromisoformat(metrics_dict["2"]["timestamp"]), datetime(
            2022, 8, 8, 0, 0, tzinfo=timezone.utc))
        self.assertEqual(metrics_dict["2"]["units"], "Wh")
        self.assertGreaterEqual(metrics_dict["2"]["value"], 49.1-38.3)
        self.assertLessEqual(metrics_dict["2"]["value"], 50.7-33.3)

        self.assertEqual(datetime.fromisoformat(metrics_dict["3"]["timestamp"]), datetime(
            2022, 8, 15, 0, 0, tzinfo=timezone.utc))
        self.assertEqual(metrics_dict["3"]["units"], "Wh")
        self.assertGreaterEqual(metrics_dict["3"]["value"], 66.3-50.7)
        self.assertLessEqual(metrics_dict["3"]["value"], 68.5-49.1)

        self.assertEqual(datetime.fromisoformat(metrics_dict["4"]["timestamp"]), datetime(
            2022, 8, 22, 0, 0, tzinfo=timezone.utc))
        self.assertEqual(metrics_dict["4"]["units"], "Wh")
        self.assertGreaterEqual(metrics_dict["4"]["value"], 68.5-79.7)
        self.assertLessEqual(metrics_dict["4"]["value"], 82.2-66.3)

        self.assertEqual(datetime.fromisoformat(metrics_dict["5"]["timestamp"]), datetime(
            2022, 8, 29, 0, 0, tzinfo=timezone.utc))
        self.assertEqual(metrics_dict["5"]["units"], "Wh")
        self.assertGreaterEqual(metrics_dict["5"]["value"], 93.9-82.2)
        self.assertLessEqual(metrics_dict["5"]["value"], 94.2-79.7)

        self.assertEqual(datetime.fromisoformat(metrics_dict["6"]["timestamp"]), datetime(
            2022, 9, 5, 0, 0, tzinfo=timezone.utc))
        self.assertEqual(metrics_dict["6"]["units"], "Wh")
        self.assertGreaterEqual(metrics_dict["6"]["value"], 103.9-93.6)
        self.assertLessEqual(metrics_dict["6"]["value"], 105.4-92.2)

        self.assertEqual(datetime.fromisoformat(metrics_dict["7"]["timestamp"]), datetime(
            2022, 9, 12, 0, 0, tzinfo=timezone.utc))
        self.assertEqual(metrics_dict["7"]["units"], "Wh")
        self.assertGreaterEqual(metrics_dict["7"]["value"], 109.5-105.4)
        self.assertLessEqual(metrics_dict["7"]["value"], 110.8-103.9)

        self.assertEqual(datetime.fromisoformat(metrics_dict["8"]["timestamp"]), datetime(
            2022, 9, 19, 0, 0, tzinfo=timezone.utc))
        self.assertEqual(metrics_dict["8"]["units"], "Wh")
        # self.assertGreaterEqual(metrics_dict["8"]["value"], 59.5-58.9)
        self.assertLessEqual(metrics_dict["8"]["value"], 110.8-109.5)


if __name__ == '__main__':
    unittest.main()
