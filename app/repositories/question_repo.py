from sqlmodel import Session, select
from app.models.question import ReflectionQuestion
import random
from typing import List, Optional

def get_random_question(
    session: Session,
    exclude_ids: Optional[List[int]] = None,
    tag: Optional[str] = None
) -> Optional[ReflectionQuestion]:
    stmt = select(ReflectionQuestion)
    if exclude_ids:
        stmt = stmt.where(ReflectionQuestion.id.notin_(exclude_ids))
    if tag:
        stmt = stmt.where(ReflectionQuestion.tags.like(f"%{tag}%"))

    results = session.exec(stmt).all()
    if not results:
        return None
    return random.choice(results)
