from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity

from moddoc import app
from moddoc.model import Document, User, DocumentPermission, Repository, RepositoryPermission  # noqa 501
from moddoc.utils import ApiException
from moddoc.dto import PermissionSchema

permission = Blueprint('permission', __name__, url_prefix='/permission')
__permissionSchema = PermissionSchema()


@permission.route('/document/<document_id>', methods=['POST'])
@jwt_required
def assign_permission_document(document_id):
    user = get_jwt_identity()
    data = request.get_json()
    document = Document.query.get_by_id(document_id, user)
    if data is None:
        raise ApiException(422, 'No data.')
    if document is None:
        raise ApiException(400, 'No document with this id exists.')
    if str(document.owner_id) != user['id']:
        raise ApiException(400, 'You do not have permission for this action.')
    data, errors = __permissionSchema.load(data)
    if errors:
        return jsonify({'error': errors}), 422
    for user_id in data['users']:
        puser = User.query.soft_get(user_id)
        document.grant_permission(puser, data['write'])
    app.db.session.commit()
    return jsonify()


@permission.route('/document/<document_id>/<user_id>', methods=['DELETE'])
@jwt_required
def unassign_permission_document(document_id, user_id):
    """Remove permission for user from document"""
    user = get_jwt_identity()
    document = Document.query.get_by_id(document_id, user)
    if document is None:
        raise ApiException(400, 'No document with this id exists.')
    if str(document.owner_id) != user['id']:
        raise ApiException(400, 'You do not have permission for this action.')
    permission = DocumentPermission.query\
        .filter_by(document_id=document_id, user_id=user_id, deleted=None)\
        .one_or_none()
    if permission is None:
        raise ApiException(400, "This permission does not exists.")
    permission.delete()
    app.db.session.add()
    return jsonify()


@permission.route('/repostory/<repository_id>', methods=['POST'])
@jwt_required
def assign_permission_repository(repository_id):
    user = get_jwt_identity()
    data = request.get_json()
    repository = Repository.query.get_by_id(repository_id, user)
    if data is None:
        raise ApiException(422, 'No data.')
    if repository is None:
        raise ApiException(400, 'No repository with this id exists.')
    if str(repository.owner_id) != user['id']:
        raise ApiException(400, 'You do not have permission for this action.')
    data, errors = __permissionSchema.load(data)
    if errors:
        return jsonify({'error': errors}), 422
    for user_id in data['users']:
        puser = User.query.soft_get(user_id)
        repository.grant_permission(puser, data['write'])
    app.db.session.commit()
    return jsonify()


@permission.route('/repository/<repository_id>/<user_id>', methods=['DELETE'])
@jwt_required
def unassign_permission_repository(repository_id, user_id):
    """Remove permission for user from document"""
    user = get_jwt_identity()
    repository = Document.query.get_by_id(repository_id, user)
    if repository is None:
        raise ApiException(400, 'No document with this id exists.')
    if str(repository.owner_id) != user['id']:
        raise ApiException(400, 'You do not have permission for this action.')
    permission = RepositoryPermission.query\
        .filter_by(repository_id=repository_id, user_id=user_id, deleted=None)\
        .one_or_none()
    if permission is None:
        raise ApiException(400, "This permission does not exists.")
    permission.delete()
    app.db.session.add()
    return jsonify()
