from datetime import datetime
from flask_sqlalchemy import Model, BaseQuery
import sqlalchemy as sa
from sqlalchemy.types import TypeDecorator, CHAR
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declared_attr
import uuid


class ApiException(Exception):
    def __init__(self, errorCode=400, message=None):
        self.errorCode = errorCode
        self.message = message


# FIXME: add source
class GUID(TypeDecorator):
    """Platform-independent GUID type.

    Uses PostgreSQL's UUID type, otherwise uses
    CHAR(32), storing as stringified hex values.

    """
    impl = CHAR

    def load_dialect_impl(self, dialect):
        if dialect.name == 'postgresql':
            return dialect.type_descriptor(UUID())
        else:
            return dialect.type_descriptor(CHAR(32))

    def process_bind_param(self, value, dialect):
        if value is None:
            return value
        elif dialect.name == 'postgresql':
            return str(value)
        else:
            if not isinstance(value, uuid.UUID):
                return "%.32x" % uuid.UUID(value).int
            else:
                # hexstring
                return "%.32x" % value.int

    def process_result_value(self, value, dialect):
        if value is None:
            return value
        else:
            if not isinstance(value, uuid.UUID):
                value = uuid.UUID(value)
            return value


class IdModel(Model):
    # FIXME add source: http://flask-sqlalchemy.pocoo.org/2.3/customizing/#model-class  # noqa 501
    @declared_attr
    def id(cls):
        for base in cls.__mro__[1:-1]:
            if getattr(base, '__table__', None) is not None:
                type = sa.ForeignKey(base.id)
                break
        else:
            type = GUID()

        return sa.Column(type, primary_key=True)


class SoftDeleteModel(object):
    created = sa.Column(sa.DateTime, nullable=False, default=datetime.utcnow)
    updated = sa.Column(sa.DateTime, nullable=True, default=None)
    deleted = sa.Column(sa.DateTime, nullable=True, default=None)


class SoftDeleteQuery(BaseQuery):
    def soft_get(self, id, default=None):
        object = self.get(id)
        if object and object.deleted is None:
            return object
        else:
            return default

    def soft_all(self):
        return self.filter_by(deleted=None).all()
