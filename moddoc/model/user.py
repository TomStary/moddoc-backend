from moddoc import app
import sqlalchemy as sa
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy.orm import backref
import uuid

from moddoc.utils import SoftDeleteModel, GUID, ApiException, SoftDeleteQuery


class User(app.db.Model, SoftDeleteModel):
    """
    User class

    Stores email and username, connected with Role and token
    """
    email = sa.Column(sa.String(128), nullable=False, unique=True)
    username = sa.Column(sa.String(64), nullable=False, unique=True)
    password = sa.Column(sa.String(255), nullable=False)
    active = sa.Column(sa.Boolean, default=True)
    roles = association_proxy('user_role', 'role')

    def __init__(self,
                 username=None,
                 email=None,
                 password=None,
                 user_id=None):
        if user_id is None:
            self.id = uuid.uuid4()
        self.email = email
        self.username = username
        self.password = app.bcrypt.generate_password_hash(
            password).decode('utf-8')

    def add_role(self, role):
        if role is None:
            raise ApiException(400, "Role has to be specified.")
        role = Role.query.filter_by(name=role, deleted=None).one_or_none()
        if role is None:
            raise ApiException(400, "Role with this name does not exists.")
        self.roles.append(role)

    def add_role_by_id(self, role_id):
        if role_id is None:
            raise ApiException(400, "No role ID.")
        role = Role.query.get_by_id(role_id)
        if role is None:
            raise ApiException(400, "Role with this ID does not exists.")
        self.roles.append(role)

    def update(self, userModel):
        if self.username != userModel['username']:
            user = User.query.filter(User.username == userModel['username'])\
                             .one_or_none()
            if user is None:
                self.username = userModel['username']
            else:
                raise ApiException(400, "Username is already taken.")
        if self.email != userModel['email']:
            user = User.query.filter(User.email == userModel['email'])\
                             .one_or_none()
            if user is None:
                self.email = userModel['email']
            else:
                raise ApiException(400, "Email is already taken.")


class RoleQueryClass(SoftDeleteQuery):
    def get_all(self):
        return self.filter_by(deleted=None).all()

    def get_by_id(self, id):
        return self.filter_by(id=id, deleted=None).one_or_none()

    def get_by_name(self, name):
        return self.filter_by(
            name=name,
            deleted=None
        ).one_or_none()


class Role(app.db.Model, SoftDeleteModel):
    """
    Role class

    Stores name of the role and also if it is default, default roles cannot be
    altered
    """
    query_class = RoleQueryClass
    name = sa.Column(sa.String(128), nullable=False, unique=True)
    flag = sa.Column(sa.Integer, nullable=False, default=0)
    default = sa.Column(sa.Boolean, nullable=False, default=False)

    def __init__(self, name=None, flag=0, default=False, role_id=None):
        if role_id is None:
            self.id = uuid.uuid4()
        self.name = name
        self.flag = flag
        self.default = default

    @staticmethod
    def create(role_model):
        check_name = Role.query.get_by_name(role_model['name'])
        if check_name is None:
            return Role(name=role_model['name'])
        else:
            raise ApiException(400, 'This name is already in use.')

    @staticmethod
    def update(role_model):
        role = Role.query.get_by_id(role_model['id'])
        if role is None:
            raise ApiException(400, 'Role with this ID does not exists')
        check_name = Role.query.get_by_name(role_model['name'])
        if check_name is None or check_name.id == role.id:
            role.name = role_model['name']
            return role
        else:
            raise ApiException(400,
                               'This name is already in use.')


class UserToRole(app.db.Model, SoftDeleteModel):
    """
    User to Role connection

    Stores connection between roles and users
    """

    user_id = sa.Column(GUID(), sa.ForeignKey(User.id))
    role_id = sa.Column(GUID(), sa.ForeignKey(Role.id))
    user = sa.orm.relationship(User, backref=backref("user_role"))
    role = sa.orm.relationship(Role)

    def __init__(self, role=None, user=None):
        self.id = uuid.uuid4()
        self.role = role
        self.user = user
