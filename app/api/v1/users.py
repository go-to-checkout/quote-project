from typing import List

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from tortoise.exceptions import DoesNotExist

from app.models import User

router = APIRouter()


class UserCreate(BaseModel):
    username: str
    email: str
    password: str


class UserResponse(BaseModel):
    id: int
    username: str
    email: str
    is_active: bool

    class Config:
        from_attributes = True


@router.post("/users/", response_model=UserResponse)
async def create_user(user_data: UserCreate):
    # 비밀번호 해싱은 실제로는 보안 모듈에서 처리
    user = await User.create(
        username=user_data.username,
        email=user_data.email,
        password_hash=f"hashed_{user_data.password}",  # 실제로는 해싱 필요
    )
    return UserResponse.from_orm(user)


@router.get("/users/", response_model=List[UserResponse])
async def get_users():
    users = await User.all()
    return [UserResponse.from_orm(user) for user in users]


@router.get("/users/{user_id}", response_model=UserResponse)
async def get_user(user_id: int):
    try:
        user = await User.get(id=user_id)
        return UserResponse.from_orm(user)
    except DoesNotExist:
        raise HTTPException(status_code=404, detail="User not found")
