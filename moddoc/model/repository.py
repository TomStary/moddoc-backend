import sqlalchemy as sa
import uuid

from moddoc import app
from moddoc.utils import GUID, SoftDeleteModel, SoftDeleteQuery, ApiException


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

    @staticmethod
    def create(repository_model):
        repository = Repository.query.filter(
            Repository.name == repository_model['name']).one_or_none()
        if repository is None:
            return Repository(name=repository_model['name'],
                              owner_id=repository_model['owner_id'])
        else:
            raise ApiException(400,
                               'This name of repository is already taken.')

    def update(self, repository_model):
        reposiotory = Repository.query.filter(
            Repository.name == repository_model['name']).one_or_none()
        if reposiotory is None:
            self.name = repository_model['name']
        else:
            raise ApiException(400,
                               'This name of repository is already taken.')


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
