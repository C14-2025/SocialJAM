from typing import Optional, List
from pydantic import BaseModel, EmailStr

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