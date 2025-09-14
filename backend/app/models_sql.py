from .database import base
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

class User(base):
    __tablename__ = 'user'
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    nome = Column(String, nullable=True)
    username = Column(String, index=True, unique=True)
    email = Column(String)
    senha = Column(String)
    favorite_artist = Column(String, nullable=True)
    user_photo_url = Column(String, nullable=True)
    
class Artist(base):
    __tablename__ = 'artist'
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    nome = Column(String)
    music_genre = Column(String)
    albums = relationship("Album", back_populates="criador")
    
class Album(base):
    __tablename__ = 'album'
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    nome = Column(String)
    total_tracks = Column(Integer)
    artist_id = Column(Integer, ForeignKey('artist.id'))
    
    criador = relationship("Artist", back_populates="albums")