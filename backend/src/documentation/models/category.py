from typing import Optional, List
from pydantic import field_validator
from sqlmodel import Field, SQLModel, Relationship


class CategoryBase(SQLModel):
    name: str = Field(unique=True)
    description: Optional[str] = Field(default=None)
    lft: int = Field(default=0)
    rgt: int = Field(default=0)
    parent_id: Optional[int] = Field(
        default=None,
        foreign_key="documentation_categories.id"
    )
    language_id: Optional[int] = Field(
        default=None,
        foreign_key="documentation_languages.id"
    )


class Category(CategoryBase, table=True):
    __tablename__ = "documentation_categories"

    id: int = Field(default=None, primary_key=True)
    language: Optional["Language"] = Relationship(back_populates="categories")
    posts: List["Post"] = Relationship(back_populates="category")

    # Auto-relation pour l'arborescence (Parent / Enfants)
    parent: Optional["Category"] = Relationship(
        back_populates="children",
        sa_relationship_kwargs={"remote_side": "Category.id"}
    )
    children: List["Category"] = Relationship(back_populates="parent")


class CategoryRead(CategoryBase):
    """Catégorie pour la lecture"""
    id: int


class CategoryCreate(CategoryBase):
    """Catégorie pour la création"""
    @field_validator("parent_id", "language_id", mode="before")
    @classmethod
    def empty_or_zero_to_none(cls, v):
        if v == 0 or v == "" or v == "0":
            return None
        return v


class CategoryUpdate(CategoryBase):
    """Catégorie pour la modification"""
    name: Optional[str] = None
    description: Optional[str] = None
    lft: Optional[int] = None
    rgt: Optional[int] = None
    parent_id: Optional[int] = None
    language_id: Optional[int] = None
