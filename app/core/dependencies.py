from fastapi import Depends

from app.core.security import get_current_user
from app.models.user import User


async def get_current_active_user(
    current_user: User = Depends(get_current_user),
) -> User:
    """활성화된 사용자만 허용"""
    # User 모델에 is_active 필드가 없으므로 모든 사용자를 활성화된 것으로 간주
    return current_user
