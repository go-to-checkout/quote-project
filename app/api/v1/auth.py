from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials

from app.core.security import (
    ACCESS_TOKEN_EXPIRE_MINUTES,
    add_token_to_blacklist,
    authenticate_user,
    create_access_token,
    get_current_user,
    get_password_hash,
    security,
)
from app.models.user import User
from app.schemas.auth import (
    UserLoginRequest,
    UserLoginResponse,
    UserResponse,
    UserSignupRequest,
    UserSignupResponse,
)
from app.schemas.base import ApiResponse

router = APIRouter(prefix="/auth", tags=["인증"])


@router.post(
    "/signup",
    response_model=ApiResponse[UserSignupResponse],
    status_code=status.HTTP_201_CREATED,
)
async def signup(user_data: UserSignupRequest):
    """회원가입"""

    # 사용자명 중복 확인
    existing_user = await User.get_or_none(username=user_data.username)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="이미 존재하는 사용자명입니다",
        )

    # 비밀번호 해싱
    hashed_password = get_password_hash(user_data.password)

    # 사용자 생성
    user = await User.create(username=user_data.username, password_hash=hashed_password)

    user_response = UserSignupResponse(user_id=user.id, username=user.username)

    return ApiResponse(success=True, message="회원가입이 완료되었습니다", data=user_response)


@router.post("/login", response_model=ApiResponse[UserLoginResponse])
async def login(user_data: UserLoginRequest):
    """로그인"""

    # 사용자 인증
    user = await authenticate_user(user_data.username, user_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="사용자명 또는 비밀번호가 잘못되었습니다",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # JWT 토큰 생성
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"user_id": user.id, "sub": user.username},
        expires_delta=access_token_expires,
    )

    login_response = UserLoginResponse(
        access_token=access_token,
        token_type="bearer",
        user_id=user.id,
        username=user.username,
    )

    return ApiResponse(success=True, message="로그인 성공", data=login_response)


@router.post("/logout", response_model=ApiResponse[None])
async def logout(
    current_user: User = Depends(get_current_user),
    credentials: HTTPAuthorizationCredentials = Depends(security),
):
    """로그아웃"""

    token = credentials.credentials

    # 토큰을 블랙리스트에 추가
    await add_token_to_blacklist(token, current_user.id)

    return ApiResponse(success=True, message="로그아웃되었습니다")


@router.get("/me", response_model=ApiResponse[UserResponse])
async def read_users_me(current_user: User = Depends(get_current_user)):
    """현재 사용자 정보 조회"""

    user_response = UserResponse(user_id=current_user.id, username=current_user.username)

    return ApiResponse(success=True, message="사용자 정보 조회 성공", data=user_response)
