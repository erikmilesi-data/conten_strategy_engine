# src/schemas/auth.py
from pydantic import BaseModel


class LoginPayload(BaseModel):
    username: str
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
    username: str
