#!/usr/bin/env python3
from flask import Flask
import os

import google
import sql

app = Flask(__name__)
app.secret_key=os.urandom(16)
app.register_blueprint(google.bp, url_prefix="/login")

sql.init_db()

@app.teardown_appcontext
def shutdown_session(exception=None):
    sql.db_session.remove()

@app.route("/")
def hello():
    if google.loggedin():
        user = google.userinfo()
        return "Hello "+user['email']
    else:
        return "Not logged in"

@app.route("/privacy")
def private():
    return """
We hereby promise never to ever do anything with your information except
use your email to confirm you are authorized to check out hardware for the
William and Mary ACM.
"""

if __name__ == "__main__":
    app.run()
