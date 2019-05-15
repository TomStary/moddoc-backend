from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity

from moddoc import app
from moddoc.dto import RepositorySchema
from moddoc.model import Repository
from moddoc.utils import ApiException

repository = Blueprint('repository', __name__, url_prefix='/repository')
__repositorySchema = RepositorySchema()


@repository.route('', methods=['GET'])
@jwt_required
def get_all():
    """Return all repositories"""
    user = get_jwt_identity()
    result = Repository.query.get_by_user(user)
    data = __repositorySchema.dump(result, many=True).data
    return jsonify(data)


@repository.route('/<repository_id>', methods=['GET'])
@jwt_required
def get_repository(repository_id):
    """Return repository"""
    user = get_jwt_identity()
    result = Repository.query.get_by_id(repository_id, user)
    data = __repositorySchema.dump(result).data
    return jsonify(data)


@repository.route('', methods=['POST'])
@jwt_required
def create_or_update_repository():
    """Create or update repository"""
    user = get_jwt_identity()
    data = request.get_json()
    if data is None:
        raise ApiException(422, "No data.")
    data, errors = __repositorySchema.load(data)
    if errors:
        return jsonify({'error': errors}), 422
    if 'id' not in data or data['id'] is None:
        data['owner_id'] = user['id']
        repository = Repository.create(data)
        app.db.session.add(repository)
    else:
        repository = Repository.query.get_by_id(data['id'], user)
        repository.update(data)
    app.db.session.commit()
    data = __repositorySchema.dump(repository).data
    return jsonify(data)


@repository.route('/<repository_id>', methods=['DELETE'])
@jwt_required
def delete_repository(repository_id):
    """Delete repository, only if user is owner of this repository"""
    user = get_jwt_identity()
    repository = Repository.query.get_by_id(repository_id, user)
    if repository is None:
        raise ApiException(400, "No module with this id was found.")
    if str(repository.owner_id) != user['id']:
        raise ApiException(400, "Not enough permissions for this action.")
    repository.delete()
    app.db.session.commit()
    return jsonify()
