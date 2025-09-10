from datetime import datetime
from typing import Optional

from pydantic import BaseModel


# --- 명언 조회 ---
class QuoteResponse(BaseModel):
    quote_id: int
    content: str
    author: Optional[str] = None

    class Config:
        from_attributes = True


# --- 랜덤 명언 ---
class RandomQuoteResponse(BaseModel):
    quote_id: int
    content: str
    author: Optional[str] = None
    is_bookmarked: bool = False


# --- 북마크 추가/제거 ---
class BookmarkRequest(BaseModel):
    quote_id: int


class BookmarkResponse(BaseModel):
    bookmark_id: int
    user_id: int
    quote_id: int
    created_at: datetime = None


# --- 북마크 목록 ---
class BookmarkedQuoteResponse(BaseModel):
    bookmark_id: int
    quote: QuoteResponse
    created_at: datetime = None


class BookmarkListResponse(BaseModel):
    bookmarks: list[BookmarkedQuoteResponse]
    total: int
