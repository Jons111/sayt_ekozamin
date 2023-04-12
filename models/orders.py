from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Boolean, func, and_
from sqlalchemy.orm import relationship, backref

from db import Base
from models.customers import Customers


class Orders(Base):
    __tablename__ = "Orders"
    id = Column(Integer, primary_key=True)
    customer_id = Column(Integer,ForeignKey('Customers.id'), nullable=False)
    comment = Column(String(200),nullable=True)
    user_id = Column(Integer, nullable=False)
    date = Column(DateTime(timezone=True), default=func.now(), nullable=False)
    status = Column(Boolean, nullable=False, default=True)
    
    history = relationship("Kpi_History",back_populates="order")
    customer = relationship("Customers",back_populates="orders")
    nasiya = relationship("Nasiya",back_populates="order_nasiya")
    

    