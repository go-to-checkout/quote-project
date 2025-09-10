import random

from fastapi import APIRouter, Depends, HTTPException, status

from app.core.security import get_current_user
from app.models.question import Question, UserQuestion
from app.models.user import User
from app.schemas.base import ApiResponse
from app.schemas.question import (
    QuestionResponse,
    RandomQuestionResponse,
    UserQuestionResponse,
)

router = APIRouter(prefix="/questions", tags=["질문"])


@router.get("/random", response_model=ApiResponse[RandomQuestionResponse])
async def get_random_question(current_user: User = Depends(get_current_user)):
    """랜덤 자기성찰 질문 조회"""

    # 전체 질문 개수 확인
    total_questions = await Question.all().count()
    if total_questions == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="등록된 질문이 없습니다")

    # 랜덤 오프셋으로 질문 선택
    random_offset = random.randint(0, total_questions - 1)
    question = await Question.all().offset(random_offset).limit(1).first()

    # 사용자 질문 기록에 추가
    await UserQuestion.create(user_id=current_user.id, question_id=question.question_id)

    question_response = RandomQuestionResponse(
        question_id=question.question_id, question_text=question.question_text
    )

    return ApiResponse(success=True, message="랜덤 질문 조회 성공", data=question_response)


@router.get("/history", response_model=ApiResponse[list[UserQuestionResponse]])
async def get_question_history(
    skip: int = 0, limit: int = 10, current_user: User = Depends(get_current_user)
):
    """내가 받은 질문 기록 조회"""

    # 사용자의 질문 기록 조회
    user_questions = (
        await UserQuestion.filter(user_id=current_user.id)
        .offset(skip)
        .limit(limit)
        .order_by("-user_question_id")
    )

    # 질문 정보와 함께 반환
    question_responses = []
    for user_question in user_questions:
        question = await Question.get(question_id=user_question.question_id)
        question_response = QuestionResponse(
            question_id=question.question_id, question_text=question.question_text
        )
        question_responses.append(
            UserQuestionResponse(
                user_question_id=user_question.user_question_id,
                question=question_response,
            )
        )

    return ApiResponse(success=True, message="질문 기록 조회 성공", data=question_responses)


@router.get("/all", response_model=ApiResponse[list[QuestionResponse]])
async def get_all_questions(
    skip: int = 0, limit: int = 50, current_user: User = Depends(get_current_user)
):
    """모든 질문 목록 조회 (관리용)"""

    questions = await Question.all().offset(skip).limit(limit).order_by("question_id")

    question_responses = [
        QuestionResponse(question_id=question.question_id, question_text=question.question_text)
        for question in questions
    ]

    return ApiResponse(success=True, message="전체 질문 조회 성공", data=question_responses)
