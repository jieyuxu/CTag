from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import pgpasslib
import os


Base = declarative_base()

# password = pgpasslib.getpass('localhost', 5555, 'qroom', 'postgres')
# if not password:
#     raise ValueError('Did not find a password in the .pgpass file')
#
# url = 'postgresql://postgres:{}@localhost:5555/iw_s20'.format(password)


url = 'postgresql://localhost/iw_s20'
# url = os.environ['DATABASE_URL']

engine = create_engine(url)
session_factory = sessionmaker(bind=engine)
