from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required, get_jwt_claims

from moddoc.model import User
from moddoc.dto import UserSchema


user = Blueprint('user', __name__, url_prefix='/user')
__userSchema = UserSchema()


@user.route("", methods=['GET'])
@jwt_required
def get_all_users():
    users = User.query.soft_all()
    print(get_jwt_claims())
    result, errors = __userSchema.dump(users, many=True)
    return jsonify(result)