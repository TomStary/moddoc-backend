from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity

from moddoc import app
from moddoc.dto import ModuleSchema
from moddoc.model import Module
from moddoc.utils import ApiException

module = Blueprint('module', __name__, url_prefix='/module')
__moduleSchema = ModuleSchema()


@module.route('/all/<repository_id>', methods=['GET'])
@jwt_required
def get_all(repository_id):
    print(repository_id)
    result = Module.query.get_by_repository(repository_id)
    data = __moduleSchema.dump(result, many=True).data
    return jsonify(data)


@module.route('/<module_id>', methods=['GET'])
@jwt_required
def get_module(module_id):
    result = Module.query.get_by_id(module_id)
    data = __moduleSchema.dump(result).data
    return jsonify(data)


@module.route('', methods=['POST'])
@jwt_required
def create_or_update():
    data = request.get_json()
    if data is None:
        raise ApiException(422, "No data.")
    data, errors = __moduleSchema.load(data)
    if errors:
        return jsonify({'error': errors}), 422
    if 'id' not in data or data['id'] is None:
        module, history = Module.create(data)
        app.db.session.add(module)
        app.db.session.add(history)
    else:
        module, history = Module.update(data)
        app.db.session.add(history)
    app.db.session.commit()
    data = __moduleSchema.dump(module).data
    return jsonify(data)
