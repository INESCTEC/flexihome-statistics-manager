from statistics_manager_service.models.energy_metrics import EnergyMetrics
from statistics_manager_service.models.energy_metric import EnergyMetric
from statistics_manager_service.models.energy_units import EnergyUnits
from statistics_manager_service.models.energy_time_series import EnergyTimeSeries
from statistics_manager_service.models.power_metrics import PowerMetrics
from statistics_manager_service.models.power_metric import PowerMetric
from statistics_manager_service.models.power_units import PowerUnits
from statistics_manager_service.models.voltage_metrics import VoltageMetrics
from statistics_manager_service.models.voltage_metric import VoltageMetric
from statistics_manager_service.models.voltage_units import VoltageUnits
from statistics_manager_service.models.instant_energy_metric import InstantEnergyMetric
from statistics_manager_service.models.instant_power_metric import InstantPowerMetric
from statistics_manager_service.models.instant_voltage_metric import InstantVoltageMetric
from statistics_manager_service.models.forecast_vs_real import ForecastVsReal as FVR

from statistics_manager_service import logger, generalLogger, INFLUX_DB_DATE_FORMAT
from statistics_manager_service.config import Config
from statistics_manager_service.models.error import Error

import math
from datetime import datetime, timedelta, timezone
import influxdb_client
import requests
import pandas as pd
import numpy as np
from pandas.tseries.offsets import DateOffset
from dateutil.relativedelta import relativedelta

def logErrorResponse(error, endText, response, cor_id):
    logger.error(error, extra=cor_id)
    logResponse(endText, response, cor_id)


def logResponse(endText, response, cor_id):
    logger.info(f"{endText}\n", extra=cor_id)
    if response is not None:
        logger.debug("Sending the following response: ", extra=cor_id)
        logger.debug(f"{response}\n", extra=cor_id)


seconds_in_day = 60 * 60 * 24
seconds_in_hour = 60 * 60
seconds_in_minute = 60

hours_in_day = 24
minutes_in_hour = 60
seconds_in_minute = 60

influx_db_timestamp_format = '%Y-%m-%d %H:%M:%S%z'


def seconds_to_days_minutes_hours(seconds, log=True):
    days = math.floor(seconds / seconds_in_day)
    hours = math.floor(seconds / seconds_in_hour)
    minutes = math.floor(seconds / seconds_in_minute)

    hours_in_rounded_days = days * hours_in_day
    hours_real = hours - hours_in_rounded_days

    minutes_in_rounded_hours = hours * minutes_in_hour
    minutes_real = minutes - minutes_in_rounded_hours

    seconds_in_rounded_minutes = minutes * seconds_in_minute
    seconds_real = seconds - seconds_in_rounded_minutes

    if log:
        generalLogger.info(
            f"Thread alive for {days} days, {hours_real} hours, {minutes_real} minutes and {seconds_real} seconds.")

    return days, hours_real, minutes_real, seconds_real


