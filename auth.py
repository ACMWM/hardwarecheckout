from flask import session
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
