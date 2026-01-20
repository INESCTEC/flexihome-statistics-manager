from datetime import datetime, timezone
import connexion

from statistics_manager_service.models.energy_metrics import EnergyMetrics
from statistics_manager_service.models.energy_metric import EnergyMetric
from statistics_manager_service.models.forecast_vs_real import ForecastVsReal as FVR
from statistics_manager_service.models.energy_time_series import EnergyTimeSeries, EnergyUnits
from statistics_manager_service.models.database.db_models import (
    DBMetricsDaily,
    DBMetricsHourly,
    DBMetricsMonthly,
    ForecastVsReal
)
from statistics_manager_service.models.error import Error
from statistics_manager_service import util, logger, db
from statistics_manager_service.config import Config
from statistics_manager_service.exception_handling_utils.auth import verify_hems_auth
from statistics_manager_service.controllers.utils import get_users_influxdb_power_data

def power_consumed_real_get(start_date, user_id, group_by=None, end_date=None):
    cor_id = {
        "X-Correlation-ID": connexion.request.headers["X-Correlation-ID"]}

    end_text = "Processed GET /energy-usage request"
    operation_text = "get consumed energy from user account"
    logger.info(operation_text, extra=cor_id)

    start_date = util.deserialize_datetime(start_date)
    if end_date is None:
        end_date = datetime.now(timezone.utc).strftime("%d-%m-%YT%H:%M:%S%z")
    end_date = util.deserialize_datetime(end_date)
    # end_date = datetime(end_date.year, end_date.month, end_date.day, 23, 59, 0)

    logger.debug(f"User Ids: {user_id}", extra=cor_id)
    logger.debug(f"start_date: {start_date}", extra=cor_id)
    logger.debug(f"end_date: {end_date}", extra=cor_id)
    logger.debug(f"group_by: {group_by}", extra=cor_id)

    response_code = 200

# -------------------------- Verify request permissions -------------------------- #

    response, response_code, users_list = verify_hems_auth(
        connexion.request.headers, [user_id], end_text, cor_id
    )

    if response_code == 200:

        response, code, error_message = get_users_influxdb_power_data(user_id, False, cor_id, start_date, end_date, group_by)

        return [response], code, cor_id
        # return response, response_code, cor_id
            
    if 400 <= response_code < 600:
        logger.error(f"Returning error code: {response_code}", extra=cor_id)
    else:
        logger.info(f"Returning response code: {response_code}", extra=cor_id)

    return response, response_code, cor_id



