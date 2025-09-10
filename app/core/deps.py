from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from starlette import status
from app.core.security import decode_token
from app.models.user import User
from app.models.token import RevokedToken
from app.models.diary import Diary

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

async def get_current_user(token: str = Depends(oauth2_scheme)) -> User:
    try:
        payload = decode_token(token)
    except Exception:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid or expired token")

    jti = payload.get("jti")
    if jti and await RevokedToken.filter(jti=jti).exists():
        raise HTTPException(status_code=401, detail="Token revoked")

    uid = payload.get("sub")
    user = await User.get_or_none(id=uid)
    if not user:
        raise HTTPException(status_code=401, detail="User not found")
    return user

async def ensure_diary_owner(diary_id: str, current: User = Depends(get_current_user)) -> Diary:
    d = await Diary.get_or_none(id=diary_id)
    if not d:
        raise HTTPException(status_code=404, detail="Diary not found")
    if str(d.user_id) != str(current.id):
        raise HTTPException(status_code=403, detail="Forbidden")
    return d
