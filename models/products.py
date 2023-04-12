from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Boolean, func
from sqlalchemy.orm import relationship

from db import Base

class Products(Base):
    __tablename__ = "Products"
    id = Column(Integer, primary_key=True)
    name = Column(String(20), nullable=False)
    birlik = Column(String(20), nullable=False)
    comment = Column(String(200),nullable=True)
    price = Column(Integer,nullable=False)
    user_id = Column(Integer, nullable=False)
    created_on = Column(DateTime(timezone=True), default=func.now(), nullable=False)
    status = Column(Boolean, nullable=False, default=True)

    trades = relationship("Trades", back_populates="products")
    
    

