from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Boolean, func, and_,Date
from sqlalchemy.orm import relationship, backref

from db import Base
from models.customers import Customers


class Nasiya(Base):
    __tablename__ = "Nasiya"
    id = Column(Integer, primary_key=True)
    money = Column(Integer, nullable=False)
    customer_id = Column(Integer,ForeignKey("Customers.id"),nullable=False)
    order_id = Column(Integer,ForeignKey("Orders.id"),nullable=False)
    user_id = Column(Integer, nullable=False)
    date_time = Column(DateTime(timezone=True), default=func.now(), nullable=False)
    status = Column(Boolean, nullable=False, default=True)
    deadline = Column(Date,nullable=False)

    customer = relationship("Customers",back_populates="nasiya")
    order_nasiya = relationship("Orders",back_populates="nasiya")