def energy_consumed_forecast_vs_real_get(start_date, user_ids=None, group_by=None, end_date=None):  # noqa: E501
    """List of user&#39;s forecasted energy consumption vs. real consumption

     # noqa: E501

    :param x_correlation_id: 
    :type x_correlation_id: str
    :type x_correlation_id: str
    :param start_date: 
    :type start_date: str
    :param authorization: 
    :type authorization: str
    :param user_ids: 
    :type user_ids: List[str]
    :param group_by: 
    :type group_by: str
    :param end_date: 
    :type end_date: str

    :rtype: Union[List[ForecastVsReal], Tuple[List[ForecastVsReal], int], Tuple[List[ForecastVsReal], int, Dict[str, str]]
    """
    cor_id = {"X-Correlation-ID": connexion.request.headers["X-Correlation-ID"]}

    end_text = "Processed GET /energy-usage request"
    operation_text = "get consumed energy from user account"
    logger.info(operation_text, extra=cor_id)

    start_date = util.deserialize_date(start_date)
    if end_date is None:
        end_date = datetime.now(timezone.utc).strftime("%d-%m-%YT%H:%M:%S%z")
    end_date = util.deserialize_date(end_date)
    end_date = datetime(end_date.year, end_date.month, end_date.day, 23, 59, 0)

    logger.debug(f"User Ids: {user_ids}", extra=cor_id)
    logger.debug(f"start_date: {start_date}", extra=cor_id)
    logger.debug(f"end_date: {end_date}", extra=cor_id)
    logger.debug(f"group_by: {group_by}", extra=cor_id)

    response_code = 200



    # -------------------------- Verify request permissions -------------------------- #

    response, response_code, users_list = verify_hems_auth(
        connexion.request.headers, user_ids, end_text, cor_id
    )

    
    if response_code == 200:

        response = []
        for user_id in users_list:

            db_forecast_vs_real = db.session.query(ForecastVsReal).filter(
                ForecastVsReal.timestamp >= start_date,
                ForecastVsReal.timestamp <= end_date,
                ForecastVsReal.user_id == user_id
            ).all()

            if db_forecast_vs_real is not None:
                
                
                # -------- Check if user has forecast data -------- #

                has_forecast = _forecast_vs_real_check_data("forecast", start_date, end_date, user_id, cor_id)
                if has_forecast == False:
                    logger.warning(
                        f"Forecast for user {user_id} between {start_date} and {end_date} is empty",
                        extra=cor_id
                    )
                    # response = Error("User has no forecast on specified date interval")
                    # response_code = 400

                    # break
                

                # -------- Check if user has dongle/smart_meter data -------- #

                has_dongle = _forecast_vs_real_check_data("dongle", start_date, end_date, user_id, cor_id)
                has_smart_meter = _forecast_vs_real_check_data("smart_meter", start_date, end_date, user_id, cor_id)
                if (has_dongle == False) and (has_smart_meter == False):
                    logger.warning(
                        f"Real data for user {user_id} between {start_date} and {end_date} is empty",
                        extra=cor_id
                    )
                    # response = Error("User has no real data on specified date interval")
                    # response_code = 400
                    
                    # break


                # -------- User real data is retrieved from dongles/smart_meter -------- #

                # else:
                if has_dongle:
                    logger.info(f"User {user_id} has dongle data", extra=cor_id)
                else:
                    logger.info(f"User {user_id} does NOT have a dongle. Using smart meter data", extra=cor_id)  

                # NOTE: Verify if dongle/smart_meter length is the same has forecast lenght?
                # NOTE: This verification should be done when inserting in the DB
                forecast, real = [], []
                slot_number = 1
                for row in db_forecast_vs_real:
                    
                    # TODO: Change when <group_by> is implemented
                    if row.units == "kW":
                        units = EnergyUnits.KWH
                    else:
                        units = EnergyUnits.WH
                    
                    
                    if has_forecast:
                        forecast.append(EnergyTimeSeries(
                            timestamp=row.timestamp, energy=row.forecast if row.forecast >= 0 else 0, units=units,
                            slot_number=slot_number
                        ))
                    else:
                        forecast = []

                    if has_dongle:
                        real.append(EnergyTimeSeries(
                            timestamp=row.timestamp, energy=row.dongle if row.dongle >= 0 else 0, units=units,
                            slot_number=slot_number
                        ))
                    elif has_smart_meter:
                        real.append(EnergyTimeSeries(
                            timestamp=row.timestamp, energy=row.smart_meter if row.smart_meter >= 0 else 0, units=units,
                            slot_number=slot_number
                        ))
                    else:
                        real = []

                    slot_number += 1
                
                response.append(FVR(user_id=user_id, forecast=forecast, real=real))

    
            else:
                logger.warning(f"Query for user {user_id} returned no results", extra=cor_id)
                response.append(FVR(user_id=user_id, forecast=[], real=[]))

    if 400 <= response_code < 600:
        logger.error(f"Returning error code: {response_code}", extra=cor_id)
    else:
        logger.info(f"Returning response code: {response_code}", extra=cor_id)
    
    return response, response_code, cor_id




def _forecast_vs_real_check_data(column, start_date, end_date, user_id, cor_id):
    has_data = False
    
    if column == "forecast":
        db_condition = db.session.query(ForecastVsReal).filter(
            ForecastVsReal.timestamp >= start_date,
            ForecastVsReal.timestamp <= end_date,
            ForecastVsReal.user_id == user_id,
            ForecastVsReal.forecast != None
        ).all()

        has_data = len(db_condition) != 0

    elif column == "dongle":
        db_condition = db.session.query(ForecastVsReal).filter(
            ForecastVsReal.timestamp >= start_date,
            ForecastVsReal.timestamp <= end_date,
            ForecastVsReal.user_id == user_id,
            ForecastVsReal.dongle != None
        ).all()

        has_data = len(db_condition) != 0

    elif column == "smart_meter":
        db_condition = db.session.query(ForecastVsReal).filter(
            ForecastVsReal.timestamp >= start_date,
            ForecastVsReal.timestamp <= end_date,
            ForecastVsReal.user_id == user_id,
            ForecastVsReal.smart_meter != None
        ).all()

        has_data = len(db_condition) != 0

    else:
        logger.error(f"Column {column} is not a valid one", extra=cor_id)

    logger.debug(f"{column} has data? {has_data}", extra=cor_id)
    
    return has_data



