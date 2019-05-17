from sqlalchemy import Column, Boolean, Integer, String, ForeignKey, Date
from sqlalchemy.orm import relationship
from sql import Base
from flask_login import UserMixin

class User(Base, UserMixin):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    email = Column(String)
    name = Column(String)

class HW(Base):
    __tablename__ = "HW"
    id = Column(Integer, primary_key=True)
    category = Column(String)
    name = Column(String)
    quantity = Column(Integer)
    available = Column(Integer)


class Checkouts(Base):
    __tablename__ = "Checkouts"
    id = Column(Integer, primary_key=True)
    outdate = Column(Date)
    returndate = Column(Date)
    whom = Column(String)
    what = Column(Integer, ForeignKey(HW.id))
    hardware = relationship(HW)
    reason = Column(String)
    quantity = Column(Integer)
    authorized_email = Column(String, ForeignKey(User.email))
    authorized_user = relationship(User)
