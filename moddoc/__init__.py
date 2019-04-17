from flask import Flask, logging
from flask_bcrypt import Bcrypt
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
import datetime


class Moddoc(Flask):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.db = None
        self.bcrypt = None
        self.jwt = None

    @staticmethod
    def create_app():
        app = Moddoc(__name__)
        CORS(app)

        # FIXME: better config loader
        app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://effit_sys:rootroot@localhost/moddoc'  # noqa 501
        app.config['SECRET_KEY'] = "I have no secret"
        app.config['JWT_BLACKLIST_ENABLED'] = True
        app.config['JWT_BLACKLIST_TOKEN_CHECKS'] = ['access', 'refresh']

        # TODO: custom settings
        from moddoc.utils import IdModel, SoftDeleteQuery
        app.db = SQLAlchemy(app, model_class=IdModel,
                            query_class=SoftDeleteQuery)

        app.jwt = JWTManager(app)

        migrate = Migrate(app, app.db, render_as_batch=True)  # noqa 841

        app.bcrypt = Bcrypt(app)

        return app

    def init_api(self):
        from moddoc.api import auth, user, repository
        self.register_blueprint(auth)
        self.register_blueprint(user)
        self.register_blueprint(repository)

    def seeds(self):
        from moddoc.seed import seed_roles, seed_users
        seed_roles()
        seed_users()


app = Moddoc.create_app()
app.init_api()


@app.before_first_request
def seeds():
    app.seeds()

import moddoc.model  # noqa 402 401
import moddoc.service.auth_service  # noqa 401 402

__all__ = [
    'app',
]
