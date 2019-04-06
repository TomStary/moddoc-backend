from moddoc import app
from moddoc.model import Role, User


__roles = [
    Role('admin', 1, True),
    Role('superadmin', 2, True),
]


def seed_roles():
    for role in __roles:
        if Role.query.filter_by(name=role.name, deleted=None).one_or_none()\
           is None:
            app.db.session.add(role)
    app.db.session.commit()


def seed_users():
    pass
