import datetime

from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Boolean, func,Float
from sqlalchemy.orm import relationship

from db import Base

class Kpi(Base):
    __tablename__ = "Kpi"
    id = Column(Integer, primary_key=True)
    percentage = Column(Float,nullable=False)
    source_id = Column(Integer,ForeignKey("Users.id"),nullable=False)
    user_id = Column(Integer, nullable=False)
    date = Column(DateTime(timezone=True), default=datetime.datetime.now(), nullable=False)
    status = Column(Boolean, nullable=False, default=True)
    
    user = relationship('Users',back_populates='kpi')