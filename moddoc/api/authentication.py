from flask import Blueprint, request, jsonify
from flask_jwt_extended import (
    create_access_token, create_refresh_token, jwt_refresh_token_required,
    get_jwt_identity, jwt_required
)
from sqlalchemy import or_

from moddoc import app
from moddoc.model import User
from moddoc.utils import ApiException
from moddoc.dto import LoginSchema, RegistrationSchema, UserSchema
from moddoc.service import (
    add_token_to_database, get_user_tokens, revoke_token
)


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
                    User.username == form['username'],
                    User.deleted is None))\
        .one_or_none()
    if user is None:
        raise ApiException(400, "Username or password mismatch.")
    from moddoc import app
    if app.bcrypt.check_password_hash(user.password, form['password']):
        data = __userSchema.dump(user).data
        data['access_token'] = create_access_token(identity=data)
        data['refresh_token'] = create_refresh_token(identity=data)
        add_token_to_database(data['access_token'],
                              app.config['JWT_IDENTITY_CLAIM'])
        add_token_to_database(data['refresh_token'],
                              app.config['JWT_IDENTITY_CLAIM'])
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
        .one_or_none()
    if user is not None:
        raise ApiException(400, "Username taken.")
    user = User.query\
        .filter(User.email == form['email'])\
        .one_or_none()
    if user is not None:
        raise ApiException(400, "Email taken.")
    user = User(form['username'], form['email'], form['password'])
    from moddoc import app
    app.db.session.add(user)
    app.db.session.commit()
    return jsonify()


@auth.route('/refresh', methods=['POST'])
@jwt_refresh_token_required
def refresh():
    current_user = get_jwt_identity()
    access_token = create_access_token(identity=current_user)
    add_token_to_database(access_token, app.config['JWT_IDENTITY_CLAIM'])
    return jsonify({'access_token': access_token}), 201


@auth.route('/logout', methods=['GET'])
@jwt_required
def logout():
    user_identity = get_jwt_identity()
    all_tokens = get_user_tokens(user_identity)
    for token in all_tokens:
        revoke_token(token.id, user_identity)
    return jsonify()
