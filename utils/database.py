from sqlalchemy import Column, String, Integer, DateTime, Time, Boolean, ForeignKey, Float
from sqlalchemy.orm import relationship
from utils.base import Base

class Users(Base):
    __tablename__ = "users"

    net_id = Column(String(120), primary_key=True)

    # a user can be associated with more than 1 album
    rooms = relationship("Albums", backref='user')

class Albums(Base):
    __tablename__ = "albums"

    album_id = Column(Integer, primary_key=True)
    name = Column(String(120), nullable=False)
    net_id = Column(String(120), ForeignKey('users.net_id'), nullable=False)
