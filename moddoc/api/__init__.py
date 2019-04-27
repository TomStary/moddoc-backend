from flask import jsonify
from moddoc.api.authentication import auth
from moddoc.api.user import user
from moddoc.api.repository import repository
from moddoc.api.document import document
from moddoc.api.module import module
from moddoc.dto import Error
from moddoc.utils import ApiException


error_scheme = Error()


@auth.errorhandler(ApiException)
@user.errorhandler(ApiException)
@module.errorhandler(ApiException)
@repository.errorhandler(ApiException)
@document.errorhandler(ApiException)
def __response_error_handler(error):
    result = {'error': error_scheme.dump(error).data}
    return jsonify(result), error.errorCode


__all__ = [
    'auth',
    'user',
    'repository',
    'module',
    'document',
]
