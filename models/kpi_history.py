from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Boolean, func,Float
from sqlalchemy.orm import relationship

from db import Base

class Kpi_History(Base):
    __tablename__ = "Kpi_History"
    id = Column(Integer, primary_key=True)
    money = Column(Integer, nullable=True)
    type = Column(String(20),nullable=True)
    order_id = Column(Integer,ForeignKey('Orders.id'), nullable=False)
    comment = Column(String(200),nullable=True)
    user_id = Column(Integer, nullable=False)
    date = Column(DateTime(timezone=True), default=func.now(), nullable=False)
    status = Column(Boolean, nullable=False, default=True)
    return_date = Column(DateTime(timezone=True), nullable=False)
    order = relationship("Orders",back_populates="history")