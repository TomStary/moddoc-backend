from marshmallow import Schema, ValidationError, fields


def not_null_or_empty(data):
    if not data:
        raise ValidationError('Data cannot be blank.')


class Error(Schema):
    message = fields.Str()


from moddoc.dto.auth_schema import LoginSchema, RegistrationSchema  # noqa 402
from moddoc.dto.user_schema import UserSchema  # noqa 402
from moddoc.dto.repository_schema import RepositorySchema, ModuleSchema  # noqa 402
from moddoc.dto.document_schema import DocumentSchema, LinkSchema  # noqa 402

__all__ = [
    'Error',
    'ErrorMessage',
    'LoginSchema',
    'RegistrationSchema',
    'UserSchema',
    'RepositorySchema',
    'ModuleSchema',
    'DocumentSchema',
    'LinkSchema',
    'not_null_or_empty',
]
