from typing import List
from sqlmodel import Field, SQLModel, Relationship


class LanguageBase(SQLModel):
    name: str = Field(unique=True)
    abbr: str = Field(index=True)


class Language(LanguageBase, table=True):
    __tablename__ = "documentation_languages"

    id: int = Field(default=None, primary_key=True)
    categories: List["Category"] = Relationship(back_populates="language")
    posts: List["Post"] = Relationship(back_populates="language")
