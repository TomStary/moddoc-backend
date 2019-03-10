from flask import Blueprint, request, jsonify, current_app
from flask_login import current_user, login_user
from sqlalchemy import or_
from moddoc.model import User
from moddoc.utils import ApiException
from moddoc.dto import LoginSchema


auth = Blueprint('auth', __name__, url_prefix='/auth')
__loginSchema = LoginSchema()


@auth.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    if not data:
        raise ApiException(422, "No data")
    if current_user.is_authenticated:
        return jsonify({'token': 'yes'})
    form, errors = __loginSchema.load(data)
    if errors:
        return jsonify(errors), 422
    user = User.query\
        .filter(or_(User.email == form['username'],
                    User.username == form['username']))\
        .first()
    if user is None:
        raise ApiException(400, "Username or password mismatch.")
    from moddoc import app
    if app.bcrypt.check_password_hash(user.password, form['password']):
        login_user(user)
        return jsonify({"status": "logged"})
    else:
        raise ApiException(400, "Username or password mismatch.")
