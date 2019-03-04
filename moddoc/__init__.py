from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate


class Moddoc(Flask):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.db = None

    @staticmethod
    def create_app():
        app = Moddoc(__name__)

        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/moddoc.db'

        # TODO: custom settings
        from moddoc.utils import IdModel
        app.db = SQLAlchemy(app, model_class=IdModel)

        migrate = Migrate(app, app.db, render_as_batch=True) # noqa 841

        return app


app = Moddoc.create_app()

from moddoc.model import User

__all__ = [
    'app'
]
