from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional

class UserCache(BaseModel):
    id: str = Field(alias='_id')  # ObjectId do MongoDB como string
    sql_user_id: int  # ID do usuário no banco SQL
    name: str
    user_photo_url: Optional[str] = None
    updated_at: datetime
    
    class Config:
        populate_by_name = True