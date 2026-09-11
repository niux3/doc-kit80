from typing import Optional, List
from datetime import datetime
from pydantic import BaseModel
from category import Category


class PostBase(BaseModel):
    title: str
    slug: str
    content: str
    category_id: int  # Clé étrangère logique pour la création / mise à jour


class Post(PostBase):
    id: int
    created_at: datetime
    updated_at: datetime
    category: Optional[Category] = None  # Relation imbriquée pour la lecture

    class Config:
        from_attributes = True
