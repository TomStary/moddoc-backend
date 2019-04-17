from setuptools import find_packages, setup

setup(
    name='moddoc',
    version='0.0.1',
    packages=find_packages(),
    install_requires=[
        'flask',
        'flask-sqlalchemy',
        'flask-migrate',
        'flask-cors',
        'flask-bcrypt',
        'flask_jwt_extended',
    ],
)
