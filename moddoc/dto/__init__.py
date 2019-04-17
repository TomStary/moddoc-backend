from marshmallow import Schema, ValidationError, fields


def not_null_or_empty(data):
    if not data:
        raise ValidationError('Data cannot be blank.')


class Error(Schema):
    message = fields.Str()


from moddoc.dto.auth_schema import LoginSchema, RegistrationSchema  # noqa 402
from moddoc.dto.user_schema import UserSchema  # noqa 402
from moddoc.dto.repository_schema import RepositorySchema  # noqa 402
# FIXME: override default error for missing data


__all__ = [
    'Error',
    'ErrorMessage',
    'LoginSchema',
    'RegistrationSchema',
    'UserSchema',
    'RepositorySchema',
    'not_null_or_empty',
]
