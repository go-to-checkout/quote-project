from pydantic import BaseModel
from typing import List

class QuestionOut(BaseModel):
    id: int
    text: str
    tags: List[str] = []
