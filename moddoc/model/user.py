from flask_login import UserMixin
from moddoc import app
from moddoc.utils import SoftDeleteModel
import sqlalchemy as sa
import uuid


class User(app.db.Model, SoftDeleteModel, UserMixin):
    """
    User class

    Stores email and username, connected with Role and token
    """
    email = sa.Column(sa.String(128), nullable=False, unique=True)
    username = sa.Column(sa.String(64), nullable=False, unique=True)
    password = sa.Column(sa.String(255), nullable=False)
    active = sa.Column(sa.Boolean, default=True)

    def __init__(self, email=None, username=None, password=None, user_id=None):
        if user_id is None:
            self.id = uuid.uuid4()
        self.email = email
        self.username = username
        self.password = app.bcrypt.generate_password_hash(password).decode('utf-8')


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
