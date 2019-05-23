from flask_login import LoginManager, current_user, login_user, logout_user, login_required
from re import compile
import sql

domain = "email.wm.edu"

checkemail = sql.checkemail

_email = compile(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)")

def validemail(e):
    return _email.fullmatch(e)

def setname(user, name):
    user.name = name
    sql.commit()

def load_user(user_id):
    return sql.getuser(user_id)

manager = None
def init(app, view):
    global manager
    manager = LoginManager()
    manager.init_app(app)
    manager.user_loader(load_user)
    manager.login_view = view
