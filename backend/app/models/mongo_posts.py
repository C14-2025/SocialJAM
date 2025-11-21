from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime

class PostCreate(BaseModel):
    author_id: str 
    artist_id: str  # ID do artista do Spotify
    content: str
    images: Optional[List[str]] = []

class AuthorInfo(BaseModel):
    name: str
    user_photo_url: Optional[str] = None

class PostDB(PostCreate):
    id: str = Field(alias='_id')
    likes: int = 0
    liked_by: List[str] = []
    created_at: datetime
    author: Optional[AuthorInfo] = None  # Informações do autor populadas pelo lookup
    
    class Config:
        populate_by_name = True

class CommentCreate(BaseModel):
    post_id: str
    author_id: str
    content: str

class CommentDB(CommentCreate):
    id: str = Field(alias="_id")
    likes: int = 0
    liked_by: List[str] = []
    created_at: datetime