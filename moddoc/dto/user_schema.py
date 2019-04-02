from marshmallow import Schema, fields


class UserSchema(Schema):
    email = fields.Str()
    username = fields.Str()
    token = fields.Str(dump_only=True)


class UsersSchema(Schema):
    users = fields.List(fields.Nested(UserSchema))
