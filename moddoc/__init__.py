from flask import Flask, logging
from flask_bcrypt import Bcrypt
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from moddoc.service import login_manager


class Moddoc(Flask):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.db = None
        self.bcrypt = None

    @staticmethod
    def create_app():
        app = Moddoc(__name__)
        CORS(app)

        # FIXME: better config loader
        app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://effit_sys:rootroot@localhost/moddoc'  # noqa 501
        app.config['SECRET_KEY'] = "I have no secret"

        # TODO: custom settings
        from moddoc.utils import IdModel, SoftDeleteQuery
        app.db = SQLAlchemy(app, model_class=IdModel,
                            query_class=SoftDeleteQuery)

        JWTManager(app)

        migrate = Migrate(app, app.db, render_as_batch=True)  # noqa 841

        app.bcrypt = Bcrypt(app)

        return app

    def init_api(self):
        from moddoc.api import auth, user
        self.register_blueprint(auth)
        self.register_blueprint(user)

    def init_user(self):
        from moddoc.model import User
        app.db.session.add(User("test@test.com", "test", "test"))
        app.db.session.commit()


app = Moddoc.create_app()
# login_manager.init_app(app)
app.init_api()

import moddoc.model  # noqa 402 401s

__all__ = [
    'app',
]
