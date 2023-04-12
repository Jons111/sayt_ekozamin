from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

#database url
# SQLALCHEMY_DATABASE_URL = 'mysql+pymysql://travert1_user:2542404Uz@83.69.139.250:3306/travert1_baza'

import os
BASE_DIR = os.path.dirname(os.path.realpath(__file__))
SQLALCHEMY_DATABASE_URL = 'sqlite:///'+os.path.join(BASE_DIR,'bazza.db')
SECRET_KEY = 'SOME-SECRET-KEY'
ALGORITHM = 'HS256'
ACCESS_TOKEN_EXPIRE_MINUTES = 30

engine = create_engine(SQLALCHEMY_DATABASE_URL, echo=True)



SessionLocal = sessionmaker(autocommit=False,autoflush=False,bind=engine)


Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()