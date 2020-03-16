from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

url = 'postgresql://localhost/iw_s20'
engine = create_engine(url)
session_factory = sessionmaker(bind=engine)
