import os
from datetime import datetime, timedelta
from typing import Optional

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import JWTError, jwt
from passlib.context import CryptContext

# 환경 변수에서 비밀키 가져오기
SECRET_KEY = os.getenv("SECRET_KEY", "your-secret-key-here-change-in-production")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# 패스워드 해싱 설정
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# HTTP Bearer 인증 설정
security = HTTPBearer()


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """비밀번호 검증"""
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    """비밀번호 해싱"""
    return pwd_context.hash(password)


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    """JWT 액세스 토큰 생성"""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def verify_token(token: str) -> Optional[dict]:
    """JWT 토큰 검증"""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: int = payload.get("user_id")
        username: str = payload.get("sub")
        if user_id is None or username is None:
            return None
        return {"user_id": user_id, "username": username}
    except JWTError:
        return None


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
):
    """현재 인증된 사용자 정보 가져오기"""
    from app.models.user import TokenBlacklist, User

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="인증 정보를 확인할 수 없습니다",
        headers={"WWW-Authenticate": "Bearer"},
    )

    token = credentials.credentials

    # 토큰 블랙리스트 확인
    blacklisted_token = await TokenBlacklist.filter(token=token).first()
    if blacklisted_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="만료된 토큰입니다",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # 토큰 검증
    payload = verify_token(token)
    if payload is None:
        raise credentials_exception

    user_id = payload.get("user_id")
    user = await User.get_or_none(id=user_id)  # user_id=user_id -> id=user_id
    if user is None:
        raise credentials_exception

    return user


async def authenticate_user(username: str, password: str):
    """사용자 인증"""
    from app.models.user import User

    user = await User.get_or_none(username=username)
    if not user:
        return False
    if not verify_password(password, user.password_hash):
        return False
    return user


async def add_token_to_blacklist(token: str, user_id: int):
    """토큰을 블랙리스트에 추가 (로그아웃)"""
    from app.models.user import TokenBlacklist

    # 토큰에서 만료 시간 추출
    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    expire_timestamp = payload.get("exp")
    expire_datetime = datetime.utcfromtimestamp(expire_timestamp)

    # 블랙리스트에 추가
    await TokenBlacklist.create(token=token, user_id=user_id, expired_at=expire_datetime)
