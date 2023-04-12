from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Boolean, func

from db import Base


class Expenses(Base):
    __tablename__ = "Expenses"
    id = Column(Integer, primary_key=True)
    money = Column(Integer, nullable=False)
    type = Column(String(20), nullable=True)
    source_id = Column(Integer, nullable=False)
    source = Column(String(200), nullable=False)
    user_id = Column(Integer,nullable=False)
    date_time = Column(DateTime(timezone=True), default=func.now(), nullable=False)
    status = Column(Boolean, nullable=False, default=True)
