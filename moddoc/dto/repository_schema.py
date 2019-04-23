from marshmallow import Schema, fields

from moddoc.dto import not_null_or_empty, UserSchema


class RepositorySchema(Schema):
    id = fields.UUID()
    name = fields.Str(required=True, validate=not_null_or_empty)
    owner_id = fields.UUID(load_only=True)
    owner = fields.Nested(UserSchema, dump_only=True)


class ModuleSchema(Schema):
    id = fields.UUID()
    name = fields.Str(required=True, validate=not_null_or_empty)
    body = fields.Str(required=True)
    repository_id = fields.UUID(load_only=True)
    repository = fields.Nested(RepositorySchema, dump_only=True)
