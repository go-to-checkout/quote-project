from sqlalchemy.orm import Session
from app.repositories.question_repo import get_random_question

def fetch_random_question(session: Session, exclude_ids: list[int] = [], tag: str = None):
    question = get_random_question(session, exclude_ids, tag)
    if not question:
        return None
    tags = question.tags.split(",") if question.tags else []
    return {"id": question.id, "text": question.text, "tags": tags}
