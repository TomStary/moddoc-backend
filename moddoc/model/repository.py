import sqlalchemy as sa
import uuid

from moddoc import app
from moddoc.utils import GUID, SoftDeleteModel, SoftDeleteQuery


class RepositoryQueryClass(SoftDeleteQuery):
    def get_by_owner(self, user):
        return self.filter_by(owner_id=user['id'], deleted=None).all()

    def get_by_id(self, repository_id):
        return self.filter_by(id=repository_id, deleted=None).one_or_none()


class Repository(app.db.Model, SoftDeleteModel):
    query_class = RepositoryQueryClass
    name = sa.Column(sa.String(64), unique=True, nullable=False)
    owner_id = sa.Column(GUID, sa.ForeignKey('user.id'))
    owner = sa.orm.relationship("User", backref="repositories")

    def __init__(self, repository_id=None, name=None, owner_id=None):
        if repository_id is None:
            self.id = uuid.uuid4()
        else:
            self.id = repository_id
        self.name = name
        self.owner_id = owner_id


class Module(app.db.Model, SoftDeleteModel):
    name = sa.Column(sa.String(64), unique=True, nullable=False)
    body = sa.Column(sa.String(), nullable=False)

    def __init__(self, module_id=None, name=None, body=None):
        if module_id is None:
            self.id = uuid.uuid4()
        else:
            self.id = module_id
        self.name = name
        self.body = body


class ModuleHistory(app.db.Model, SoftDeleteModel):
    body = sa.Column(sa.String(), nullable=False)

    def __init__(self, history_id=None, body=None):
        if history_id is None:
            self.id = uuid.uuid4()
        else:
            self.id = history_id
        self.body = body
