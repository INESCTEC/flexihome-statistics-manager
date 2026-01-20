from marshmallow import Schema, fields, validate


ForecastComputedEvent = "ForecastComputedEvent"
ComputeMockConsumptionCurveEvent = "ComputeMockConsumptionCurveEvent"
GetUserRealDataEvent = "GetUserRealDataEvent"


class MetricsSchema(Schema):
    id = fields.Integer(load_only=True)
    consumed_value = fields.Float(required=True, validate=validate.Range(min=0.0))
    grid_consumed_value = fields.Float(required=True, validate=validate.Range(min=0.0))
    other_value = fields.Float(required=True, validate=validate.Range(min=0.0))
    self_consumed_value = fields.Float(required=True, validate=validate.Range(min=0.0))
    thermal_value = fields.Float(required=True, validate=validate.Range(min=0.0))
    slot_number = fields.Integer(required=True, validate=validate.Range(min=1))
    timestamp = fields.DateTime(required=True, format="%Y-%m-%d %H:%M:%S")
    units = fields.String(required=True, validate=validate.Length(min=1))

class UserStatisticsSchema(Schema):
    id = fields.Integer(load_only=True)
    user_id = fields.Integer(required=True, validate=validate.Length(min=10, max=10))
    group_by = fields.String(required=True, validate=validate.Length(min=1)) # enum
    metrics = fields.List(fields.Nested(MetricsSchema, required=True))


class ForecastComputedSchema(Schema):
    # user_ids_computed = fields.List(fields.String(required=False, validate=validate.Length(min=10, max=10)))
    user_id = fields.String(required=False, validate=validate.Length(min=10, max=10))
    forecast_date = fields.Date(format="%Y-%m-%d", required=True)


class MockConsumptionCurveSchema(Schema):
    user_id = fields.String(required=False, validate=validate.Length(min=10, max=10))
    start_date = fields.Date(format="%Y-%m-%d", required=True)
    delivery_time = fields.Integer(required=True, validate=validate.Range(min=15))
    contracted_power = fields.Float(required=True)


class GetUserRealDataSchema(Schema):
    user_id = fields.String(required=False, validate=validate.Length(min=10, max=10))
    start_date = fields.DateTime(format="%Y-%m-%d %H:%M:%S", required=True)
    end_date = fields.DateTime(format="%Y-%m-%d %H:%M:%S", required=True)
