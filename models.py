from sqlalchemy import Column, Boolean, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from sql import Base

class User(Base):
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
