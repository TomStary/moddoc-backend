from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity

from moddoc import app
from moddoc.utils import ApiException
from moddoc.dto import DocumentSchema, LinkSchema
from moddoc.model import Document

document = Blueprint('document', __name__, url_prefix='/document')
__documentSchema = DocumentSchema()
__linkSchema = LinkSchema()


@document.route('', methods=['GET'])
@jwt_required
def get_all():
    user = get_jwt_identity()
    result = Document.query.get_by_owner(user)
    data = __documentSchema.dump(result, many=True).data
    return jsonify(data)


@document.route('/<document_id>', methods=['GET'])
def get_by_id(document_id):
    reuslt = Document.query.get_by_id(document_id)
    data = __documentSchema.dump(reuslt).data
    return jsonify(data)


@document.route('', methods=['POST'])
@jwt_required
def post_document():
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
        document, revision = Document.update(data)
        app.db.session.add(revision)
    app.db.session.commit()
    data = __documentSchema.dump(document).data
    return jsonify(data)


@document.route('/link', methods=['POST'])
@jwt_required
def create_link():
    data = request.get_json()
    if data is None:
        raise ApiException(422, "No data.")
    data, error = __linkSchema.load(data)
    if error:
        return jsonify({'error': error}), 422
    document = Document.query.get_by_id(data['document_id'])
    if document is None:
        raise ApiException(400, 'Document with this id does not exists.')
    else:
        document.add_repository(data['repository_id'])
    app.db.session.commit()
    result = __documentSchema.dump(document).data
    return jsonify(result)
