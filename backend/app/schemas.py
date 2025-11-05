from typing import Optional, List
from pydantic import BaseModel, EmailStr
from datetime import datetime

class User(BaseModel):
    username: str
    nome: Optional[str] = None
    senha: str
    email: EmailStr
    
class ShowUser(BaseModel):
    username: str
    nome: str
    email: str
    photo: Optional[str] = None
    favorite_artist: Optional[str] = None
    class Config:
        orm_mode = True
    
class Artist(BaseModel):
    nome: str
    music_genre: str
    
    
class Album(BaseModel):
    nome:str
    total_tracks: int
    artist_id : int
    
class ShowArtist(Artist):
    albums: List[Album]
    class Config:
        orm_mode=True


class Login(BaseModel):
    username_email: str
    senha: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None
    email: Optional[str] = None

class FavoriteArtist(BaseModel):
    artist_id: str


class FriendRequestBase(BaseModel):
    sender_id: int
    receiver_id: int

class FriendRequestOut(BaseModel):
    id: int
    sender_id: int
    receiver_id: int
    status: str
    created_at: datetime

    class Config:
        orm_mode = True


class FriendshipOut(BaseModel):
    id: int
    user1_id: int
    user2_id: int
    created_at: datetime

    class Config:
        orm_mode = True

class NotificationOut(BaseModel):
    id: int
    type: str
    content: str
    read: bool
    created_at: datetime

    class Config:
        orm_mode = True

class FriendRequestCreate(BaseModel):
    receiver_id: int

class FriendRequestResponse(BaseModel):
    response: str  # "accepted" or "denied"