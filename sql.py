db = "sqlite:///test.db"

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine(db, convert_unicode=True)
db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))
Base = declarative_base()
Base.query = db_session.query_property()

from models import HW, User, Checkout

def init_db():
    import models
    #import oauthdb
    #oauthdb.storage(db_session)
    Base.metadata.create_all(bind=engine)

def commit():
    db_session.commit()

def add(obj):
    db_session.add(obj)
    commit()

def delete(obj):
    db_session.delete(obj)
    commit()

def checkemail(email):
    print(db_session.query(User).filterby(email=email))
    return True

def getuser(uid):
    return db_session.query(User).get(uid)

def gethw(id):
    return db_session.query(HW).get(id)

def search(keyword):
    if keyword is None:
        return db_session.query(HW)
    else:
        return db_session.query(HW).filter(HW.name.like('%'+keyword+'%'))

def addhw(name, category, quantity):
    h = HW(name=name, category=category, quantity=quantity, available=quantity)
    print(h)
    add(h)

def current():
    return db_session.query(Checkout).filter(Checkout.returndate==None).all()

def history():
    return db_session.query(Checkout).filter(Checkout.returndate!=None).all()

def checkout(outdate, who, hw, reason, quantity, user):
    c = Checkout(outdate=outdate, who=who, hardware=hw,
            what=hw.id, reason=reason, quantity=quantity, authorized_user=user,
            )
            #authorized_email=user.email)
    add(c)
