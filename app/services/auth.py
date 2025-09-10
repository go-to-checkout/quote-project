from datetime import datetime, timezone
from tortoise.transactions import in_transaction
from app.models.user import User
from app.models.token import RevokedToken
from app.core.security import hash_password, verify_password, create_access_token, decode_token

async def register(email: str, password: str, nickname: str | None):
    async with in_transaction():
        exists = await User.filter(email=email).exists()
        if exists:
            raise ValueError("email_exists")
        user = await User.create(email=email, password_hash=hash_password(password), nickname=nickname)
        return user

async def login(email: str, password: str) -> str:
    user = await User.get_or_none(email=email)
    if not user or not verify_password(password, user.password_hash):
        raise ValueError("bad_credentials")
    return create_access_token(str(user.id))

async def logout(token: str):
    payload = decode_token(token)
    jti = payload.get("jti")
    exp = payload.get("exp")
    if not jti or not exp:
        return
    expires_at = datetime.fromtimestamp(exp, tz=timezone.utc)
    await RevokedToken.get_or_create(jti=jti, defaults={"expires_at": expires_at})