def _save_consumption_metric(
    user_id, consumed_energy, metrics, fixed_timestamp, slot_number, group_by, cor_id
):
    metric = EnergyMetric(
        timestamp=fixed_timestamp,
        value=consumed_energy,
        units="kWh", # TODO: All data must be saved hourly and the grouped by accordingly. The measure is always kWh.
        slot_number=slot_number,
    )

    metrics.append(metric)


    # Verificar se a métrica já existe na bd e guardar ou dar replace
    if group_by == "monthly":
        existing_metric = db.session.query(DBMetricsMonthly).filter(
            extract("month", DBMetricsMonthly.timestamp) == fixed_timestamp.month,
            extract("year", DBMetricsMonthly.timestamp) == fixed_timestamp.year,
        ).first()

        metric_db_obj = DBMetricsMonthly(
            timestamp=metric.timestamp,
            consumed_value=metric.value,
            units=metric.units,
            slot_number=metric.slot_number,
            user_id=user_id,
        )

        if existing_metric is None:
            logger.info(
                f"Metric for time - {metric.timestamp} - is not in DB. Saving....\n",
                extra=cor_id,
            )

            db.session.add(metric_db_obj)

        else:
            logger.debug(f"ID existing metric: {existing_metric.id}", extra=cor_id)
            db.session.query(DBMetricsMonthly).filter_by(id=existing_metric.id).delete()
            db.session.add(metric_db_obj)

    elif group_by == "daily":
        existing_metric = db.session.query(DBMetricsDaily).filter(
            extract("month", DBMetricsDaily.timestamp) == fixed_timestamp.month,
            extract("year", DBMetricsDaily.timestamp) == fixed_timestamp.year,
            extract("day", DBMetricsDaily.timestamp) == fixed_timestamp.day,
        ).first()

        metric_db_obj = DBMetricsDaily(
            timestamp=metric.timestamp,
            consumed_value=metric.value,
            units=metric.units,
            slot_number=metric.slot_number,
            user_id=user_id,
        )

        if existing_metric is None:
            logger.info(
                f"Metric for time - {metric.timestamp} - is not in DB. Saving....\n",
                extra=cor_id,
            )

            db.session.add(metric_db_obj)
            
        else:
            logger.debug(f"ID existing metric: {existing_metric.id}", extra=cor_id)
            db.session.query(DBMetricsDaily).filter_by(id=existing_metric.id).delete()
            db.session.add(metric_db_obj)

    elif group_by == "hourly":
        existing_metric = db.session.query(DBMetricsHourly).filter(
            extract("month", DBMetricsHourly.timestamp) == fixed_timestamp.month,
            extract("year", DBMetricsHourly.timestamp) == fixed_timestamp.year,
            extract("day", DBMetricsHourly.timestamp) == fixed_timestamp.day,
            extract("hour", DBMetricsHourly.timestamp) == fixed_timestamp.hour,
        ).first()

        metric_db_obj = DBMetricsHourly(
            timestamp=metric.timestamp,
            consumed_value=metric.value,
            units=metric.units,
            slot_number=metric.slot_number,
            user_id=user_id,
        )

        if existing_metric is None:
            logger.info(
                f"Metric for time - {metric.timestamp} - is not in DB. Saving....\n",
                extra=cor_id,
            )

            db.session.add(metric_db_obj)
            
        else:
            logger.debug(f"ID existing metric: {existing_metric.id}", extra=cor_id)
            db.session.query(DBMetricsHourly).filter_by(id=existing_metric.id).delete()
            db.session.add(metric_db_obj)
    
    db.session.commit()
