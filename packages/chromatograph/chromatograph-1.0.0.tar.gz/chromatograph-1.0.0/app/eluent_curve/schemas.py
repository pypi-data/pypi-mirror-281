from marshmallow import Schema, fields

class curvePoint(Schema):
    time = fields.Str()
    value = fields.Float()

class curveInPut(Schema):
    start_time = fields.Str()
class curveOutPut(Schema):
    message = fields.Str()
    point = fields.Nested(curvePoint,required=True)

class verticalePoint(Schema):
    timeStart = fields.Str()
    timeEnd = fields.Str()
    tube = fields.Float()

class verticalOutPut(Schema):
    message = fields.Str()
    point = fields.Nested(verticalePoint,required=True)

class lineOutPut(Schema):
    message = fields.Str()
    point = fields.List(fields.Nested(curvePoint), required=True)