def get_values_influxdb_energy(user_ids, db_variable, last, corId, start_date=None, end_date=None, group_by=None):
    logger.info(
        f"Getting users information from account manager...", extra=corId)
    headers = {
        "X-Correlation-ID": "b2fdda1b-9550-4afd-9b3d-d180a6398986",
    }
    query_string = {"user-ids": user_ids}
    users_response = requests.get(
        Config.ACCOUNT_MANAGER_ENDPOINT + "/user",
        headers=headers,
        params=query_string
    )

    users = users_response.json()

    if users_response.status_code != 200:
        logger.error(
            f"The call to account manager to get the users information returned the following error {users}",
            extra=corId,
        )
        message = users["error"]
        response = Error(message)

        return response, users_response.status_code, message

    client = influxdb_client.InfluxDBClient(
        url=f"http://{Config.INFLUX_URL}:{Config.INFLUX_PORT}",
        token=Config.INFLUX_TOKEN,
        org=Config.INFLUX_ORG
    )

    query_api = client.query_api()
    response = []

    for user in users:
        if user.get("api_key") is None:
            if last == False:
                metric = EnergyMetrics(user_id=user["user_id"],
                                       metrics=[])
            else:
                metric = InstantEnergyMetric(user_id=user["user_id"], timestamp=datetime.fromtimestamp(0, tz=timezone.utc),
                                             value=float('nan'), units=EnergyUnits.WH)
            response.append(metric)
            continue

        if end_date is None:
            end_date = datetime.now(timezone.utc)

        if group_by == "daily":
            aggregate_time = "1D"
            interpolation_interval = "15min"
            aux_start_date = start_date - timedelta(days=1)
            aux_end_date = end_date + timedelta(days=1)
        elif group_by == "15_mins":
            aggregate_time = "15min"
            interpolation_interval = "30S"
            aux_start_date = start_date - timedelta(minutes=15)
            aux_end_date = end_date + timedelta(minutes=15)
        elif group_by == "hourly":
            aggregate_time = "1H"
            interpolation_interval = "2min"
            aux_start_date = start_date - timedelta(hours=1)
            aux_end_date = end_date + timedelta(hours=1)
        elif group_by == "weekly":
            aggregate_time = "7D"
            interpolation_interval = "30min"
            aux_start_date = start_date - timedelta(days=7)
            aux_end_date = end_date + timedelta(days=7)
        elif group_by == "monthly":
            # aggregate_time = "1mo"
            aggregate_time = "MS"
            interpolation_interval = "2H"
            aux_start_date = start_date - relativedelta(months=1)
            aux_end_date = end_date + relativedelta(months=1)

        if last == False:
            query = f"""from(bucket: "{Config.INFLUX_BUCKET}")
                |> range(start: {int(aux_start_date.timestamp())}, stop: {int(aux_end_date.timestamp())})
                |> filter(fn: (r) => r["_measurement"] == "{user["api_key"]}")
                |> filter(fn: (r) => r["_field"] == "{db_variable}")
                |> yield(name: "{db_variable}")"""
        else:
            query = f"""from(bucket: "{Config.INFLUX_BUCKET}")
                |> range(start: 0)
                |> filter(fn: (r) => r["_measurement"] == "{user["api_key"]}")
                |> filter(fn: (r) => r["_field"] == "{db_variable}")
                |> last()"""

        logger.debug(f"Query: {query}\n", extra=corId)

        try:
            influx_df = query_api.query_data_frame(query=query)
        except Exception as e:
            logger.error(e, extra=corId)

            message = "Internal Server Error"
            response = Error(message)

            return response, 500, message

        logger.debug(f"InfluxDB query result: {influx_df}\n", extra=corId)

        if influx_df.size == 0:
            if last == False:
                metric = EnergyMetrics(user_id=user["user_id"], metrics=[])
            else:
                metric = InstantEnergyMetric(user_id=user["user_id"], timestamp=datetime.fromtimestamp(0, tz=timezone.utc),
                                             value=float('nan'), units=EnergyUnits.WH)

            response.append(metric)
            continue

        if last == False:
            initial_data = [[aux_start_date, float('nan')], [
                aux_end_date, float('nan')]]
            main_df = pd.DataFrame(initial_data, columns=[
                                   'timestamp', 'value'])
            main_df = main_df.set_index('timestamp')

            main_df = main_df.resample(interpolation_interval).mean()

            df = influx_df[['_time', '_value']].copy()
            df.rename(columns={'_time': 'timestamp',
                      '_value': 'value'}, inplace=True)
            df = df.set_index('timestamp')

            main_df = pd.concat([main_df, df], ignore_index=False).sort_index()

            # main_df = main_df[~main_df.index.duplicated(keep='last')]
            main_df = main_df[~main_df.index.duplicated(
                keep=False) | main_df[['value']].notnull().any(axis=1)]

            main_df = main_df.interpolate(method='time')

            end_remove = pd.to_datetime(end_date)
            main_df = main_df.query(f'index <= @end_remove')

            main_df = main_df.groupby(pd.Grouper(
                freq=aggregate_time, label='left')).last()

            main_df = main_df.diff()

            main_df = main_df.iloc[1:]

            main_df['value'] = np.where(np.isnan(main_df['value']) == True, float('nan'), round(main_df['value'], 2))

            print(main_df.to_string())

            metrics = []
            slot_number = 1
            for index, row in main_df.iterrows():
                metric = EnergyMetric(timestamp=index,
                                      slot_number=slot_number,
                                      value=row['value'],
                                      units=EnergyUnits.WH)

                metrics.append(metric)
                slot_number = slot_number + 1

            metric = EnergyMetrics(user_id=user["user_id"],
                                   metrics=metrics)
        else:
            metric = InstantEnergyMetric(user_id=user["user_id"], timestamp=influx_df.iloc[0]["_time"],
                                         value=influx_df.iloc[0]["_value"], units=EnergyUnits.WH)

        # print(metric)

        response.append(metric)

    return response, 200, ""


