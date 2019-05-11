#!/usr/bin/env python3
from flask import Flask
import os

import google
import sql

app = Flask(__name__)
app.secret_key=os.environ.get("SECRET_KEY")

sql.init_db()

@app.teardown_appcontext
def shutdown_session(exception=None):
    sql.db_session.remove()

@app.route("/")
def hello():
    return "Hello World!!"


if __name__ == "__main__":
    app.run()
