from datetime import datetime
from typing import Optional

from pydantic import BaseModel


# --- 일기 작성 ---
class DiaryCreateRequest(BaseModel):
    title: str
    content: str


class DiaryCreateResponse(BaseModel):
    diary_id: int
    title: str
    content: str
    user_id: int
    created_at: datetime


# --- 일기 수정 ---
class DiaryUpdateRequest(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None


class DiaryUpdateResponse(BaseModel):
    diary_id: int
    title: str
    content: str
    user_id: int
    created_at: datetime


# --- 일기 조회 ---
class DiaryResponse(BaseModel):
    diary_id: int
    title: str
    content: str
    user_id: int
    created_at: datetime

    class Config:
        from_attributes = True


# --- 일기 목록 ---
class DiaryListResponse(BaseModel):
    diaries: list[DiaryResponse]
    total: int