def get_values_influxdb_power(user_ids, db_variable, last, corId, start_date=None, end_date=None, group_by=None):
    logger.info(
        f"Getting users information from account manager...", extra=corId)
    headers = {
        "X-Correlation-ID": "b2fdda1b-9550-4afd-9b3d-d180a6398986",
    }
    query_string = {"user-ids": user_ids}
    users_response = requests.get(
        Config.ACCOUNT_MANAGER_ENDPOINT + "/user",
        headers=headers,
        params=query_string
    )

    users = users_response.json()
    logger.debug(f"Users response: {users}", extra=corId)

    if users_response.status_code != 200:
        logger.error(
            f"The call to account manager to get the users information returned the following error {users}",
            extra=corId,
        )
        message = users["error"]
        response = Error(message)

        return response, users_response.status_code, message

    client = influxdb_client.InfluxDBClient(
        url=f"http://{Config.INFLUX_URL}:{Config.INFLUX_PORT}",
        token=Config.INFLUX_TOKEN,
        org=Config.INFLUX_ORG
    )

    query_api = client.query_api()
    response = []

    for user in users:
        if user.get("api_key") is None:
            if last == False:
                metric = PowerMetrics(user_id=user["user_id"],
                                      metrics=[])
            else:
                metric = InstantPowerMetric(user_id=user["user_id"], timestamp=datetime.fromtimestamp(0, tz=timezone.utc),
                                            value=float('nan'), units=PowerUnits.W)
            response.append(metric)
            continue

        if end_date is None:
            end_date = datetime.now(timezone.utc)

        if group_by == "daily":
            aggregate_time = "1D"
            interpolation_interval = "1D"
            # aux_start_date = start_date - timedelta(days=1)
            # aux_end_date = end_date + timedelta(days=1)
        elif group_by == "15_mins":
            aggregate_time = "15min"
            interpolation_interval = "15min"
            # aux_start_date = start_date - timedelta(minutes=15)
            # aux_end_date = end_date + timedelta(minutes=15)
        elif group_by == "hourly":
            aggregate_time = "1H"
            interpolation_interval = "1H"
            # aux_start_date = start_date - timedelta(hours=1)
            # aux_end_date = end_date + timedelta(hours=1)
        elif group_by == "weekly":
            aggregate_time = "7D"
            interpolation_interval = "7D"
            # aux_start_date = start_date - timedelta(days=7)
            # aux_end_date = end_date + timedelta(days=7)
        elif group_by == "monthly":
            # aggregate_time = "1mo"
            aggregate_time = "MS"
            interpolation_interval = "MS"
            # aux_start_date = start_date - relativedelta(months=1)
            # aux_end_date = end_date + relativedelta(months=1)
        
        if last == False:
            query = f"""from(bucket: "{Config.INFLUX_BUCKET}")
                |> range(start: {int(start_date.timestamp())}, stop: {int(end_date.timestamp())})
                |> filter(fn: (r) => r["_measurement"] == "{user["api_key"]}")
                |> filter(fn: (r) => r["_field"] == "{db_variable}")
                |> yield(name: "{db_variable}")"""
        else:
            query = f"""from(bucket: "{Config.INFLUX_BUCKET}")
                |> range(start: 0)
                |> filter(fn: (r) => r["_measurement"] == "{user["api_key"]}")
                |> filter(fn: (r) => r["_field"] == "{db_variable}")
                |> last()"""

        logger.debug(f"Query: {query}\n", extra=corId)

        try:
            influx_df = query_api.query_data_frame(query=query)
        except Exception as e:
            logger.error(e, extra=corId)

            message = "Internal Server Error"
            response = Error(message)

            return response, 500, message

        logger.debug(f"InfluxDB query result: {influx_df}\n", extra=corId)

        if influx_df.size == 0:
            if last == False:
                metric = PowerMetrics(user_id=user["user_id"],
                                      metrics=[])
            else:
                metric = InstantPowerMetric(user_id=user["user_id"], timestamp=datetime.fromtimestamp(0, tz=timezone.utc),
                                            value=float('nan'), units=PowerUnits.W)

            response.append(metric)
            continue

        if last == False:
            initial_data = [[start_date, float('nan')], [
                end_date, float('nan')]]
            main_df = pd.DataFrame(initial_data, columns=[
                                   'timestamp', 'value'])
            main_df = main_df.set_index('timestamp')

            main_df = main_df.resample(interpolation_interval).mean()

            df = influx_df[['_time', '_value']].copy()
            df.rename(columns={'_time': 'timestamp',
                      '_value': 'value'}, inplace=True)
            df = df.set_index('timestamp')

            main_df = pd.concat([main_df, df], ignore_index=False).sort_index()

            # main_df = main_df[~main_df.index.duplicated(keep='last')]
            main_df = main_df[~main_df.index.duplicated(
                keep=False) | main_df[['value']].notnull().any(axis=1)]

            # print(main_df.to_string())

            # main_df = main_df.interpolate(method='time')

            # end_remove = pd.to_datetime(end_date)
            # main_df = main_df.query(f'index <= @end_remove')

            main_df = main_df.groupby(pd.Grouper(
                freq=aggregate_time, label='left')).mean()

            # main_df = main_df.diff()

            # main_df = main_df.iloc[1:]

            # print(main_df.to_string())

            # main_df = main_df.round({'value': 2})
            # main_df["value"] = main_df["value"].astype(float).round(2)
            # main_df["value"] = np.round(main_df["value"], decimals = 2)
            main_df['value'] = np.where(np.isnan(main_df['value']) == True, float('nan'), round(main_df['value'], 2))

            print(main_df.to_string())
        

        # if last == False:
        #     powerQuery = f"""from(bucket: "{Config.INFLUX_BUCKET}")
        #         |> range(start: {int(aux_start_date.timestamp())}, stop: {int(aux_end_date.timestamp())})
        #         |> filter(fn: (r) => r["_measurement"] == "{user["api_key"]}")
        #         |> filter(fn: (r) => r["_field"] == "{db_variable}")
        #         |> yield(name: "{db_variable}")"""
        # else:
        #     powerQuery = f"""from(bucket: "{Config.INFLUX_BUCKET}")
        #         |> range(start: 0)
        #         |> filter(fn: (r) => r["_measurement"] == "{user["api_key"]}")
        #         |> filter(fn: (r) => r["_field"] == "{db_variable}")
        #         |> last()"""

        # logger.debug(f"Query: {powerQuery}\n", extra=corId)

        # try:
        #     influx_df_power = query_api.query_data_frame(query=powerQuery)
        # except Exception as e:
        #     logger.error(e, extra=corId)

        #     message = "Internal Server Error"
        #     response = Error(message)

        #     return response, 500, message

        # logger.debug(f"InfluxDB power query result: {influx_df_power}\n", extra=corId)

        # if influx_df_power.size == 0:
        #     if last == False:
        #         metric = PowerMetrics(user_id=user["user_id"],
        #                               metrics=[])
        #     else:
        #         metric = InstantPowerMetric(user_id=user["user_id"], timestamp=datetime.fromtimestamp(0, tz=timezone.utc),
        #                                     value=float('nan'), units=PowerUnits.W)

        #     response.append(metric)
        #     continue

        # if last == False:
        #     if db_variable == "powerImported":
        #         energyQuery = f"""from(bucket: "{Config.INFLUX_BUCKET}")
        #             |> range(start: {int(aux_start_date.timestamp())}, stop: {int(aux_end_date.timestamp())})
        #             |> filter(fn: (r) => r["_measurement"] == "{user["api_key"]}")
        #             |> filter(fn: (r) => r["_field"] == "energyImported")
        #             |> yield(name: "energyImported")"""
        #     elif db_variable == "powerExported":
        #         energyQuery = f"""from(bucket: "{Config.INFLUX_BUCKET}")
        #             |> range(start: {int(aux_start_date.timestamp())}, stop: {int(aux_end_date.timestamp())})
        #             |> filter(fn: (r) => r["_measurement"] == "{user["api_key"]}")
        #             |> filter(fn: (r) => r["_field"] == "energyExported")
        #             |> yield(name: "energyExported")"""
            
        #     logger.debug(f"EnergyQuery: {energyQuery}\n", extra=corId)

        #     try:
        #         influx_df_energy = query_api.query_data_frame(query=energyQuery)
        #     except Exception as e:
        #         logger.error(e, extra=corId)

        #         message = "Internal Server Error"
        #         response = Error(message)

        #         return response, 500, message

        #     logger.debug(f"InfluxDB energy query result: {influx_df_energy}\n", extra=corId)

        #     initial_data = [[aux_start_date, float('nan')], [
        #         aux_end_date, float('nan')]]
        #     main_df = pd.DataFrame(initial_data, columns=[
        #                            'timestamp', 'value'])
        #     main_df = main_df.set_index('timestamp')

        #     main_df = main_df.resample(interpolation_interval).mean()

        #     df = influx_df_energy[['_time', '_value']].copy()
        #     df.rename(columns={'_time': 'timestamp',
        #               '_value': 'value'}, inplace=True)
        #     df = df.set_index('timestamp')

        #     main_df = pd.concat([main_df, df], ignore_index=False).sort_index()

        #     # main_df = main_df[~main_df.index.duplicated(keep='last')]
        #     main_df = main_df[~main_df.index.duplicated(
        #         keep=False) | main_df[['value']].notnull().any(axis=1)]

        #     main_df = main_df.interpolate(method='time')

        #     end_remove = pd.to_datetime(end_date)
        #     main_df = main_df.query(f'index <= @end_remove')

        #     main_df = main_df.groupby(pd.Grouper(
        #         freq=aggregate_time, label='left')).last()

        #     main_df = main_df.diff()

        #     # print(main_df.to_string())

        #     main_df = main_df.iloc[1:]

        #     main_df = main_df.div(divide_by)

        #     # print(main_df.to_string())
            
        #     # print(influx_df_energy.iloc[-1])
        #     influx_db_energy_last_date = influx_df_energy.iloc[-1]["_time"]

        #     main_df.loc[influx_db_energy_last_date] = 0
        #     # print(main_df.to_string())

        #     main_df = main_df.sort_index()

        #     influx_db_energy_last_value = main_df.iloc[main_df.index.get_loc(influx_db_energy_last_date)-1]
        #     main_df.loc[influx_db_energy_last_date] = influx_db_energy_last_value
        #     main_df.loc[influx_db_energy_last_date + pd.Timedelta(seconds=1)] = 0

        #     main_df = main_df.sort_index()

        #     # print(main_df.to_string())

        #     main_df = main_df.resample(interpolation_interval).mean()

        #     main_df.loc[influx_db_energy_last_date] = influx_db_energy_last_value
        #     main_df.loc[influx_db_energy_last_date + pd.Timedelta(seconds=1)] = 0

        #     main_df = main_df.sort_index()

        #     # Talvez nao precise de meter tantas vezes o influx_db_energy_last_value e 0
        #     # fazer dois cenários, um onde o ultimo valor de energia é menor que o pedido e outro maior

        #     print(main_df.to_string())

        #     df = influx_df_power[['_time', '_value']].copy()
        #     df.rename(columns={'_time': 'timestamp',
        #               '_value': 'value'}, inplace=True)
        #     df = df.set_index('timestamp')
        #     begin_remove = pd.to_datetime(influx_db_energy_last_date)
        #     df = df.query(f'index > @begin_remove')

        #     # print(df.to_string())

        #     # o ultimo valor no final vai ser o primeiro dia da leitura
        #     # por isso é preciso meter o timestamp final como igual ao valor do inicio da leitura
        #     # e só dps fazer o resampling e interpolacao

        #     # print(main_df.to_string())

            metrics = []
            slot_number = 1
            for index, row in main_df.iterrows():
                metric = PowerMetric(timestamp=index,
                                     slot_number=slot_number,
                                     value=row['value'],
                                     units=PowerUnits.W)

                metrics.append(metric)
                slot_number = slot_number + 1

            metric = PowerMetrics(user_id=user["user_id"],
                                  metrics=metrics)
        else:
            metric = InstantPowerMetric(user_id=user["user_id"], timestamp=influx_df.iloc[0]["_time"],
                                        value=influx_df.iloc[0]["_value"], units=PowerUnits.W)

        # print(metric)

        response.append(metric)

    return response, 200, ""


