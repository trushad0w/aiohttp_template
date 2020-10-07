from marshmallow import (
    Schema,
    fields,
)


class PaginationSchema(Schema):
    offset = fields.Int(required=True)
    limit = fields.Int(required=True)
    total = fields.Int(required=False)


class ErrorSchema(Schema):
    code = fields.Str(required=True)
    message = fields.Str(required=False)
    field_name = fields.Str(required=False)
    meta = fields.Dict(required=False)
