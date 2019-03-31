from flask import Blueprint, jsonify
from flask_login import login_required

from moddoc.model import User


user = Blueprint('user', __name__, url_prefix='/user')


@login_required
def get_all_users():
    User.query.soft_all()
