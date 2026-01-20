import uuid
from datetime import datetime

from sqlalchemy.dialects.postgresql import UUID, JSONB

from statistics_manager_service import db, Config
import string


#########################################################################
########################## Energy Usage Metrics #########################
#########################################################################

class DBMetricsHourly(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String(64), nullable=False)
    consumed_value = db.Column(db.Float, nullable=False)
    grid_consumed_value = db.Column(db.Float, nullable=True)
    other_value = db.Column(db.Float, nullable=True)
    self_consumed_value = db.Column(db.Float, nullable=True)
    thermal_value = db.Column(db.Float, nullable=True)
    slot_number = db.Column(db.Integer, nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False)
    units = db.Column(db.String(64), nullable=False)

    def __repr__(self):
        return f"""
        DBMetricsHourly(id={self.id}, consumed_value={self.consumed_value}, grid_consumed_value={self.grid_consumed_value}, 
        other_value={self.other_value}, self_consumed_value={self.self_consumed_value}, thermal_value={self.thermal_value},
        slot_number={self.slot_number}, timestamp={self.timestamp}, units={self.units}, user_id={self.user_id})"""


class DBMetricsDaily(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String(64), nullable=False)
    consumed_value = db.Column(db.Float, nullable=False)
    grid_consumed_value = db.Column(db.Float, nullable=True)
    other_value = db.Column(db.Float, nullable=True)
    self_consumed_value = db.Column(db.Float, nullable=True)
    thermal_value = db.Column(db.Float, nullable=True)
    slot_number = db.Column(db.Integer, nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False)
    units = db.Column(db.String(64), nullable=False)

    def __repr__(self):
        return f"""
        DBMetricsDaily(id={self.id}, consumed_value={self.consumed_value}, grid_consumed_value={self.grid_consumed_value}, 
        other_value={self.other_value}, self_consumed_value={self.self_consumed_value}, thermal_value={self.thermal_value},
        slot_number={self.slot_number}, timestamp={self.timestamp}, units={self.units}, user_id={self.user_id})"""


class DBMetricsMonthly(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String(64), nullable=False)
    consumed_value = db.Column(db.Float, nullable=False)
    grid_consumed_value = db.Column(db.Float, nullable=True)
    other_value = db.Column(db.Float, nullable=True)
    self_consumed_value = db.Column(db.Float, nullable=True)
    thermal_value = db.Column(db.Float, nullable=True)
    slot_number = db.Column(db.Integer, nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False)
    units = db.Column(db.String(64), nullable=False)

    def __repr__(self):
        return f"""
        DBMetricsMonthly(id={self.id}, consumed_value={self.consumed_value}, grid_consumed_value={self.grid_consumed_value}, 
        other_value={self.other_value}, self_consumed_value={self.self_consumed_value}, thermal_value={self.thermal_value},
        slot_number={self.slot_number}, timestamp={self.timestamp}, units={self.units}, user_id={self.user_id})"""


###############################################################################
########################## Energy Consumption Metrics #########################
###############################################################################

class ForecastVsReal(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String(64), nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False)  # 15 min interval
    forecast = db.Column(db.Float, nullable=True)
    dongle = db.Column(db.Float, nullable=True)
    smart_meter = db.Column(db.Float, nullable=True)
    units = db.Column(db.String(64), nullable=False)  # kW

    def __repr__(self):
        return f"""
        ForecastVsReal(id={self.id}, user_id={self.user_id}, timestamp={self.timestamp}, 
        forecast={self.forecast}, dongle={self.dongle}, smart_meter={self.smart_meter}, 
        units={self.units})"""


###############################################################################
############################### Kafka Debezium ################################
###############################################################################

