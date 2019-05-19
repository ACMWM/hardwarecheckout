#!/usr/bin/env python3
from flask import Flask, url_for, redirect, render_template
import os

import google
import sql
#import login
import forms

app = Flask(__name__)
app.secret_key=os.environ.get("SECRET_KEY") or os.urandom(16)
app.register_blueprint(google.bp, url_prefix="/login")
#login.init(app)

sql.init_db()

@app.teardown_appcontext
def shutdown_session(exception=None):
    sql.db_session.remove()

@app.route("/")
def hello():
    if google.loggedin():
        user = google.userinfo()
        print("LOGGED IN "+user['email'])
    return render_template("index.html")

@app.route("/auth")
def login():
    return redirect(url_for("google.login"))

@app.route("/add", methods=["GET", "POST"])
def add():
    form = forms.AddHW()
    if form.validate_on_submit():
        print("Adding "+form.name.data)
        sql.addhw(form.name.data, form.category.data, form.quantity.data)
        return redirect(url_for("list"))
    return render_template("addhw.html", form=form)

@app.route("/delete/<id>/")
def delete(id):
    pass

@app.route("/checkout/<id>/")
def checkout(id):
    pass

@app.route("/show/<id>/")
def show(id):
    pass

@app.route("/privacy")
def private():
    return """
We hereby promise never to ever do anything with your information except
use your email to confirm you are authorized to check out hardware for the
William and Mary ACM.
"""

@app.route("/list/")
@app.route("/list/<keyword>")
def list(keyword=None):
    s = sql.search(keyword)
    return render_template("list.html", objs=s)

@app.route("/current/")
def current():
    pass

@app.route("/history/")
def history():
    pass

if __name__ == "__main__":
    app.run()
