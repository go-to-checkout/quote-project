# app/api/v1/auth.py
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from app.schemas.user import RegisterIn, TokenOut, MeOut  # LoginIn은 이제 안 써도 됩니다
from app.services.auth import login
from app.api.v1.deps import get_current_user  # 이미 있다면 OK
from app.models.user import User

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/register")
async def register_user(payload: RegisterIn):
    # ... 기존 로직 그대로

@router.post("/login", response_model=TokenOut)
async def login_user(form_data: OAuth2PasswordRequestForm = Depends()):
    try:
        token = await login(form_data.username, form_data.password)
    except ValueError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    return {"access_token": token}

@router.get("/me", response_model=MeOut)
async def me(current: User = Depends(get_current_user)):
    return {"id": current.id, "email": current.email, "nickname": current.nickname}
