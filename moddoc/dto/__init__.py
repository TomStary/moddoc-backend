from marshmallow import Schema, ValidationError, fields


def not_null_or_empty(data):
    if not data:
        raise ValidationError('Data cannot be blank.')


class Error(Schema):
    message = fields.Str()


from moddoc.dto.auth_schema import LoginSchema, RegistrationSchema


__all__ = [
    'Error',
    'LoginSchema',
    'RegistrationSchema',
    'not_null_or_empty',
]