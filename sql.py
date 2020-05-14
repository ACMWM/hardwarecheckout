from os import environ
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

from models import Base, HW, User, Checkout

class SQL:
    def __init__(self, google=None, db=None):
        if db is None:
            db = environ.get("DATABASE_URL") or "sqlite:///test.db"
        self._db = db
        self._engine = create_engine(db, convert_unicode=True)
        self.db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=self._engine))
        Base.query = self.db_session.query_property()
        self._createall()

    def _createall(self):
        Base.metadata.create_all(bind=self._engine, checkfirst=True)

    def setgoogle(self, google):
        import oauthdb
        oauthdb.storage(self.db_session, google)
        self._createall()

    def commit(self):
        self.db_session.commit()

    def add(self, obj):
        self.db_session.add(obj)
        self.commit()

    def allusers(self):
        return self.db_session.query(User).order_by(User.name)

    def getuser(self, e):
        return self.db_session.query(User).get(e)

    def newuser(self, email):
        self.add(User(id=email))

    def deluser(self, email):
        self.db_session.delete(self.getuser(email))
        self.commit()

    def setname(self, user, name):
        user.name = name
        self.commit()

    def gethw(self, id):
        return self.db_session.query(HW).get(id)

    def getchk(self, id):
        return self.db_session.query(Checkout).get(id)

    def search(self, keyword):
        q = self.db_session.query(HW).order_by(HW.category).order_by(HW.name)
        if keyword is None:
            return q
        else:
            return q.filter(HW.name.like('%'+keyword+'%'))

    def addhw(self, name, category, quantity):
        h = HW(name=name, category=category, quantity=quantity, available=quantity)
        self.add(h)

    def categories(self):
        return self.db_session.query(HW.category).distinct()

    def current(self):
        return self.db_session.query(Checkout).filter(Checkout.returndate==None).all()

    def history(self):
        return self.db_session.query(Checkout).filter(Checkout.returndate!=None).all()

    def checkout(self, outdate, who, hw, reason, quantity, user):
        c = Checkout(outdate=outdate, who=who, hardware=hw,
                what=hw.id, reason=reason, quantity=quantity, out_auth_user=user,
                out_auth_email=user.id)
        self.add(c)

    def Return(self, chk, user, date):
        chk.returndate = date
        chk.hardware.available += chk.quantity
        chk.in_auth_user = user
        self.commit()
