# models/__init__.py
from .diary import Diary
from .question import Question, UserQuestion
from .quote import Bookmark, Quote
from .user import TokenBlacklist, User

__all__ = [
    "User",
    "TokenBlacklist",
    "Diary",
    "Quote",
    "Bookmark",
    "Question",
    "UserQuestion",
]
