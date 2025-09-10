from datetime import datetime

from pydantic import BaseModel


# --- 질문 조회 ---
class QuestionResponse(BaseModel):
    question_id: int
    question_text: str

    class Config:
        from_attributes = True


# --- 랜덤 질문 ---
class RandomQuestionResponse(BaseModel):
    question_id: int
    question_text: str


# --- 사용자 질문 기록 ---
class UserQuestionResponse(BaseModel):
    user_question_id: int
    question: QuestionResponse
    created_at: datetime = None
