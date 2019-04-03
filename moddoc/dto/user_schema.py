from marshmallow import Schema, fields


class RoleSchema(Schema):
    name = fields.Str()


class UserSchema(Schema):
    email = fields.Str()
    username = fields.Str()
    token = fields.Str(dump_only=True)
    roles = fields.Nested(RoleSchema, many=True)
