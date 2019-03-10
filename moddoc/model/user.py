from moddoc import app
from moddoc.utils import SoftDeleteModel
import sqlalchemy as sa


class User(app.db.Model, SoftDeleteModel):
    """
    User class

    Stores email and username, connected with Role and token
    """
    email = sa.Column(sa.String(128), nullable=False, unique=True)
    username = sa.Column(sa.String(64), nullable=False, unique=True)
    password = sa.Column(sa.String(128), nullable=False)
    active = sa.Column(sa.Boolean, default=True)

    def __init__(self, email=None, username=None, password=None):
        self.email = email
        self.username = username
        self.password = password


class UserToken(app.db.Model, SoftDeleteModel):
    """
    User Token class

    Stores all used token by user
    """
    token = sa.Column(sa.String(128), nullable=False, unique=True)

    def __init__(self, token=None):
        self.token = token


class Role(app.db.Model, SoftDeleteModel):
    """
    Role class

    Stores name of the role and also if it is default, default roles cannot be
    altered
    """
    name = sa.Column(sa.String(128), nullable=False, unique=True)
    default = sa.Column(sa.Boolean, nullable=False, default=False)

    def __init__(self, name=None):
        self.name = name
