from sqlmodel import SQLModel, Field
from typing import Optional

class ReflectionQuestion(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    text: str
    tags: Optional[str] = None  # "습관,성장" 같은 CSV 문자열 저장
