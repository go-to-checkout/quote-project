from datetime import datetime
from typing import Optional

from pydantic import BaseModel


# --- 사용자 회원가입 ---
class UserSignupRequest(BaseModel):
    username: str
    password: str


class UserSignupResponse(BaseModel):
    user_id: int
    username: str
    created_at: datetime = None


# --- 사용자 로그인 ---
class UserLoginRequest(BaseModel):
    username: str
    password: str


class UserLoginResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user_id: int
    username: str


# --- JWT 토큰 ---
class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    user_id: Optional[int] = None
    username: Optional[str] = None


# --- 사용자 정보 ---
class UserResponse(BaseModel):
    user_id: int
    username: str

    class Config:
        from_attributes = True
