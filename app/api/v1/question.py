from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List
from app.schemas.question import QuestionOut
from app.services.question_service import fetch_random_question
from app.db.session import get_session

router = APIRouter(prefix="/question", tags=["question"])

@router.get("/random", response_model=QuestionOut)
def get_random_question_api(
    exclude_ids: str = Query(None, description="콤마로 구분된 제외할 질문 id"),
    tag: str = Query(None, description="태그 필터"),
    session: Session = Depends(get_session)
):
    exclude_list = [int(x) for x in exclude_ids.split(",")] if exclude_ids else []
    question = fetch_random_question(session, exclude_list, tag)
    if not question:
        raise HTTPException(status_code=404, detail="조건에 맞는 질문이 없습니다.")
    return question
