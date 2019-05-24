from os import environ
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

from models import Base, HW, User, Checkout

db = environ.get("DATABASE_URL") or "sqlite:///test.db"

engine = create_engine(db, convert_unicode=True)
db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))
Base.query = db_session.query_property()

def init_db(auth=None, google=None):
    import oauthdb
    if auth is not None and google is not None:
        oauthdb.storage(db_session, auth, google)
    Base.metadata.create_all(bind=engine, checkfirst=True)

def commit():
    db_session.commit()

def add(obj):
    db_session.add(obj)
    commit()

def allusers():
    return db_session.query(User).order_by(User.name)

def getuser(e):
    return db_session.query(User).get(e)

def newuser(email):
    add(User(id=email))

def deluser(email):
    db_session.delete(getuser(email))
    commit()

def setname(user, name):
    user.name = name
    commit()

def gethw(id):
    return db_session.query(HW).get(id)

def getchk(id):
    return db_session.query(Checkout).get(id)

def search(keyword):
    q = db_session.query(HW).order_by(HW.category).order_by(HW.name)
    if keyword is None:
        return q
    else:
        return q.filter(HW.name.like('%'+keyword+'%'))

def addhw(name, category, quantity):
    h = HW(name=name, category=category, quantity=quantity, available=quantity)
    add(h)

def categories():
    return db_session.query(HW.category).distinct()

def current():
    return db_session.query(Checkout).filter(Checkout.returndate==None).all()

def history():
    return db_session.query(Checkout).filter(Checkout.returndate!=None).all()

def checkout(outdate, who, hw, reason, quantity, user):
    c = Checkout(outdate=outdate, who=who, hardware=hw,
            what=hw.id, reason=reason, quantity=quantity, out_auth_user=user,
            out_auth_email=user.id)
    add(c)

def Return(chk, user, date):
    chk.returndate = date
    chk.hardware.available += chk.quantity
    chk.in_user_auth = user
    chk.in_user_email = user.id
    commit()
