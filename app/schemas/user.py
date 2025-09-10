from pydantic import BaseModel, EmailStr, Field
from uuid import UUID

class RegisterIn(BaseModel):
    email: EmailStr
    password: str = Field(min_length=4)
    nickname: str | None = None

class LoginIn(BaseModel):
    email: EmailStr
    password: str

class TokenOut(BaseModel):
    access_token: str
    token_type: str = "bearer"

class MeOut(BaseModel):
    id: UUID
    email: EmailStr
    nickname: str | None = None
