from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity

from moddoc import app
from moddoc.model import User
from moddoc.dto import UserSchema, RoleAssignSchema
from moddoc.service import check_roles_access
from moddoc.utils import ApiException


user = Blueprint('user', __name__, url_prefix='/user')
__userSchema = UserSchema()
__assignRolesSchema = RoleAssignSchema()


@user.route("", methods=['GET'])
@jwt_required
@check_roles_access(1)
def get_all_users():
    """
    Returns all user, only available for administrators, because it could
    contain sensitive data
    """
    users = User.query.soft_all()
    result, errors = __userSchema.dump(users, many=True)
    return jsonify(result)


@user.route("/<id>", methods=['GET'])
@jwt_required
@check_roles_access(1)
def get_user(id):
    """
    Returns user by its `id`, only available for administrators, because it
    could contain sensitive data
    """
    user = User.query.soft_get(id)
    result, error = __userSchema.dump(user)
    return jsonify(result)


@user.route('/yourself', methods=['GET'])
@jwt_required
def get_your_information():
    """
    Returns your full information
    """
    user = get_jwt_identity()
    result, error = __userSchema.dump(user)
    return jsonify(result)


@user.route('/yourself', methods=['POST'])
@jwt_required
def update_your_profile():
    """
    Changes users personal info
    """
    data = request.get_json()
    if not data:
        raise ApiException(422, "No data.")
    userData, errors = __userSchema.load(data)
    if errors:
        return jsonify({'error': errors}), 422
    user = User.query.soft_get(userData['id'])
    user.update(userData)
    result = __userSchema.dump(user).data
    app.db.session.commit()
    return jsonify(result)


@user.route('/yourself', methods=['DELETE'])
@jwt_required
def delete_profile():
    """
    Remove profile
    """
    user = get_jwt_identity()
    dbUser = User.query.soft_get(user['id'])
    if dbUser is None:
        raise ApiException(404, "Your account has been deleted.")
    dbUser.delete()
    app.db.session.commit()
    return jsonify()


@user.route('/roles', methods=['POST'])
@jwt_required
@check_roles_access(1)
def assign_roles_to_users():
    """Assing one or more roles to
    one or more users"""
    data = request.get_json()
    if not data:
        raise ApiException(422, "No data.")
    assignRoles, errors = __assignRolesSchema.load(data)
    if errors:
        return jsonify({'error': errors}), 422
    for user_id in assignRoles['users']:
        user = User.query.soft_get(user_id)
        if user is None:
            raise ApiException(400, "One of the users does not exists.")
        for role_id in assignRoles['roles']:
            user.add_role_by_id(role_id)
    app.db.session.commit()
    return jsonify()
