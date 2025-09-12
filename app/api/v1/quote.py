from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel
from typing import List, Optional
import random

app = FastAPI(title="Self-Reflection Questions (Prototype)")

# --- Pydantic models (요청/응답 검증용) ---
class Question(BaseModel):
    id: int
    text: str
    tags: Optional[List[str]] = []

class RandomQuestionResponse(BaseModel):
    question: Question

# --- 데이터 (샘플) ---
QUESTIONS = [
    {"id": 1, "text": "오늘 내가 감사했던 일은 무엇인가?", "tags": ["gratitude"]},
    {"id": 2, "text": "지난 한 달 동안 내가 가장 성장한 점은?", "tags": ["growth"]},
    {"id": 3, "text": "지금의 목표가 진짜 나의 목표인지 어떻게 확인할까?", "tags": ["goal"]},
    # ... 더 추가
]

# --- 랜덤 질문 제공 엔드포인트 ---
@app.get("/reflection/random", response_model=RandomQuestionResponse)
def get_random_question(exclude_ids: Optional[str] = Query(None, description="콤마로 구분된 제외할 질문 id들 (예: 1,2,3)"),
                        tag: Optional[str] = Query(None, description="특정 태그 필터링")):
    exclude_set = set()
    if exclude_ids:
        try:
            exclude_set = set(int(x) for x in exclude_ids.split(",") if x.strip())
        except ValueError:
            raise HTTPException(status_code=400, detail="exclude_ids는 정수 ID의 콤마 리스트여야 합니다.")
    # 필터링
    candidates = [q for q in QUESTIONS if q["id"] not in exclude_set]
    if tag:
        candidates = [q for q in candidates if tag in q.get("tags", [])]
    if not candidates:
        raise HTTPException(status_code=404, detail="조건에 맞는 질문이 없습니다.")
    chosen = random.choice(candidates)
    return {"question": chosen}


