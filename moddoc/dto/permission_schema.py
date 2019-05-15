from marshmallow import Schema, fields


class PermissionSchema(Schema):
    users = fields.List(fields.UUID())
    write = fields.Boolean(required=True, default=False)
