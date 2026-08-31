from fastapi import HTTPException
from fastapi.security import OAuth2PasswordRequestForm

from app.core.security import hash_password, create_access_token, verify_password

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.user import User
from app.schemas.user import UserCreate


def register(user_data: UserCreate, db: Session) -> User:
    existing_user = db.scalar(select(User).where(User.email == user_data.email))

    if existing_user is not None:
        raise HTTPException(status_code=400, detail="Email already registered")

    user = User(
        email=user_data.email, hashed_password=hash_password(user_data.password)
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    return user


def login(form_data: OAuth2PasswordRequestForm, db: Session):
    user = db.scalar(select(User).where(User.email == form_data.username))

    if user is None or not verify_password(
        form_data.password, str(user.hashed_password)
    ):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    access_token = create_access_token(user.id)

    return {"access_token": access_token, "token_type": "bearer"}
