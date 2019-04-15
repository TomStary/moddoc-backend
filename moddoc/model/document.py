import sqlalchemy as sa
import uuid

from moddoc import app
from moddoc.utils import SoftDeleteModel


class Document(app.db.Model, SoftDeleteModel):
    name = sa.Column(sa.String(), unique=True, nullable=False)

    def __init__(self, document_id=None, name=None):
        if document_id is None:
            self.id = uuid.uuid4()
        else:
            self.id = document_id
        self.name = name


class Revision(app.db.Model, SoftDeleteModel):
    name = sa.Column(sa.String(), unique=True, nullable=False)

    def __init__(self, revision_id=None, name=None):
        if revision_id is None:
            self.id = uuid.uuid4()
        else:
            self.id = revision_id
        self.name = name
