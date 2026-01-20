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
    populate_influxdb_energy_exported,
    clean_account,
    superuser_login,
    mock_register,
    mock_change_settings,
)


class TestEnergyQueriesControllerInjectionLast(BaseTestCase):
    """EnergyQueriesController for injection last values integration test stubs"""

    def test_energy_injection_last_get(self):
        """Test case for energy_injection_last_get

        Retrieve the last value of the energy injection for one user.
        """
        clean_account()

        clean_influxdb()
        populate_influxdb_energy_exported()

        user_key, user_id, second_user_key, second_user_id = mock_register()

        query_string = {"user_ids": f"{user_id}"}

        headers = {
            "Accept": "application/json",
            "x_correlation_id": str(uuid.uuid4()),
        }

        response = self.client.open(
            "/api/statistics/energy-injection-last",
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
            2022, 9, 19, 6, 3, 30, tzinfo=timezone.utc))
        self.assertEqual(metrics_dict["units"], "Wh")
        self.assertEqual(metrics_dict["value"], 110.8)

    def test_energy_injection_last_get_several_users_and_no_api_key(self):
        """Test case for energy_injection_last_get for several users

        Retrieve the last value of the energy injection for several users.
        One of the users does not have an API Key
        """
        clean_account()

        clean_influxdb()
        populate_influxdb_energy_exported()

        user_key, user_id, second_user_key, second_user_id = mock_register()

        query_string = {"user_ids": f"{user_id},{second_user_id}"}

        headers = {
            "Accept": "application/json",
            "x_correlation_id": str(uuid.uuid4()),
        }

        response = self.client.open(
            "/api/statistics/energy-injection-last",
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
            2022, 9, 19, 6, 3, 30, tzinfo=timezone.utc))
        self.assertEqual(metrics[good_user_id_index]["units"], "Wh")
        self.assertEqual(metrics[good_user_id_index]["value"], 110.8)

        self.assertEqual(metrics[bad_user_id_index]
                         ["user_id"], second_user_id)
        self.assertEqual(datetime.fromisoformat(metrics[bad_user_id_index]["timestamp"]), datetime(
            1970, 1, 1, 0, 0, 0, tzinfo=timezone.utc))
        self.assertEqual(metrics[bad_user_id_index]["units"], "Wh")
        self.assertTrue(math.isnan(metrics[bad_user_id_index]["value"]))

    def test_energy_injection_last_get_empty(self):
        """Test case for energy_injection_last_get with an empty value on DB

        Retrieve the last value of the energy injection for several users but there is no value on DB.
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
            "/api/statistics/energy-injection-last",
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
        self.assertEqual(metrics_dict["units"], "Wh")
        self.assertTrue(math.isnan(metrics_dict["value"]))

    def test_energy_injection_wrong_userid(self):
        """Test case for energy_injection_last_get with a non existing user_id

        Retrieve the last value of the energy injection for several users with a non existing user_id
        """
        clean_account()

        clean_influxdb()

        query_string = {"user_ids": f"1234567890"}

        headers = {
            "Accept": "application/json",
            "x_correlation_id": str(uuid.uuid4()),
        }

        response = self.client.open(
            "/api/statistics/energy-injection-last",
            method="GET",
            headers=headers,
            query_string=query_string,
        )
        self.assert404(response, "Response body is : " +
                       response.data.decode("utf-8"))

    def test_energy_injection_last_get_several_users_with_authentication(self):
        """Test case for energy_injection_last_get for several users with authentication
        Meaning that the user will not have access to the other user_id

        Retrieve the last value of the energy injection for several users with authentication
        The user does not have access to the second user_id
        """
        clean_account()

        clean_influxdb()

        user_key, user_id, second_user_key, second_user_id = mock_register()

        authorization = superuser_login(id=user_key)

        query_string = {"user_ids": f"{user_id},{second_user_id}"}

        headers = {
            "Accept": "application/json",
            "x_correlation_id": str(uuid.uuid4()),
            "Authorization": authorization,
        }

        response = self.client.open(
            "/api/statistics/energy-injection-last",
            method="GET",
            headers=headers,
            query_string=query_string,
        )
        self.assert403(response, "Response body is : " +
                       response.data.decode("utf-8"))


if __name__ == '__main__':
    unittest.main()
