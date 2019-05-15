from setuptools import find_packages, setup

setup(
    name='moddoc',
    version='0.1.0',
    packages=find_packages(),
    install_requires=[
        'flask',
        'flask-sqlalchemy',
        'flask-migrate',
        'flask-cors',
        'flask-bcrypt',
        'flask_jwt_extended',
        'psycopg2',
        'pypandoc',
        'marshmallow'
    ],
)
