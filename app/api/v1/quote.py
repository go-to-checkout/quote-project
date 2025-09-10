import random

from fastapi import APIRouter, Depends, HTTPException, status

from app.core.security import get_current_user
from app.models.quote import Bookmark, Quote
from app.models.user import User
from app.schemas.base import ApiResponse
from app.schemas.quote import (
    BookmarkedQuoteResponse,
    BookmarkListResponse,
    BookmarkRequest,
    BookmarkResponse,
    QuoteResponse,
    RandomQuoteResponse,
)

router = APIRouter(prefix="/quotes", tags=["명언"])


@router.get("/random", response_model=ApiResponse[RandomQuoteResponse])
async def get_random_quote(current_user: User = Depends(get_current_user)):
    """랜덤 명언 조회"""

    # 전체 명언 개수 확인
    total_quotes = await Quote.all().count()
    if total_quotes == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="등록된 명언이 없습니다")

    # 랜덤 오프셋으로 명언 선택
    random_offset = random.randint(0, total_quotes - 1)
    quote = await Quote.all().offset(random_offset).limit(1).first()

    # 북마크 여부 확인
    is_bookmarked = await Bookmark.filter(user_id=current_user.id, quote_id=quote.quote_id).exists()

    quote_response = RandomQuoteResponse(
        quote_id=quote.quote_id,
        content=quote.content,
        author=quote.author,
        is_bookmarked=is_bookmarked,
    )

    return ApiResponse(success=True, message="랜덤 명언 조회 성공", data=quote_response)


@router.post(
    "/bookmark",
    response_model=ApiResponse[BookmarkResponse],
    status_code=status.HTTP_201_CREATED,
)
async def add_bookmark(
    bookmark_data: BookmarkRequest, current_user: User = Depends(get_current_user)
):
    """명언 북마크 추가"""

    # 명언 존재 여부 확인
    quote = await Quote.get_or_none(quote_id=bookmark_data.quote_id)
    if not quote:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="명언을 찾을 수 없습니다")

    # 이미 북마크된 명언인지 확인
    existing_bookmark = await Bookmark.get_or_none(
        user_id=current_user.id, quote_id=bookmark_data.quote_id
    )
    if existing_bookmark:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="이미 북마크된 명언입니다"
        )

    # 북마크 생성
    bookmark = await Bookmark.create(user_id=current_user.id, quote_id=bookmark_data.quote_id)

    bookmark_response = BookmarkResponse(
        bookmark_id=bookmark.bookmark_id,
        user_id=bookmark.user_id,
        quote_id=bookmark.quote_id,
    )

    return ApiResponse(success=True, message="명언이 북마크되었습니다", data=bookmark_response)


@router.delete("/bookmark/{quote_id}", response_model=ApiResponse[None])
async def remove_bookmark(quote_id: int, current_user: User = Depends(get_current_user)):
    """북마크 제거"""

    # 북마크 조회
    bookmark = await Bookmark.get_or_none(user_id=current_user.id, quote_id=quote_id)
    if not bookmark:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="북마크를 찾을 수 없습니다"
        )

    # 북마크 삭제
    await bookmark.delete()

    return ApiResponse(success=True, message="북마크가 제거되었습니다")


@router.get("/bookmarks", response_model=ApiResponse[BookmarkListResponse])
async def get_my_bookmarks(
    skip: int = 0, limit: int = 10, current_user: User = Depends(get_current_user)
):
    """내 북마크 목록 조회"""

    # 사용자의 북마크 목록 조회
    bookmarks = (
        await Bookmark.filter(user_id=current_user.id)
        .offset(skip)
        .limit(limit)
        .order_by("-bookmark_id")
    )
    total = await Bookmark.filter(user_id=current_user.id).count()

    # 북마크된 명언 정보와 함께 반환
    bookmark_responses = []
    for bookmark in bookmarks:
        quote = await Quote.get(quote_id=bookmark.quote_id)
        quote_response = QuoteResponse(
            quote_id=quote.quote_id, content=quote.content, author=quote.author
        )
        bookmark_responses.append(
            BookmarkedQuoteResponse(bookmark_id=bookmark.bookmark_id, quote=quote_response)
        )

    list_response = BookmarkListResponse(bookmarks=bookmark_responses, total=total)

    return ApiResponse(success=True, message="북마크 목록 조회 성공", data=list_response)
