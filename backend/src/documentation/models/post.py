from typing import Optional
from datetime import datetime
from sqlmodel import Field, SQLModel, Relationship, TEXT
from src.documentation.models import LanguageRead, CategoryRead


class PostBase(SQLModel):
    title: str = Field(unique=True)
    slug: str = Field(unique=True)
    content: str = Field(default="", sa_type=TEXT)
    online: bool = Field(default=True)
    category_id: Optional[int] = Field(
        default=None,
        foreign_key="documentation_categories.id"
    )
    language_id: Optional[int] = Field(
        default=None,
        foreign_key="documentation_languages.id"
    )


class Post(PostBase, table=True):
    __tablename__ = "documentation_posts"

    id: int = Field(default=None, primary_key=True)
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)
    category: Optional["Category"] = Relationship(back_populates="posts")
    language: Optional["Language"] = Relationship(back_populates="posts")


class PostRead(PostBase):
    """Post pour la lecture"""
    id: int
    language: Optional[LanguageRead] = None
    category: Optional[CategoryRead] = None


class PostCreate(PostBase):
    """Post pour la création"""
    ...


class PostUpdate(PostBase):
    """Post pour la modification"""
    title: Optional[str] = None
    slug: Optional[str] = None
    content: Optional[str] = None
    online: Optional[bool] = None
    category_id: Optional[int] = None
    language_id: Optional[int] = None
