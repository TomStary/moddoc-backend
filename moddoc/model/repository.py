from sqlalchemy.orm import backref
from sqlalchemy.ext.associationproxy import association_proxy
from datetime import datetime
import sqlalchemy as sa
from sqlalchemy import or_, and_
import uuid

from moddoc import app
from moddoc.utils import GUID, SoftDeleteModel, SoftDeleteQuery, ApiException


class RepositoryQueryClass(SoftDeleteQuery):
    def get_by_owner(self, user):
        return self.filter_by(owner_id=user['id'], deleted=None).all()

    def get_by_user(self, user):
        return self.filter(or_(Repository.owner_id == user['id'],
                               Repository.permissions.any(id=user['id'],deleted=None))).all()  # noqa 501

    def get_by_id(self, repository_id, user):
        return self.filter(and_(Repository.id == repository_id,
                                Repository.deleted.is_(None),
                                or_(Repository.owner_id == user['id'],
                                    Repository.permissions.any(id=user['id'], deleted=None)))).one_or_none()  # noqa 501


class Repository(app.db.Model, SoftDeleteModel):
    query_class = RepositoryQueryClass
    name = sa.Column(sa.String(64), unique=True, nullable=False)
    owner_id = sa.Column(GUID, sa.ForeignKey('user.id'))
    owner = sa.orm.relationship('User', backref='repositories')
    permissions = association_proxy('permission', 'user')

    def __init__(self, repository_id=None, name=None, owner_id=None):
        if repository_id is None:
            self.id = uuid.uuid4()
        else:
            self.id = repository_id
        self.name = name
        self.owner_id = owner_id

    def grant_permission(self, user, write):
        permission = RepositoryPermission(self, user, write)
        app.db.session.add(permission)

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


class RepositoryPermission(app.db.Model, SoftDeleteModel):
    repository_id = sa.Column(GUID(), sa.ForeignKey('repository.id'))
    user_id = sa.Column(GUID(), sa.ForeignKey('user.id'))
    write = sa.Column(sa.Boolean, nullable=False, default=False)

    repository = sa.orm.relationship(Repository,
                                     backref=backref('permission'))
    user = sa.orm.relationship('User')

    def __init__(self,
                 repository=None,
                 user=None,
                 write=None):
        self.repository = repository
        self.user = user
        self.write = write


class ModuleQuery(SoftDeleteQuery):
    def get_by_user(self, user):
        return self.filter(Module.repository.owner_id == user['id'],
                           Module.deleted is None).all()

    def get_by_repository(self, repository_id):
        return self.filter_by(repository_id=repository_id,
                              deleted=None).all()

    def get_by_id(self, module_id):
        return self.filter_by(deleted=None,
                              id=module_id)\
                   .one_or_none()

    def get_by_name(self, name, repository_id):
        return self.filter_by(deleted=None,
                              name=name,
                              repository_id=repository_id)\
                   .one_or_none()


class Module(app.db.Model, SoftDeleteModel):
    query_class = ModuleQuery
    name = sa.Column(sa.String(64), nullable=False)
    body = sa.Column(sa.String(), nullable=False)
    repository_id = sa.Column(GUID, sa.ForeignKey('repository.id'))
    repository = sa.orm.relationship('Repository', backref='modules')

    def __init__(self, module_id=None, name=None, body=None,
                 repository_id=None):
        if module_id is None:
            self.id = uuid.uuid4()
        else:
            self.id = module_id
        self.name = name
        self.body = body
        self.repository_id = repository_id

    @staticmethod
    def create(module_data):
        check_name = Module.query.get_by_name(module_data['name'],
                                              module_data['repository_id'])
        if check_name is None:
            module = Module(name=module_data['name'], body=module_data['body'],
                            repository_id=module_data['repository_id'])
            history = ModuleHistory.create_history(module)
            return module, history
        else:
            raise ApiException(400,
                               'Module with this name is already present in this repository')  # noqa 501

    @staticmethod
    def update(module_data, user):
        module = Module.query.get_by_id(module_data['id'], user)
        if module is None:
            raise ApiException(400, 'Module with id does not exists.')
        check_name = Module.query.get_by_name(module_data['name'],
                                              module.repository_id)
        if check_name is None or check_name.id == module.id:
            module.name = module_data['name']
            module.body = module_data['body']
            history = ModuleHistory.create_history(module)
            return module, history
        else:
            raise ApiException(400,
                               'Module with this name is already present in this repository')  # noqa 501


class ModuleHistory(app.db.Model, SoftDeleteModel):
    body = sa.Column(sa.String(), nullable=False)
    name = sa.Column(sa.String())
    history_data = sa.Column(sa.DateTime, default=datetime.utcnow)
    module_id = sa.Column(GUID(), sa.ForeignKey('module.id'))
    module = sa.orm.relationship('Module', backref='history')

    def __init__(self,
                 history_id=None,
                 body=None,
                 name=None,
                 module_id=None):
        if history_id is None:
            self.id = uuid.uuid4()
        else:
            self.id = history_id
        self.body = body
        self.name = name
        self.module_id = module_id

    @staticmethod
    def create_history(module):
        history = ModuleHistory(None,
                                module.body,
                                module.name,
                                module.id)
        return history
