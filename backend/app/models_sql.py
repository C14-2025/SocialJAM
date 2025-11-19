from .database import base
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, UniqueConstraint, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime

class User(base):
    __tablename__ = 'user'
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    nome = Column(String, nullable=True)
    username = Column(String, index=True, unique=True)
    email = Column(String, unique=True, index=True)
    senha = Column(String)
    favorite_artist = Column(String, nullable=True)
    user_photo_url = Column(String, nullable=True)
    spotify_user_token = Column(String, nullable=True)
    spotify_refresh_token = Column(String, nullable=True)
    spotify_expires_at = Column(DateTime, nullable=True)
    
class Artist(base):
    __tablename__ = 'artist'
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    nome = Column(String)
    music_genre = Column(String)
    albums = relationship("Album", back_populates="criador")
    
class Album(base):
    __tablename__ = 'album'
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    artist_id = Column(Integer, ForeignKey('artist.id'))
    artist_name = Column(String)
    artist_genre = Column(String)
    album_name = Column(String)
    release_date = Column(DateTime)
    album_cover_url = Column(String)
    total_tracks = Column(Integer)
    
    criador = relationship("Artist", back_populates="albums")

class FriendRequest(base):
    __tablename__ = "friend_requests"

    id = Column(Integer, primary_key=True, index=True)

    sender_id = Column(Integer, ForeignKey("user.id"), nullable=False)
    receiver_id = Column(Integer, ForeignKey("user.id"), nullable=False)

    status = Column(String, default="Pending") #Isso pode ser Pending, Accepted, Denied,
    created_at = Column(DateTime, default=datetime.now)

    sender = relationship("User", foreign_keys=[sender_id])
    receiver = relationship("User", foreign_keys=[receiver_id])


class Friendship(base):
    __tablename__ = "friendship"

    id = Column(Integer, primary_key=True, index=True)
    user1_id = Column(Integer, ForeignKey("user.id"), nullable=False)
    user2_id = Column(Integer, ForeignKey("user.id"), nullable=False)

    created_at = Column(DateTime, default=datetime.now)

    __table_args__ = (
        UniqueConstraint("user1_id", "user2_id", name="unique_friendship"),
    )

class Notification(base):
    __tablename__ = "notifications"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("user.id"), nullable=False)

    type = Column(String)   #pode ser friend_request, system, message, e outras pombas para caso precise escalonar
    content = Column(String)
    read = Column(Boolean, default=False)

    created_at = Column(DateTime, default=datetime.now)

    user = relationship("User", foreign_keys=[user_id])


class FriendRequestHistory(base):
    __tablename__ = "friend_request_history"

    id = Column(Integer, primary_key=True, index=True)
    user1_id = Column(Integer, ForeignKey("user.id"), nullable=False)
    user2_id = Column(Integer, ForeignKey("user.id"), nullable=False)
    action = Column(String, nullable=False)  # "sent", "accepted", "denied", "friendship_removed"
    initiated_by = Column(Integer, ForeignKey("user.id"), nullable=False)  # who initiated this action
    created_at = Column(DateTime, default=datetime.now)

    user1 = relationship("User", foreign_keys=[user1_id])
    user2 = relationship("User", foreign_keys=[user2_id])
    initiator = relationship("User", foreign_keys=[initiated_by])