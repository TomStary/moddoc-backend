from flask import jsonify
from moddoc.api.authentication import auth
from moddoc.api.user import user
from moddoc.dto import Error
from moddoc.utils import ApiException


error_scheme = Error()


@auth.errorhandler(ApiException)
@user.errorhandler(ApiException)
def __response_error_handler(error):
    result = {'error': error_scheme.dump(error).data}
    return jsonify(result), error.errorCode


__all__ = [
    'auth',
    'user'
]
