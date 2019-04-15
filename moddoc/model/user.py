from moddoc import app
from moddoc.utils import SoftDeleteModel, GUID, ApiException
import sqlalchemy as sa
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy.orm import backref
import uuid


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
                 user_id=None,
                 roles=[]):
        if user_id is None:
            self.id = uuid.uuid4()
        self.email = email
        self.username = username
        self.password = app.bcrypt.generate_password_hash(
            password).decode('utf-8')
        for role in roles:
            self.add_role(role)

    def add_role(self, role):
        if role is None:
            raise ApiException(400, "Role has to be specified.")
        role = Role.query.filter_by(name=role, deleted=None).one_or_none()
        if role is None:
            raise ApiException(400, "Role with this name does not exists.")
        self.roles.append(role)

    def update(self, userModel):
        if self.username != userModel.username:
            user = User.query.filter(User.username == userModel.username,
                                     User.deleted is None)\
                             .one_or_none()
            if user is None:
                self.username = userModel.username
            else:
                raise ApiException(400, "Username is already taken.")
        if self.email != userModel.email:
            user = User.query.filter(User.email == userModel.email,
                                     User.deleted is None)\
                             .one_or_none()
            if user is None:
                self.email = userModel.email
            else:
                raise ApiException(400, "Email is already taken.")


class Role(app.db.Model, SoftDeleteModel):
    """
    Role class

    Stores name of the role and also if it is default, default roles cannot be
    altered
    """
    name = sa.Column(sa.String(128), nullable=False, unique=True)
    flag = sa.Column(sa.Integer, nullable=False, default=0)
    default = sa.Column(sa.Boolean, nullable=False, default=False)

    def __init__(self, name=None, flag=0, default=False, role_id=None):
        if role_id is None:
            self.id = uuid.uuid4()
        self.name = name
        self.flag = flag
        self.default = default


class UserToRole(app.db.Model, SoftDeleteModel):
    """
    User to Role connection

    Stores connection between roles and users
    """

    user_id = sa.Column(GUID(), sa.ForeignKey(User.id), primary_key=True)
    role_id = sa.Column(GUID(), sa.ForeignKey(Role.id), primary_key=True)
    user = sa.orm.relationship(User, backref=backref("user_role"))
    role = sa.orm.relationship(Role)

    def __init__(self, user=None, role=None):
        self.id = uuid.uuid4()
        self.role = role
        self.user = user
