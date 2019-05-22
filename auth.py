from flask import session
import sql

domain = "email.wm.edu"

def checkemail(email):
    return sql.checkemail()
