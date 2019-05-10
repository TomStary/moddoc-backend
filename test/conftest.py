from flask_migrate import upgrade
import os
import pytest

from moddoc import Moddoc


@pytest.fixture(scope='session')
def app():
    """
    Creates instance of application with test configuration for each test
    session
    """
    app = Moddoc.create_app('test')

    # register our blueprints
    with app.app_context():
        app.init_api()

    # return generator for app
    yield app


@pytest.fixture(scope='session')
def db(app):
    with app.app_context():
        upgrade(os.path.dirname(__file__) + '/../migrations')
        app.db.create_all()

    yield app.db

    with app.app_context():
        app.db.session.remove()
        app.db.reflect()
        app.db.drop_all()


@pytest.fixture(scope='session')
def client(app, db):
    client = app.test_client()
    yield client