def get_values_influxdb_voltage(user_ids, db_variable, last, corId, start_date=None, end_date=None, group_by=None):
    logger.info(
        f"Getting users information from account manager...", extra=corId)
    headers = {
        "X-Correlation-ID": "b2fdda1b-9550-4afd-9b3d-d180a6398986",
    }
    query_string = {"user-ids": user_ids}
    users_response = requests.get(
        Config.ACCOUNT_MANAGER_ENDPOINT + "/user",
        headers=headers,
        params=query_string
    )

    users = users_response.json()

    if users_response.status_code != 200:
        logger.error(
            f"The call to account manager to get the users information returned the following error {users}",
            extra=corId,
        )
        message = users["error"]
        response = Error(message)

        return response, users_response.status_code, message

    client = influxdb_client.InfluxDBClient(
        url=f"http://{Config.INFLUX_URL}:{Config.INFLUX_PORT}",
        token=Config.INFLUX_TOKEN,
        org=Config.INFLUX_ORG
    )

    query_api = client.query_api()
    response = []

    for user in users:
        if user.get("api_key") is None:
            if last == False:
                metric = VoltageMetrics(user_id=user["user_id"],
                                      metrics=[])
            else:
                metric = InstantVoltageMetric(user_id=user["user_id"], timestamp=datetime.fromtimestamp(0, tz=timezone.utc),
                                            value=float('nan'), units=VoltageUnits.V)
            response.append(metric)
            continue

        if end_date is None:
            end_date = datetime.now(timezone.utc)

        if group_by == "daily":
            aggregate_time = "1D"
            interpolation_interval = "1D"
            # aux_start_date = start_date - timedelta(days=1)
            # aux_end_date = end_date + timedelta(days=1)
        elif group_by == "15_mins":
            aggregate_time = "15min"
            interpolation_interval = "15min"
            # aux_start_date = start_date - timedelta(minutes=15)
            # aux_end_date = end_date + timedelta(minutes=15)
        elif group_by == "hourly":
            aggregate_time = "1H"
            interpolation_interval = "1H"
            # aux_start_date = start_date - timedelta(hours=1)
            # aux_end_date = end_date + timedelta(hours=1)
        elif group_by == "weekly":
            aggregate_time = "7D"
            interpolation_interval = "7D"
            # aux_start_date = start_date - timedelta(days=7)
            # aux_end_date = end_date + timedelta(days=7)
        elif group_by == "monthly":
            # aggregate_time = "1mo"
            aggregate_time = "MS"
            interpolation_interval = "MS"
            # aux_start_date = start_date - relativedelta(months=1)
            # aux_end_date = end_date + relativedelta(months=1)
        
        if last == False:
            query = f"""from(bucket: "{Config.INFLUX_BUCKET}")
                |> range(start: {int(start_date.timestamp())}, stop: {int(end_date.timestamp())})
                |> filter(fn: (r) => r["_measurement"] == "{user["api_key"]}")
                |> filter(fn: (r) => r["_field"] == "{db_variable}")
                |> yield(name: "{db_variable}")"""
        else:
            query = f"""from(bucket: "{Config.INFLUX_BUCKET}")
                |> range(start: 0)
                |> filter(fn: (r) => r["_measurement"] == "{user["api_key"]}")
                |> filter(fn: (r) => r["_field"] == "{db_variable}")
                |> last()"""

        logger.debug(f"Query: {query}\n", extra=corId)

        try:
            influx_df = query_api.query_data_frame(query=query)
        except Exception as e:
            logger.error(e, extra=corId)

            message = "Internal Server Error"
            response = Error(message)

            return response, 500, message

        logger.debug(f"InfluxDB query result: {influx_df}\n", extra=corId)

        if influx_df.size == 0:
            if last == False:
                metric = VoltageMetrics(user_id=user["user_id"],
                                      metrics=[])
            else:
                metric = InstantVoltageMetric(user_id=user["user_id"], timestamp=datetime.fromtimestamp(0, tz=timezone.utc),
                                            value=float('nan'), units=VoltageUnits.V)

            response.append(metric)
            continue

        if last == False:
            initial_data = [[start_date, float('nan')], [
                end_date, float('nan')]]
            main_df = pd.DataFrame(initial_data, columns=[
                                   'timestamp', 'value'])
            main_df = main_df.set_index('timestamp')

            main_df = main_df.resample(interpolation_interval).mean()

            df = influx_df[['_time', '_value']].copy()
            df.rename(columns={'_time': 'timestamp',
                      '_value': 'value'}, inplace=True)
            df = df.set_index('timestamp')

            main_df = pd.concat([main_df, df], ignore_index=False).sort_index()

            # main_df = main_df[~main_df.index.duplicated(keep='last')]
            main_df = main_df[~main_df.index.duplicated(
                keep=False) | main_df[['value']].notnull().any(axis=1)]

            # print(main_df.to_string())

            # main_df = main_df.interpolate(method='time')

            # end_remove = pd.to_datetime(end_date)
            # main_df = main_df.query(f'index <= @end_remove')

            main_df = main_df.groupby(pd.Grouper(
                freq=aggregate_time, label='left')).mean()

            # main_df = main_df.diff()

            # main_df = main_df.iloc[1:]

            # print(main_df.to_string())

            # main_df = main_df.round({'value': 2})
            # main_df["value"] = main_df["value"].astype(float).round(2)
            # main_df["value"] = np.round(main_df["value"], decimals = 2)
            main_df['value'] = np.where(np.isnan(main_df['value']) == True, float('nan'), round(main_df['value'], 2))

            print(main_df.to_string())

            metrics = []
            slot_number = 1
            for index, row in main_df.iterrows():
                metric = VoltageMetric(timestamp=index,
                                       slot_number=slot_number,
                                       value=row['value'],
                                       units=VoltageUnits.V)

                metrics.append(metric)
                slot_number = slot_number + 1

            metric = VoltageMetrics(user_id=user["user_id"],
                                    metrics=metrics)
        else:
            metric = InstantVoltageMetric(user_id=user["user_id"], timestamp=influx_df.iloc[0]["_time"],
                                        value=influx_df.iloc[0]["_value"], units=VoltageUnits.V)

        # print(metric)

        response.append(metric)

    return response, 200, ""


