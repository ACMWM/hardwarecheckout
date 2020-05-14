from flask_login import LoginManager, current_user, login_user, logout_user, login_required
from re import compile

domain = "email.wm.edu"

class EmailRegex:

    def __init__(self):
        self._email = compile(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)")

    def validemail(self, e):
        return self._email.fullmatch(e)

def initmanager(app, view, sql):
    manager = LoginManager()
    manager.init_app(app)
    manager.user_loader(sql.getuser)
    manager.login_view = view
