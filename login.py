from flask_login import LoginManager, current_user, login_user, logout_user, login_required
from sql import getuser

manager = LoginManager()

def init(app):
    manager.init_app(app)

@manager.user_loader
def load_user(user_id):
    return getuser(user_id)
