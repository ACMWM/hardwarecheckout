#!/usr/bin/env python3
from flask import Flask, url_for, redirect, render_template, flash
import os

import google
import sql
import login
import forms

app = Flask(__name__)
app.secret_key=os.environ.get("SECRET_KEY") or os.urandom(16)
app.register_blueprint(google.bp, url_prefix="/login")
login.init(app)

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

@app.route("/add/", methods=["GET", "POST"])
def add():
    form = forms.AddHW()
    if form.validate_on_submit():
        flash("Added "+form.name.data)
        sql.addhw(form.name.data, form.category.data, form.quantity.data)
        return redirect(url_for("list"))
    return render_template("addhw.html", form=form)


@app.route("/update/<id>/", methods=["GET", "POST"])
def update(id):
    hw = sql.gethw(id)
    if hw is None:
        return "No such Hardware!"
    form = forms.UpdateHW()
    form.sethw(hw)
    if form.validate_on_submit():
        form.populate_obj(hw)
        if hw.quantity < hw.available:
            hw.available = hw.quantity
        sql.commit()
        return redirect(url_for("list"))
    return render_template("updatehw.html", form=form)

@app.route("/delete/<id>/", methods=["GET", "POST"])
def delete(id):
    hw = sql.gethw(int(id))
    if hw is None:
        return "No such id."
    form = forms.RemoveHW()
    form.sethw(hw)
    if hw is None:
        return err
    if form.validate_on_submit():
        hw.quantity = 0
        hw.available = 0
        sql.commit()
        flash("Deleted "+hw.name)
        return redirect(url_for("list"))
    else:
        return render_template("delhw.html", form=form)

@app.route("/checkout/<id>/", methods=["GET", "POST"])
def checkout(id):
    form = forms.Checkout()
    hw = sql.gethw(id)
    if hw is None:
        return "No such hardware!"
    form.sethw(hw)
    if hw.available < 1:
        flash("No "+hw.name+" available to checkout!")
        return redirect(url_for("list"))
    if form.validate_on_submit():
        flash("Checkout of "+hw.name+" x"+str(form.quantity.data)+" by "+form.who.data)
        sql.checkout(form.outdate.data, form.who.data, hw, form.reason.data,
                form.quantity.data, None)
        hw.available -= form.quantity.data
        sql.commit()
        return redirect(url_for("current"))
    else:
        return render_template("outform.html", form=form, hw=hw)

@app.route("/return/<id>/", methods=["GET", "POST"])
def Return(id):
    form = forms.Return()
    chk = sql.getchk(id)
    if chk is None:
        return "No such checkout!"
    form.setchk(chk)
    if chk.returndate != None:
        flash("Already Returned!")
        return redirect(url_for("list"))
    if form.validate_on_submit():
        sql.Return(chk, None, form.returndate.data)
        return redirect(url_for("current"))
    else:
        return render_template("return.html", form=form)


@app.route("/show/<id>/")
def show(id):
    hw=sql.gethw(id)
    if hw is None:
        return "No such hardware!"
    return render_template("hw.html", hw=hw)

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
    return render_template("checkouts.html", rows=sql.current())

@app.route("/history/")
def history():
    return render_template("checkouts.html", rows=sql.history())

if __name__ == "__main__":
    app.run()
