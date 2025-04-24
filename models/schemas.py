from typing import List, Optional
from pydantic import BaseModel
from datetime import datetime

# Used for returning image data to the client
class ImageOut(BaseModel):
    id: int
    title: str
    author: str
    image: str
    tags: List[str]
    created_at: datetime
    class Config:
        orm_mode = True  # tells Pydantic to support SQLAlchemy models

# Used for updating image description/title
class ImageUpdate(BaseModel):
    title: str

class ImageCreate(BaseModel):
    image: str
    title: str
    author: str
    tags: List[str]