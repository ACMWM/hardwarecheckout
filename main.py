
from flask import Flask

import oauth
import sql

sql.init_db()

@app.teardown_appcontext
def shutdown_session(exception=None):
    sql.db_session.remove()

app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello World!!"
