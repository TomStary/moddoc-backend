from flask_jwt_extended import get_jwt_claims, decode_token
from functools import wraps
from datetime import datetime
from sqlalchemy.orm.exc import NoResultFound
import uuid

from moddoc import app
from moddoc.utils import ApiException
from moddoc.model import TokenBlacklist


@app.jwt.user_claims_loader
def add_claims(user):
    return {'roles': user['roles']}


@app.jwt.user_identity_loader
def load_user(user):
    return user


def _epoch_utc_to_datetime(epoch_utc):
    """
    Helper function for converting epoch timestamps (as stored in JWTs) into
    python datetime objects (which are easier to use with sqlalchemy).
    """
    return datetime.fromtimestamp(epoch_utc)


def add_token_to_database(encoded_token, identity_claim):
    """
    Adds a new token to the database. It is not revoked when it is added.
    :param identity_claim:
    """
    decoded_token = decode_token(encoded_token)
    jti = decoded_token['jti']
    token_type = decoded_token['type']
    user_identity = decoded_token[identity_claim]['id']
    expires = _epoch_utc_to_datetime(decoded_token['exp'])
    revoked = False

    db_token = TokenBlacklist(
        id=uuid.uuid4(),
        jti=jti,
        token_type=token_type,
        user_identity=user_identity,
        expires=expires,
        revoked=revoked,
    )
    app.db.session.add(db_token)
    app.db.session.commit()


def is_token_revoked(decoded_token):
    """
    Checks if the given token is revoked or not. Because we are adding all the
    tokens that we create into this database, if the token is not present
    in the database we are going to consider it revoked, as we don't know where
    it was created.
    """
    jti = decoded_token['jti']
    try:
        token = TokenBlacklist.query.filter_by(jti=jti).one()
        return token.revoked
    except NoResultFound:
        return True


def get_user_tokens(user_identity):
    """
    Returns all of the tokens, revoked and unrevoked, that are stored for the
    given user
    """
    return TokenBlacklist.query.filter_by(user_identity=user_identity['id'])\
        .all()


def revoke_token(token_id, user):
    """
    Revokes the given token. Raises a TokenNotFound error if the token does
    not exist in the database
    """
    try:
        token = TokenBlacklist.query.filter_by(id=token_id,
                                               user_identity=user['id'])\
            .one()
        token.revoked = True
        app.db.session.commit()
    except NoResultFound:
        raise ApiException("Could not find the token {}".format(token_id))


def unrevoke_token(token_id, user):
    """
    Unrevokes the given token. Raises a TokenNotFound error if the token does
    not exist in the database
    """
    try:
        token = TokenBlacklist.query.filter_by(id=token_id,
                                               user_identity=user['id'])\
            .one()
        token.revoked = False
        app.db.session.commit()
    except NoResultFound:
        raise ApiException("Could not find the token {}".format(token_id))


def prune_database():
    """
    Delete tokens that have expired from the database.
    How (and if) you call this is entirely up you. You could expose it to an
    endpoint that only administrators could call, you could run it as a cron,
    set it up with flask cli, etc.
    """
    now = datetime.now()
    expired = TokenBlacklist.query.filter(TokenBlacklist.expires < now).all()
    for token in expired:
        app.db.session.delete(token)
    app.db.session.commit()


@app.jwt.token_in_blacklist_loader
def check_if_token_revoked(decoded_token):
    return is_token_revoked(decoded_token)


def check_roles_access(minimum_flag=0):
    """
    This decorator is used to check if user has enough permission for an action
    If not 403 error will be raised
    """
    def check_roles_access_decorator(func):
        @wraps(func)
        def function_wrapper(*args, **kwargs):
            roles = get_jwt_claims()
            for role in roles['roles']:
                if role['flag'] > minimum_flag:
                    return func(*args, **kwargs)
            raise ApiException(403, "You do not have enough permission for\
 this action.")
        return function_wrapper
    return check_roles_access_decorator
