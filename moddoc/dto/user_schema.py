from marshmallow import Schema, fields, pre_dump


class RoleSchema(Schema):
    name = fields.Str()
    flag = fields.Int()


class UserSchema(Schema):
    id = fields.UUID()
    email = fields.Str()
    username = fields.Str()
    access_token = fields.Str(dump_only=True)
    refresh_token = fields.Str(dump_only=True)
    roles = fields.Nested(RoleSchema, many=True, dump_only=True)