class DBEvent(db.Model):
    __tablename__ = 'events'

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    aggregatetype = db.Column(
        db.String(255), nullable=False, default=Config.KAFKA_TOPIC_SUFFIX)
    aggregateid = db.Column(db.String(255), nullable=False)
    type = db.Column(db.String(255), nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    payload = db.Column(JSONB, nullable=False)

    def __repr__(self):
        return (
            f"DBEvent('{self.aggregatetype}', '{self.aggregateid}', "
            f"'{self.type}', '{self.timestamp}', '{self.payload}')"
        )


class DBProcessedEvent(db.Model):
    __tablename__ = 'processed_events'

    id = db.Column(db.Integer, primary_key=True)
    event_type = db.Column(db.String(255), nullable=False)
    event_id = db.Column(UUID(as_uuid=True), nullable=False, index=True)

    def __repr__(self):
        return f"DBProcessedEvent('{self.event_type}', '{self.event_id}')"


# Processed Event table #
# class DBProcessedEvent(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     eventType = db.Column(db.String(255), nullable=False)  # Topic name
#     eventId = db.Column(UUID(as_uuid=True), nullable=False, index=True)

#     def __repr__(self):
#         return f"DBProcessedEvent('{self.eventType}', '{self.eventId}')"

# -------------- ACCOUNT MANAGER DATABASE FOR TESTING -------------- #


def id_generator(
    size=Config.USER_ID_SIZE, chars=string.ascii_lowercase + string.digits
):
    return "".join(random.choice(chars) for _ in range(size))


class DBUser(db.Model):
    __tablename__ = "users"
    __bind_key__ = "account_manager"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String(32), unique=True, index=True,
                        nullable=False, default=id_generator)
    meter_id = db.Column(db.String(32), unique=True, index=True)

    first_name = db.Column(db.String(32), nullable=False)
    last_name = db.Column(db.String(32), nullable=True)
    email = db.Column(db.String(64), unique=True, index=True, nullable=False)
    password = db.Column(db.String(128), nullable=True)

    is_active = db.Column(db.Boolean, nullable=False, default=False)
    is_google_account = db.Column(db.Boolean, nullable=False, default=False)
    deleted = db.Column(db.Boolean, nullable=False, default=False)

    api_key = db.Column(db.String(32), nullable=True)  # Dongle API Key
    wp_token = db.Column(db.String(500), nullable=True)  # WP account token
    # Expo notification token
    expo_token = db.Column(db.String(128), nullable=True)

    created_timestamp = db.Column(
        db.DateTime, nullable=False, default=datetime.utcnow)
    modified_timestamp = db.Column(
        db.DateTime, nullable=False, default=datetime.utcnow)

    settings = db.relationship(
        "DBUserSettings", back_populates="user", lazy="joined", uselist=False)

    def __repr__(self):
        return (
            f"DBUser('{self.user_id}', '{self.first_name}', "
            f"'{self.last_name}', '{self.email}', '{self.password}', '{self.is_active}', "
            f"'{self.deleted}', '{self.meter_id}', '{self.api_key}', "
            f"'{self.expo_token}', '{self.wp_token}', '{self.is_google_account}', "
            f"'{self.settings}', '{self.created_timestamp}', '{self.modified_timestamp}')"
        )

    def encode_auth_token(self):
        """
        Generates the Auth Token
        :return: string
        """
        try:
            payload = {
                'exp': datetime.now(timezone.utc) + timedelta(seconds=Config.JWT_EXPIRATION_TIME_SECONDS),
                'iat': datetime.now(timezone.utc),
                'sub': self.user_id,
                'email': self.email,
                'meter_id': self.meter_id
            }
            return jwt.encode(
                payload,
                Config.JWT_SIGN_KEY,
                algorithm=Config.JWT_SIGN_ALGORITHM
            )
        except Exception as e:
            print(e)
            return None

    @ staticmethod
    def decode_auth_token(auth_token):
        """
        Validates the auth token
        :param auth_token:
        :return: string
        """
        try:
            payload = jwt.decode(auth_token, Config.JWT_SIGN_KEY, algorithms=[
                Config.JWT_SIGN_ALGORITHM])
            # is_blacklisted_token = TokenBlacklist.check_blacklist(auth_token)
            # if is_blacklisted_token:
            #     raise Exception('Token blacklisted. Please log in again.')
            # else:
            #     return payload['sub']
            return payload['sub']
        except Exception as e:
            raise


