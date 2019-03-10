from flask import Blueprint, request, jsonify
from moddoc.utils import ApiException


auth = Blueprint('auth', __name__, url_prefix='/auth')


@auth.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    if not data:
        raise ApiException(422, "No data")
    return jsonify({'token': "yes"})
