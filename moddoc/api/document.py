from flask import Blueprint, jsonify, request, send_file
from flask_jwt_extended import jwt_required, get_jwt_identity

from moddoc import app
from moddoc.utils import ApiException
from moddoc.dto import DocumentSchema, LinkSchema
from moddoc.model import Document, LinkedRepositories

document = Blueprint('document', __name__, url_prefix='/document')
__documentSchema = DocumentSchema()
__linkSchema = LinkSchema()


@document.route('', methods=['GET'])
@jwt_required
def get_all():
    """
    Return all documents which User can access.
    """
    user = get_jwt_identity()
    result = Document.query.get_by_user(user)
    data = __documentSchema.dump(result, many=True).data
    return jsonify(data)


@document.route('/<document_id>', methods=['GET'])
@jwt_required
def get_by_id(document_id):
    """Return document by its id."""
    user = get_jwt_identity()
    reuslt = Document.query.get_by_id(document_id, user)
    data = __documentSchema.dump(reuslt).data
    return jsonify(data)


@document.route('', methods=['POST'])
@jwt_required
def post_document():
    """Create or update document."""
    user = get_jwt_identity()
    data = request.get_json()
    if data is None:
        raise ApiException(422, 'No data.')
    data, errors = __documentSchema.load(data)
    if errors:
        return jsonify({'error': errors}), 422
    if 'id' not in data or data['id'] is None:
        data['owner_id'] = user['id']
        document, revision = Document.create(data)
        app.db.session.add(document)
        app.db.session.add(revision)
    else:
        document, revision = Document.update(data, user)
        app.db.session.add(revision)
    app.db.session.commit()
    data = __documentSchema.dump(document).data
    return jsonify(data)


@document.route('/<document_id>', methods=['DELETE'])
@jwt_required
def delete_document(document_id):
    """Delete document, document can be deleted only by its owner"""
    user = get_jwt_identity()
    document = Document.query.get_by_id(document_id, user)
    if document is None:
        raise ApiException(400, 'Document with this id does not exists.')
    elif str(document.owner_id) != user['id']:
        raise ApiException(400, 'You do not have permission for this action.')
    else:
        document.delete()
    app.db.session.commit()
    return jsonify()


@document.route('/link/<document_id>', methods=['GET'])
@jwt_required
def get_links(document_id):
    """Return all links to given document"""
    links = LinkedRepositories.query\
        .filter_by(deleted=None, document_id=document_id)\
        .all()
    result = __linkSchema.dump(links, many=True).data
    return jsonify(result)


@document.route('/link', methods=['POST'])
@jwt_required
def create_link():
    """Create link between repository and document. This is used to
    declare which repositories are used in document."""
    user = get_jwt_identity()
    data = request.get_json()
    if data is None:
        raise ApiException(422, "No data.")
    data, error = __linkSchema.load(data)
    if error:
        return jsonify({'error': error}), 422
    document = Document.query.get_by_id(data['document_id'], user)
    if document is None:
        raise ApiException(400, 'Document with this id does not exists.')
    else:
        document.add_repository(data['repository_id'])
    app.db.session.commit()
    result = __documentSchema.dump(document).data
    return jsonify(result)


@document.route('/link/<link_id>', methods=['DELETE'])
@jwt_required
def remove_link(link_id):
    """Remove once created link between repository and document."""
    link = LinkedRepositories.query.soft_get(link_id, None)
    if None:
        raise ApiException(400, "Link could not be removed, because it does not exists")  # noqa 501
    else:
        link.delete()
    app.db.session.commit()
    return jsonify()


@document.route('/build/<document_id>', methods=['GET'])
@jwt_required
def build_document(document_id):
    """
    Creates document for given document id.
    """
    user = get_jwt_identity()
    document = Document.query.get_by_id(document_id, user)
    if document is None:
        raise ApiException(400, 'Document with this id does not exists.')
    generated = document.build()
    return send_file(generated, mimetype='application/pdf')
