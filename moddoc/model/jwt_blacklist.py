import sqlalchemy as sa

from moddoc import app


class TokenBlacklist(app.db.Model):
    jti = sa.Column(sa.String(36), nullable=False)
    token_type = sa.Column(sa.String(10), nullable=False)
    user_identity = sa.Column(sa.String(50), nullable=False)
    revoked = sa.Column(sa.Boolean, nullable=False)
    expires = sa.Column(sa.DateTime, nullable=False)