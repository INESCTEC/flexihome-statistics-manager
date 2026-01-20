# coding: utf-8

from __future__ import absolute_import
import unittest

from flask import json

from jsonschema import validate

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

from statistics_manager_service.test.schemas import InstantPowerMetricSchema


class TestPowerQueriesControllerConsumptionLast(BaseTestCase):
    """PowerQueriesController for consumption last values integration test stubs"""

    def test_power_consumption_last_get(self):
        """Test case for power_consumption_last_get

        Retrieve the last value of the power consumption for one user.
        """
        clean_account()

        clean_influxdb()
        populate_influxdb_power_imported()

        user_key, user_id, second_user_key, second_user_id = mock_register(register_api_key=True)

        query_string = {"user_ids": f"{user_id}"}

        headers = {
            "Accept": "application/json",
            "x_correlation_id": str(uuid.uuid4()),
        }

        response = self.client.open(
            "/api/statistics/power-consumption-last",
            method="GET",
            headers=headers,
            query_string=query_string,
        )
        self.assert200(response, "Response body is : " +
                       response.data.decode("utf-8"))

        metrics = json.loads(response.data.decode("utf-8"))
        print(metrics)

        metrics_dict = metrics[0]
        validate(metrics_dict, InstantPowerMetricSchema)

        self.assertEqual(metrics_dict["user_id"], user_id)
        self.assertEqual(datetime.fromisoformat(metrics_dict["timestamp"]), datetime(
            2022, 12, 23, 13, 0, 51, tzinfo=timezone.utc))
        self.assertEqual(metrics_dict["units"], "W")
        self.assertEqual(metrics_dict["value"], 879.4)

    def test_power_consumption_last_get_several_users_and_no_api_key(self):
        """Test case for power_consumption_last_get for several users

        Retrieve the last value of the power consumption for several users.
        One of the users does not have an API Key
        """
        clean_account()

        clean_influxdb()
        populate_influxdb_power_imported()

        user_key, user_id, second_user_key, second_user_id = mock_register()

        query_string = {"user_ids": f"{user_id},{second_user_id}"}

        headers = {
            "Accept": "application/json",
            "x_correlation_id": str(uuid.uuid4()),
        }

        response = self.client.open(
            "/api/statistics/power-consumption-last",
            method="GET",
            headers=headers,
            query_string=query_string,
        )
        self.assert200(response, "Response body is : " +
                       response.data.decode("utf-8"))

        metrics = json.loads(response.data.decode("utf-8"))

        metrics_dict = {}

        if metrics[0]["user_id"] == user_id:
            good_user_id_index = 0
            bad_user_id_index = 1
        else:
            good_user_id_index = 1
            bad_user_id_index = 0

        self.assertEqual(metrics[good_user_id_index]["user_id"], user_id)
        self.assertEqual(datetime.fromisoformat(metrics[good_user_id_index]["timestamp"]), datetime(
            2022, 12, 23, 13, 0, 51, tzinfo=timezone.utc))
        self.assertEqual(metrics[good_user_id_index]["units"], "W")
        self.assertEqual(metrics[good_user_id_index]["value"], 879.4)

        self.assertEqual(metrics[bad_user_id_index]
                         ["user_id"], second_user_id)
        self.assertEqual(datetime.fromisoformat(metrics[bad_user_id_index]["timestamp"]), datetime(
            1970, 1, 1, 0, 0, 0, tzinfo=timezone.utc))
        self.assertEqual(metrics[bad_user_id_index]["units"], "W")
        self.assertTrue(math.isnan(metrics[bad_user_id_index]["value"]))

    def test_power_consumption_last_get_empty(self):
        """Test case for power_consumption_last_get with an empty value on DB

        Retrieve the last value of the power consumption for several users but there is no value on DB.
        """
        clean_account()

        clean_influxdb()

        user_key, user_id, second_user_key, second_user_id = mock_register()

        query_string = {"user_ids": f"{user_id}"}

        headers = {
            "Accept": "application/json",
            "x_correlation_id": str(uuid.uuid4()),
        }

        response = self.client.open(
            "/api/statistics/power-consumption-last",
            method="GET",
            headers=headers,
            query_string=query_string,
        )
        self.assert200(response, "Response body is : " +
                       response.data.decode("utf-8"))

        metrics = json.loads(response.data.decode("utf-8"))

        metrics_dict = metrics[0]

        self.assertEqual(metrics_dict["user_id"], user_id)
        self.assertEqual(datetime.fromisoformat(metrics_dict["timestamp"]), datetime(
            1970, 1, 1, 0, 0, 0, tzinfo=timezone.utc))
        self.assertEqual(metrics_dict["units"], "W")
        self.assertTrue(math.isnan(metrics_dict["value"]))

    def test_power_consumption_wrong_userid(self):
        """Test case for power_consumption_last_get with a non existing user_id

        Retrieve the last value of the power consumption for several users with a non existing user_id
        """
        clean_account()

        query_string = {"user_ids": f"1234567890"}

        headers = {
            "Accept": "application/json",
            "x_correlation_id": str(uuid.uuid4()),
        }

        response = self.client.open(
            "/api/statistics/power-consumption-last",
            method="GET",
            headers=headers,
            query_string=query_string,
        )
        self.assert404(response, "Response body is : " +
                       response.data.decode("utf-8"))

    def test_power_consumption_last_get_several_users_with_authentication(self):
        """Test case for power_consumption_last_get for several users with authentication
        Meaning that the user will not have access to the other user_id

        Retrieve the last value of the power consumption for several users with authentication
        The user does not have access to the second user_id
        """
        clean_account()

        user_key, user_id, second_user_key, second_user_id = mock_register()

        authorization = superuser_login(id=user_key)

        query_string = {"user_ids": f"{user_id},{second_user_id}"}

        headers = {
            "Accept": "application/json",
            "x_correlation_id": str(uuid.uuid4()),
            "Authorization": authorization,
        }

        response = self.client.open(
            "/api/statistics/power-consumption-last",
            method="GET",
            headers=headers,
            query_string=query_string,
        )
        self.assert403(response, "Response body is : " +
                       response.data.decode("utf-8"))


if __name__ == '__main__':
    unittest.main()
