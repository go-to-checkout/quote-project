# api/v1/diary.py
from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException, status

from app.core.security import get_current_user
from app.models.diary import Diary
from app.models.user import User
from app.schemas.base import ApiResponse
from app.schemas.diary import (
    DiaryCreateRequest,
    DiaryCreateResponse,
    DiaryListResponse,
    DiaryResponse,
    DiaryUpdateRequest,
    DiaryUpdateResponse,
)

router = APIRouter(prefix="/diaries", tags=["일기"])


@router.post(
    "",
    response_model=ApiResponse[DiaryCreateResponse],
    status_code=status.HTTP_201_CREATED,
)
async def create_diary(
    diary_data: DiaryCreateRequest, current_user: User = Depends(get_current_user)
):
    """일기 작성"""

    # 일기 생성
    diary = await Diary.create(
        title=diary_data.title,
        content=diary_data.content,
        user_id=current_user.id,
        created_at=datetime.utcnow(),
    )

    diary_response = DiaryCreateResponse(
        diary_id=diary.diary_id,
        title=diary.title,
        content=diary.content,
        user_id=diary.user_id,
        created_at=diary.created_at,
    )

    return ApiResponse(success=True, message="일기가 작성되었습니다", data=diary_response)


@router.get("", response_model=ApiResponse[DiaryListResponse])
async def get_my_diaries(
    skip: int = 0, limit: int = 10, current_user: User = Depends(get_current_user)
):
    """내 일기 목록 조회"""

    # 사용자의 일기 목록 조회
    diaries = (
        await Diary.filter(user_id=current_user.id)
        .offset(skip)
        .limit(limit)
        .order_by("-created_at")
    )
    total = await Diary.filter(user_id=current_user.id).count()

    diary_responses = [
        DiaryResponse(
            diary_id=diary.diary_id,
            title=diary.title,
            content=diary.content,
            user_id=diary.user_id,
            created_at=diary.created_at,
        )
        for diary in diaries
    ]

    list_response = DiaryListResponse(diaries=diary_responses, total=total)

    return ApiResponse(success=True, message="일기 목록 조회 성공", data=list_response)


@router.get("/{diary_id}", response_model=ApiResponse[DiaryResponse])
async def get_diary(diary_id: int, current_user: User = Depends(get_current_user)):
    """특정 일기 조회"""

    # 일기 조회 및 권한 확인
    diary = await Diary.get_or_none(diary_id=diary_id, user_id=current_user.id)
    if not diary:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="일기를 찾을 수 없습니다")

    diary_response = DiaryResponse(
        diary_id=diary.diary_id,
        title=diary.title,
        content=diary.content,
        user_id=diary.user_id,
        created_at=diary.created_at,
    )

    return ApiResponse(success=True, message="일기 조회 성공", data=diary_response)


@router.put("/{diary_id}", response_model=ApiResponse[DiaryUpdateResponse])
async def update_diary(
    diary_id: int,
    diary_data: DiaryUpdateRequest,
    current_user: User = Depends(get_current_user),
):
    """일기 수정"""

    # 일기 조회 및 권한 확인
    diary = await Diary.get_or_none(diary_id=diary_id, user_id=current_user.id)
    if not diary:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="일기를 찾을 수 없습니다")

    # 수정할 필드만 업데이트
    update_data = diary_data.dict(exclude_unset=True)
    if not update_data:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="수정할 내용이 없습니다"
        )

    # 일기 업데이트
    await diary.update_from_dict(update_data)
    await diary.save()

    diary_response = DiaryUpdateResponse(
        diary_id=diary.diary_id,
        title=diary.title,
        content=diary.content,
        user_id=diary.user_id,
        created_at=diary.created_at,
    )

    return ApiResponse(success=True, message="일기가 수정되었습니다", data=diary_response)


@router.delete("/{diary_id}", response_model=ApiResponse[None])
async def delete_diary(diary_id: int, current_user: User = Depends(get_current_user)):
    """일기 삭제"""

    # 일기 조회 및 권한 확인
    diary = await Diary.get_or_none(diary_id=diary_id, user_id=current_user.id)
    if not diary:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="일기를 찾을 수 없습니다")

    # 일기 삭제
    await diary.delete()

    return ApiResponse(success=True, message="일기가 삭제되었습니다")
