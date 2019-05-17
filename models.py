from sqlalchemy import Column, Boolean, Integer, String, ForeignKey
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
    name = Column(String)
    quantity = Column(Integer)
    whom = Column(String)
    authorized_email = Column(String, ForeignKey(User.email))
    authorized_user = relationship(User)
