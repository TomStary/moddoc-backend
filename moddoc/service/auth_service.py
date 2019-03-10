from flask_login import LoginManager


login_manager = LoginManager()


@login_manager.user_loader
def get_user(user_id):
    from moddoc.model import User
    return User.query.get(user_id)
