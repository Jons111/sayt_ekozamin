from sqlalchemy import Column, Integer, String, Boolean,Float,Text
from sqlalchemy.orm import relationship

from db import Base




class Users(Base):
    __tablename__ = "Users"
    id = Column(Integer, primary_key=True)
    roll = Column(String(20), nullable=False)
    name = Column(String(20), nullable=False)
    number = Column(String(20), nullable=False)
    balance = Column(Float, nullable=True,default=0)
    salary = Column(Float, nullable=True,default=0)
    username = Column(String(20), unique=True, nullable=False)
    password = Column(String(200), nullable=False)
    status = Column(Boolean, nullable=False, default=True)
    token = Column(String(400), default='',nullable=True)
    
    kpi = relationship("Kpi",back_populates="user")

    