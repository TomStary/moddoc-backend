from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token
from sqlalchemy import or_
from moddoc.model import User
from moddoc.utils import ApiException
from moddoc.dto import LoginSchema, RegistrationSchema, UserSchema


auth = Blueprint('auth', __name__, url_prefix='/auth')
__loginSchema = LoginSchema()
__registrationSchema = RegistrationSchema()
__userSchema = UserSchema()


# TODO: need some refactor
@auth.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    if not data:
        raise ApiException(422, "No data.")
    form, errors = __loginSchema.load(data)
    if errors:
        return jsonify({'error': errors}), 422
    user = User.query\
        .filter(or_(User.email == form['username'],
                    User.username == form['username']))\
        .first()
    if user is None:
        raise ApiException(400, "Username or password mismatch.")
    from moddoc import app
    if app.bcrypt.check_password_hash(user.password, form['password']):
        data = __userSchema.dump(user).data
        data['token'] = create_access_token(identity=data)
        return jsonify(data)
    else:
        raise ApiException(400, "Username or password mismatch.")


@auth.route('/registration', methods=['POST'])
def registration():
    # TODO: make decorator with schema as param, returns valid data or raise exception  # noqa 501
    data = request.get_json()
    if not data:
        raise ApiException(422, "No data.")
    form, errors = __registrationSchema.load(data)
    if errors:
        return jsonify(errors), 422
    user = User.query\
        .filter(User.username == form['username'])\
        .first()
    if user is not None:
        raise ApiException(400, "Username taken.")
    user = User.query\
        .filter(User.email == form['email'])\
        .first()
    if user is not None:
        raise ApiException(400, "Email taken.")
    user = User(form['email'], form['username'], form['password'])
    from moddoc import app
    app.db.session.add(user)
    app.db.session.commit()
    data = __userSchema.dump(user).data
    data['token'] = create_access_token(data)
    return jsonify(data)
