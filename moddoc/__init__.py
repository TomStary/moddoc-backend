from flask import Flask, logging
from flask_bcrypt import Bcrypt
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
import datetime
import os


class Moddoc(Flask):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.db = None
        self.bcrypt = None
        self.jwt = None

    @staticmethod
    def create_app(environment='prod'):
        app = Moddoc(__name__, instance_relative_config=True)
        CORS(app)

        # Load the default configuration
        app.config.from_object('config.default')

        # Load the configuration from the instance folder
        app.config.from_pyfile('config.py')
        app.config.from_pyfile('%s.py' % environment, True)

        from moddoc.utils import IdModel, SoftDeleteQuery, naming_convention
        from sqlalchemy import MetaData
        app.db = SQLAlchemy(app, model_class=IdModel,
                            query_class=SoftDeleteQuery,
                            metadata=MetaData(naming_convention=naming_convention))  # noqa 501

        app.jwt = JWTManager(app)

        migrate = Migrate(app, app.db, render_as_batch=True)  # noqa 841

        app.bcrypt = Bcrypt(app)

        return app

    def init_api(self):
        from moddoc.api import auth, user, repository, role, module, document, permission  # noqa 501
        self.register_blueprint(auth)
        self.register_blueprint(user)
        self.register_blueprint(module)
        self.register_blueprint(document)
        self.register_blueprint(repository)
        self.register_blueprint(role)
        self.register_blueprint(permission)

    def seeds(self):
        from moddoc.seed import seed_roles, seed_users
        seed_roles()
        seed_users()

    def prepare_build(self):
        if not os.path.isdir('./build'):
            os.mkdir('./build')

    def create_file(self, filename, content):
        path_to_file = './build/%s.rst' % filename
        file = open(path_to_file, 'w')
        file.write(content)
        file.close()

    def generate_file(self, filename):
        import pypandoc
        path_to_file = './build/%s.rst' % filename
        outputfile = os.getcwd() + '/build/%s.pdf' % filename
        pypandoc.convert_file(path_to_file, 'pdf', outputfile=outputfile)
        return outputfile


app = Moddoc.create_app()
app.init_api()
app.prepare_build()


@app.before_first_request
def seeds():
    app.seeds()

import moddoc.model  # noqa 402 401
import moddoc.service.auth_service  # noqa 401 402

__all__ = [
    'app',
    'Moddoc'
]