class DBUserSettings(db.Model):
    __tablename__ = "user_settings"
    __bind_key__ = "account_manager"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.ForeignKey("users.user_id"),
                        index=True, nullable=False)

    country = db.Column(db.String(32), nullable=True)
    postal_code = db.Column(db.String(32), nullable=True)

    schedule_type = db.Column(
        db.String(32), nullable=True, default=Config.DEFAULT_SCHEDULE_TYPE)
    tarif_type = db.Column(db.String(32), nullable=True)
    contracted_power = db.Column(db.String(32), nullable=True)

    global_optimizer = db.Column(db.Boolean, nullable=True, default=True)
    permissions = db.Column(db.String(32), nullable=False, default="None")

    modified_timestamp = db.Column(
        db.DateTime, nullable=False, default=datetime.utcnow)

    user = db.relationship("DBUser", back_populates="settings", lazy="joined")
    not_disturb = db.relationship(
        "DBNotDisturbUser", lazy="joined", back_populates="settings")

    def __repr__(self):
        return (
            f"DBUserSettings('{self.country}', '{self.postal_code}', "
            f"'{self.schedule_type}', '{self.tarif_type}', '{self.contracted_power}', "
            f"'{self.not_disturb}', '{self.global_optimizer}', "
            f"'{self.permissions}', '{self.modified_timestamp}')"
        )


class DBNotDisturbUser(db.Model):
    __tablename__ = 'not_disturbs'
    __bind_key__ = 'account_manager'

    id = db.Column(db.Integer, primary_key=True)
    settings_id = db.Column(db.ForeignKey("user_settings.id"),
                            index=True, nullable=False)
    settings = db.relationship(
        "DBUserSettings", back_populates="not_disturb", lazy="joined")
    day_of_week = db.Column(db.String(32), nullable=False)
    start_timestamp = db.Column(db.String(32), nullable=False)
    end_timestamp = db.Column(db.String(32), nullable=False)

    def __repr__(self):
        return f"DBNotDisturb('{self.day_of_week}', '{self.start_timestamp}', '{self.end_timestamp}')"


class DBConfirmationToken(db.Model):
    __tablename__ = "confirmation_tokens"
    __bind_key__ = "account_manager"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String(32), index=True, nullable=False)
    token = db.Column(db.String(64), unique=True, nullable=False)
    expiration_timestamp = db.Column(db.DateTime, nullable=False)

    def __repr__(self):
        return f"DBConfirmationToken('{self.user_id}', '{self.token}', '{self.expiration_timestamp}')"


class DBForgotPasswordToken(db.Model):
    __tablename__ = "forgot_password_tokens"
    __bind_key__ = "account_manager"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String(32), index=True, nullable=False)
    token = db.Column(db.String(64), unique=True, nullable=False)
    expiration_timestamp = db.Column(db.DateTime, nullable=False)

    def __repr__(self):
        return f"DBForgotPasswordToken('{self.user_id}', '{self.token}', '{self.expiration_timestamp}')"


class TokenBlacklist(db.Model):
    __tablename__ = 'token_blacklist'
    __bind_key__ = 'jwt_token_management'

    id = db.Column(db.Integer, primary_key=True)
    token = db.Column(db.String(512), index=True,
                      unique=True, nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False,
                          default=datetime.utcnow)

    def __repr__(self):
        return f"TokenBlacklist('{self.token}', '{self.timestamp}')"


# class DBEventUser(db.Model):
#     __tablename__ = 'events'
#     __bind_key__ = 'account_manager'

#     id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
#     aggregatetype = db.Column(
#         db.String(255), nullable=False, default=Config.KAFKA_TOPIC_SUFFIX)  # Topic name
#     aggregateid = db.Column(db.String(255), nullable=False)
#     type = db.Column(db.String(255), nullable=False)
#     timestamp = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
#     payload = db.Column(JSONB, nullable=False)

#     def __repr__(self):
#         return f"DBEvent('{self.aggregatetype}', '{self.aggregateid}', '{self.type}', '{self.timestamp}', '{self.payload}')"


db.create_all()
