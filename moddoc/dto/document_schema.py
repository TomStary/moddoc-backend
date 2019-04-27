from marshmallow import Schema, fields

from moddoc.dto import not_null_or_empty, UserSchema, RepositorySchema


class RevisionSchema(Schema):
    id = fields.UUID()
    name = fields.Str(required=True, validate=not_null_or_empty)
    body = fields.Str()
    revision_date = fields.DateTime()


class DocumentSchema(Schema):
    id = fields.UUID()
    name = fields.Str(required=True, validate=not_null_or_empty)
    body = fields.Str()
    owner_id = fields.UUID(load_only=True)
    owner = fields.Nested(UserSchema, dump_only=True)
    revisions = fields.Nested(RevisionSchema, many=True, dump_only=True)
    repositories = fields.Nested(RepositorySchema, many=True)


class LinkSchema(Schema):
    repository_id = fields.UUID(required=True)
    document_id = fields.UUID(required=True)
