from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity

from moddoc.dto import ModuleSchema
from moddoc.model import Module
from moddoc.utils import ApiException

module = Blueprint('module', __name__, url_prefix='/module')
__moduleSchema = ModuleSchema()


@module.route('/all/<repository_id>', methods=['GET'])
@jwt_required
def get_all(repository_id):
    result = Module.query.get_by_repository(repository_id)
    data = __moduleSchema.dump(result, many=True).data
    return jsonify(data)


@module.route('/<module_id>', methods=['GET'])
@jwt_required
def get_module(module_id):
    user = get_jwt_identity()
    result = Module.query.get_by_id(module_id, user)
    data = __moduleSchema.dump(result).data
    return jsonify(data)


@module.route('', methods=['POST'])
@jwt_required
def create_or_update():
    user = get_jwt_identity()
    data = request.get_json()
    if data is None:
        raise ApiException(422, "No data.")
    data, errors = __moduleSchema.load(data)
    if errors:
        return jsonify({'error': errors}), 422
    module = Module.create_or_update(data, user)
    data = __moduleSchema.dump(module).data
    return jsonify(data)
