from flask import jsonify
from moddoc.api.authentication import auth
from moddoc.dto import Error
from moddoc.utils import ApiException


error_scheme = Error()


@auth.errorhandler(ApiException)
def __response_error_handler(error):
    result = error_scheme.dump(error)
    return jsonify({'error': result}), error.errorCode


__all__ = [
    'auth',
]