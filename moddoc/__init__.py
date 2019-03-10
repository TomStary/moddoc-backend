from flask import Flask, Blueprint
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_restful import Api


class Moddoc(Flask):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.db = None
        self.api = None

    @staticmethod
    def create_app():
        app = Moddoc(__name__)

        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/moddoc.db'

        # TODO: custom settings
        from moddoc.utils import IdModel
        app.db = SQLAlchemy(app, model_class=IdModel)

        migrate = Migrate(app, app.db, render_as_batch=True) # noqa 841

        app.api = Api(app)

        return app

    def init_api_resources(self):
        from moddoc.api import Login
        self.api.add_resource(Login, '/login')


app = Moddoc.create_app()
app.init_api_resources()

import moddoc.model  # noqa 402 401

__all__ = [
    'app'
]
