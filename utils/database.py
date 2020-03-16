from sqlalchemy import Column, String, Integer, BLOB, ForeignKey
from sqlalchemy.orm import relationship
from utils.base import Base

class Users(Base):
    __tablename__ = "users"

    net_id = Column(String(120), primary_key=True)
    albums = relationship("Albums", backref='user') # a user - many albums

class Albums(Base):
    __tablename__ = "albums"

    album_id = Column(Integer, primary_key=True)
    name = Column(String(120), nullable=False)
    net_id = Column(String(120), ForeignKey('users.net_id'), nullable=False)

    images = relationship("Images", backref='album') # an album - many images


class Images(Base):
    __tablename__ = "images"

    image_id = Column(Integer, primary_key=True)
    album_id = Column(Integer, ForeignKey('albums.album_id'), nullable=False)

    tags = relationship("Tags", secondary = 'image_tags')


class Tags(Base):
    __tablename__ = "tags"

    tag_id = Column(Integer, primary_key=True)
    name = Column(String(120), nullable=False)
    confidence = Column(Integer, nullable=True)
    tag_type = Column(String(120), ForeignKey('tag_types.name'), nullable=False)

    images = relationship("Images", secondary = 'image_tags')

class Tag_Types(Base):
    __tablename__ = "tag_types"

    name = Column(String(120), primary_key=True)
    tags = relationship("Tags", backref='type') # a type - many tags

# junction table for image and tags, many-to-many relationship
class Image_Tags(Base):
    __tablename__ = "image_tags"

    tag_id = Column(Integer, ForeignKey('tags.tag_id'), primary_key = True)
    image_id =  Column(Integer, ForeignKey('images.image_id'), primary_key = True)
