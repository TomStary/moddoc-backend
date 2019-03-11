from marshmallow import Schema, fields
from moddoc.dto import not_null_or_empty


class LoginSchema(Schema):
    username = fields.Str(required=True, validate=not_null_or_empty)
    password = fields.Str(required=True, validate=not_null_or_empty)


class RegistrationSchema(Schema):
    username = fields.Str(required=True, validate=not_null_or_empty)
    email = fields.Email(required=True)
    password = fields.Str(required=True, validate=not_null_or_empty)
