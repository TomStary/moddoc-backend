from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity

from moddoc import app
from moddoc.dto import RepositorySchema
from moddoc.model import Repository
from moddoc.utils import ApiException

repository = Blueprint('repository', __name__, url_prefix='/repository')
__repositoryScheme = RepositorySchema()


@repository.route('', methods=['GET'])
@jwt_required
def get_all():
    user = get_jwt_identity()
    result = Repository.query.get_by_owner(user)
    data = __repositoryScheme.dump(result, many=True).data
    return jsonify(data)


@repository.route('/<repository_id>', methods=['GET'])
@jwt_required
def get_repository(repository_id):
    result = Repository.query.get_by_id(repository_id)
    data = __repositoryScheme.dump(result).data
    return jsonify(data)


@repository.route('', methods=['POST'])
@jwt_required
def create_or_update_repository():
    user = get_jwt_identity()
    data = request.get_json()
    if data is None:
        raise ApiException(422, "No data.")
    data, errors = __repositoryScheme.load(data)
    if errors:
        return jsonify({'error': errors}), 422
    if 'id' not in data or data['id'] is None:
        data['owner_id'] = user['id']
        repository = Repository.create(data)
        app.db.session.add(repository)
    else:
        repository = Repository.query.get_by_id(data['id'])
        repository.update(data)
    app.db.session.commit()
    data = __repositoryScheme.dump(repository).data
    return jsonify(data)
