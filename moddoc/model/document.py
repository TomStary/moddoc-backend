import sqlalchemy as sa
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy.orm import backref
import uuid
from datetime import datetime

from moddoc import app
from moddoc.utils import SoftDeleteModel, GUID, ApiException, SoftDeleteQuery


class DocumentQueryClass(SoftDeleteQuery):
    def get_by_id(self, document_id):
        return self.filter_by(id=document_id, deleted=None).one_or_none()

    def get_by_name(self, name):
        return self.filter_by(name=name, deleted=None).one_or_none()

    def get_by_owner(self, user):
        return self.filter_by(owner_id=user['id'], deleted=None).all()


class Document(app.db.Model, SoftDeleteModel):
    query_class = DocumentQueryClass
    name = sa.Column(sa.String(), nullable=False)
    body = sa.Column(sa.String())
    owner_id = sa.Column(GUID, sa.ForeignKey('user.id'))
    owner = sa.orm.relationship('User', backref='documents')
    repositories = association_proxy('document_repository', 'repository')

    def __init__(self, document_model):
        if 'id' not in document_model or document_model['id'] is None:
            self.id = uuid.uuid4()
        else:
            self.id = document_model['id']
        self.name = document_model['name']
        self.body = document_model['body']
        self.owner_id = document_model['owner_id']

    def add_repository(self, repository_id):
        from moddoc.model import Repository
        repository = Repository.query.get_by_id(repository_id)
        if repository is None:
            raise ApiException(400, "Repository with this id does not exists.")
        self.repositories.append(repository)
        return self

    @staticmethod
    def create(document_model):
        checkName = Document.query.filter_by(
            name=document_model['name'],
            deleted=None
        ).one_or_none()
        if checkName is None:
            document = Document(document_model)
            revision = Revision.create_revision(document)
            return document, revision
        else:
            raise ApiException(400,
                               'Document with this name already exists.')

    @staticmethod
    def update(document_model):
        document = Document.query.get_by_id(document_model['id'])
        if document is None:
            raise ApiException(400, "No document with this ID exists.")
        checkName = Document.query.get_by_name(document_model['name'])
        if checkName is None or checkName.id == document.id:
            document.name = document_model['name']
            document.body = document_model['body']
            revision = Revision.create_revision(document)
            return document, revision
        else:
            raise ApiException(400,
                               'Document with this name already exists.')


class LinkedRepositories(app.db.Model, SoftDeleteModel):
    repository_id = sa.Column(GUID(), sa.ForeignKey('repository.id'),
                              primary_key=True)
    document_id = sa.Column(GUID(), sa.ForeignKey(Document.id),
                            primary_key=True)
    document = sa.orm.relationship(Document,
                                   backref=backref('document_repository'))
    repository = sa.orm.relationship('Repository')

    def __init__(self, repository=None, document=None):
        self.id = uuid.uuid4()
        self.document = document
        self.repository = repository


class Revision(app.db.Model, SoftDeleteModel):
    name = sa.Column(sa.String(), nullable=False)
    body = sa.Column(sa.String())
    revision_date = sa.Column(sa.DateTime, default=datetime.utcnow)
    document_id = sa.Column(GUID(), sa.ForeignKey('document.id'))
    document = sa.orm.relationship('Document', backref='revisions')

    def __init__(self,
                 revision_id=None,
                 name=None,
                 body=None,
                 document_id=None):
        if revision_id is None:
            self.id = uuid.uuid4()
        else:
            self.id = revision_id
        self.name = name
        self.body = body
        self.document_id = document_id

    @staticmethod
    def create_revision(document):
        revision = Revision(None,
                            document.name,
                            document.body,
                            document.id)
        return revision
