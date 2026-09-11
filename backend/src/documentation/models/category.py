from typing import Optional, List
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
