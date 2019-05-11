from Flask import session
import sql


def checkemail(email):
    return sql.checkemail()

def getuser(email):
    return session['email']
