from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime

class PostCreate(BaseModel):
    author_id: str 
    content: str
    artist_id: str
    images: Optional[List[str]] = []

class PostDB(PostCreate):
    id: str = Field(alias='_id')
    likes: int = 0
    liked_by: List[str] = []
    created_at: datetime

class CommentCreate(BaseModel):
    post_id: str
    author_id: str
    content: str

class CommentDB(CommentCreate):
    id: str = Field(alias="_id")
    likes: int = 0
    liked_by: List[str] = []
    created_at: datetime