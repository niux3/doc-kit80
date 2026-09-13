from typing import List, Optional
from sqlmodel import Field, SQLModel, Relationship


class LanguageBase(SQLModel):
    name: str = Field(unique=True)
    abbr: str = Field(index=True)


class Language(LanguageBase, table=True):
    __tablename__ = "documentation_languages"

    id: int = Field(default=None, primary_key=True)
    categories: List["Category"] = Relationship(back_populates="language")
    posts: List["Post"] = Relationship(back_populates="language")


class LanguageRead(LanguageBase):
    """Langage pour la lecture"""
    id: int


class LanguageCreate(LanguageBase):
    """Langage pour la création"""
    ...


class LanguageUpdate(LanguageBase):
    """Langage pour la modification"""
    name: Optional[str] = None
    abbr: Optional[str] = None
