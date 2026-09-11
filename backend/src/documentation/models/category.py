from typing import Optional
from pydantic import BaseModel, Field


class CategoryBase(BaseModel):
    name: str
    description: Optional[str] = None
    lft: int
    rgt: int
    parent_id: Optional[int] = None


class Category(CategoryBase):
    id: int

    class Config:
        from_attributes = True
