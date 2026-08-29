from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.security import hash_password, create_access_token, verify_password
from app.db.database import get_db
from app.models.user import User
from app.schemas.user import UserCreate, UserResponse, Token

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register", response_model=UserResponse)
def register(user_data: UserCreate, db: Session = Depends(get_db)):
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


@router.post("/login", response_model=Token)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)
):
    user = db.scalar(select(User).where(User.email == form_data.username))

    if user is None or not verify_password(
        form_data.password, str(user.hashed_password)
    ):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    access_token = create_access_token(user.id)

    return {"access_token": access_token, "token_type": "bearer"}
