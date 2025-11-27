# src/schemas/user.py

from pydantic import BaseModel


class UserBase(BaseModel):
    username: str


class UserCreate(UserBase):
    password: str


class UserRead(UserBase):
    id: int

    class Config:
        from_attributes = True  # pydantic v2 (antes era orm_mode = True)


class UserLogin(BaseModel):
    username: str
    password: str
