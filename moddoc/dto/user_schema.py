from marshmallow import Schema, fields

from moddoc.dto import not_null_or_empty


class RoleSchema(Schema):
    id = fields.UUID()
    name = fields.Str(required=True, validate=not_null_or_empty)
    flag = fields.Int(dump_only=True)


class UserSchema(Schema):
    id = fields.UUID()
    email = fields.Str()
    username = fields.Str()
    access_token = fields.Str(dump_only=True)
    refresh_token = fields.Str(dump_only=True)
    roles = fields.Nested(RoleSchema, many=True, dump_only=True)


class RoleAssignSchema(Schema):
    users = fields.List(fields.UUID())
    roles = fields.List(fields.UUID())
