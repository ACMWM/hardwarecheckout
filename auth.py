from flask_login import LoginManager, current_user, login_user, logout_user, login_required
from re import compile

domain = "email.wm.edu"

_email = compile(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)")

def validemail(e):
    return _email.fullmatch(e)

manager = None
def init(app, view, sql):
    global manager
    manager = LoginManager()
    manager.init_app(app)
    manager.user_loader(sql.getuser)
    manager.login_view = view
