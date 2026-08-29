from datetime import datetime, timedelta, timezone

from pwdlib import PasswordHash

from jwt import encode  # type: ignore[call-arg]

from app.core.config import settings

from typing import Any

ALGORITHM: str = "HS256"

password_hash = PasswordHash.recommended()


def hash_password(password: str) -> str:
    return password_hash.hash(password)


def verify_password(password: str, hashed_password: str) -> bool:
    return password_hash.verify(password, hashed_password)


def create_access_token(user_id: int, expires_minutes: int = 60) -> str:
    expire = datetime.now(timezone.utc) + timedelta(minutes=expires_minutes)

    payload: dict[str, Any] = {
        "sub": str(user_id),
        "exp": expire,
    }

    return encode(payload, settings.secret_key, algorithm=ALGORITHM)
