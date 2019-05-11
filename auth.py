from flask import session
import sql


def checkemail(email):
    return sql.checkemail()

def getuser():
    return session['user']
