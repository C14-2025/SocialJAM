from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional

class UserCache(BaseModel):
    id: int = Field(alias='_id')
    name: str
    user_photo_url: Optional[str] = None
    updated_at: datetime