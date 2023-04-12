from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Boolean, func
from sqlalchemy_utils import URLType
from db import Base

class Uploaded_files(Base):
    __tablename__ = "Uploaded_files"
    id = Column(Integer, primary_key=True)
    file = Column(URLType, nullable=False)
    source_id = Column(Integer, nullable=False)
    source = Column(String(20),nullable=True)
    comment = Column(String(200),nullable=True)
    user_id = Column(Integer, ForeignKey('Users.id',), nullable=False)
    created_on = Column(DateTime(timezone=True), default=func.now(), nullable=False)
    status = Column(Boolean, nullable=False, default=True)