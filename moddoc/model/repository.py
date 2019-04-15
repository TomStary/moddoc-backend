import sqlalchemy as sa
import uuid

from moddoc import app
from moddoc.utils import SoftDeleteModel


class Repository(app.db.Model, SoftDeleteModel):
    name = sa.Column(sa.String(64), unique=True, nullable=False)

    def __init__(self, repository_id=None, name=None):
        if repository_id is None:
            self.id = uuid.uuid4()
        else:
            self.id = repository_id
        self.name = name


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
