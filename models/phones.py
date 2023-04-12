from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Boolean, func, and_
from sqlalchemy.orm import relationship, backref
from db import Base
from .customers import Customers
from .users import Users


class Phones(Base):
    __tablename__ = "Phones"
    id = Column(Integer, primary_key=True)
    number = Column(String(20), nullable=False)
    source_id = Column(Integer,ForeignKey('Customers.id'), nullable=False)
    comment = Column(String(200),nullable=True)
    user_id = Column(Integer, nullable=False)
    created_on = Column(DateTime(timezone=True), default=func.now(), nullable=False)
    status = Column(Boolean, nullable=False, default=True)

    owner = relationship('Customers', back_populates='phones')
    

