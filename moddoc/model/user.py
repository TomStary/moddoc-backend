from moddoc import app
from moddoc.utils import SoftDeleteModel
import sqlalchemy as sa


class User(app.db.Model, SoftDeleteModel):
    email = sa.Column(sa.String(128), nullable=False, unique=True)
    username = sa.Column(sa.String(64), nullable=False, unique=True)

    def __init__(self, email=None, username=None):
        self.email = email
        self.username = username
