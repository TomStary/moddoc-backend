from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required
from datetime import datetime

from moddoc import app
from moddoc.dto import RoleSchema
from moddoc.model import Role
from moddoc.service import check_roles_access
from moddoc.utils import ApiException


role = Blueprint('role', __name__, url_prefix='/role')
__roleSchema = RoleSchema()


@role.route('', methods=['GET'])
@jwt_required
@check_roles_access(1)
def get_all():
    roles = Role.query.get_all()
    result = __roleSchema.dump(roles, many=True).data
    return jsonify(result)


@role.route('/<role_id>', methods=['GET'])
@jwt_required
@check_roles_access(1)
def get_role(role_id):
    role = Role.query.get_by_id(role_id)
    if role is None:
        raise ApiException(400, 'No role with this ID was found.')
    result = __roleSchema.dump(role).data
    return jsonify(result)


@role.route('', methods=['POST'])
@jwt_required
@check_roles_access(1)
def post_role():
    data = request.get_json()
    if data is None:
        raise ApiException(422, 'No data.')
    data, errors = __roleSchema.load(data)
    if errors:
        return jsonify({'error': errors}), 422
    if 'id' not in data or data['id'] is None:
        role = Role.create(data)
        app.db.session.add(role)
    else:
        role = Role.update(data)
    app.db.session.commit()
    data = __roleSchema.dump(role).data
    return jsonify(data)


@role.route('/<role_id>', methods=['DELETE'])
@jwt_required
@check_roles_access(1)
def delete_role(role_id):
    role = Role.query.get_by_id(role_id)
    if role is None:
        raise ApiException(400,
                           'No role with this ID was found.')
    if role.default:
        raise ApiException(400,
                           'This role cannot be deleted')
    role.deleted = datetime.utcnow()
    app.db.session.commit()
    return jsonify()