def get_users_influxdb_power_data(user_id, last, corId, start_date=None, end_date=None, group_by=None):
    logger.info(
        f"Getting users information from account manager...", extra=corId)
    headers = {
        "X-Correlation-ID": "61795a10-cec8-4094-a688-d3481d7c2ad2",
    }
    query_string = {"user-ids": user_id}
    users_response = requests.get(
        Config.ACCOUNT_MANAGER_ENDPOINT + "/user",
        headers=headers,
        params=query_string
    )

    user = users_response.json()[0]

    if users_response.status_code != 200:
        logger.error(f"The call to account manager to get the users information returned the following error {user}",extra=corId)
        message = user["error"]
        response = Error(message)

        return response, users_response.status_code, message

    client = influxdb_client.InfluxDBClient(
        url=f"http://{Config.INFLUX_URL}:{Config.INFLUX_PORT}",
        token=Config.INFLUX_TOKEN,
        org=Config.INFLUX_ORG
    )

    query_api = client.query_api()
    response = []

    if end_date is None:
        end_date = datetime.now(timezone.utc)

    if group_by == "daily":
        aggregate_time = "1d"
    elif group_by == "hourly":
        aggregate_time = "1h"

    if user.get("api_key") is None:
        query = f"""from(bucket: "{Config.INFLUX_BUCKET}")
            |> range(start: {start_date.strftime(INFLUX_DB_DATE_FORMAT)} , stop: {end_date.strftime(INFLUX_DB_DATE_FORMAT)})
            |> filter(fn: (r) => r["_measurement"] == "{user["meter_id"]}")
            |> filter(fn: (r) => r["_field"] == "meterPowerImported")
            |> aggregateWindow(every: {aggregate_time}, fn: sum, createEmpty: true)
            |> yield(name: "mean")"""
    else:
        query = f"""from(bucket: "{Config.INFLUX_BUCKET}")
            |> range(start: {start_date.strftime(INFLUX_DB_DATE_FORMAT)}, stop: {end_date.strftime(INFLUX_DB_DATE_FORMAT)})
            |> filter(fn: (r) => r["_measurement"] == "{user["api_key"]}")
            |> filter(fn: (r) => r["_field"] == "energyImported")
            |> aggregateWindow(every: {aggregate_time}, fn: mean, createEmpty: true)
            |> difference(nonNegative: false, columns: ["_value"])"""
    
    logger.debug(f"Query: {query}\n", extra=corId)

    try:
        influx_df = query_api.query_data_frame(query=query)
    except Exception as e:
        logger.error(e, extra=corId)

        message = "Internal Server Error"
        response = Error(message)

        return response, 500, message

    logger.debug(f"InfluxDB query result: {influx_df}\n", extra=corId)

    # Read influx data and export to EnergyTimeSeries

    if influx_df.size == 0:
        return FVR(user_id=user_id, real=[]), 200, ""

    real = []
    slot_number = 1
    count_null = 0
    size = 0
    for index, row in influx_df.iterrows():

        val = float(row._value) - 1 if isinstance(row._value, float) else -1
        
        if val == -1:
            count_null += 1
        
        energy_time_series = EnergyTimeSeries(
            timestamp=row._time, energy=(round(row._value, 1) if val > -1 else 0), slot_number=slot_number, units=EnergyUnits.KWH)

        real.append(energy_time_series)
        slot_number = slot_number + 1
        size = index + 1

    if count_null == size:
        metric = FVR(user_id=user_id, real=[])
    else:
        metric = FVR(user_id=user_id, real=real)

    return metric, 200, ""
