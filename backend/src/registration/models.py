from typing import Optional
from sqlmodel import Field, SQLModel


class UserBase(SQLModel):
    username: str = Field(unique=True)
    email: str = Field(unique=True)
    is_active: bool = Field(default=True)


class User(UserBase, table=True):
    __tablename__ = "registration_users"

    id: int = Field(default=None, primary_key=True)
    firstname: Optional[str] = Field(default=None)
    lastname: Optional[str] = Field(default=None)
    hashed_password: str = Field(nullable=False)


class UserCreate(UserBase):
    password: str  # Mot de passe en clair envoyé par le client HTTP


class UserRead(UserBase):
    id: int
    firstname: Optional[str] = None
    lastname: Optional[str] = None
