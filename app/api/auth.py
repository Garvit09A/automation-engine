from fastapi import APIRouter, HTTPException, Depends
from passlib.context import CryptContext
from datetime import datetime, timedelta, timezone
from jose import jwt

from app.schemas.user import UserCreate, UserResponse, Token, UserLogin
from app.models.user import users_db
from app.core.config import settings
from app.dependencies.auth import get_current_user

router = APIRouter()
pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")

@router.post("/register", response_model=UserResponse)
async def register(user: UserCreate):
    if user.email in users_db:
        raise HTTPException(status_code=400, detail="User already exists")

    hashed_password = pwd_context.hash(user.password)
    users_db[user.email] = hashed_password
    return UserResponse(email=user.email)

@router.post("/login", response_model=Token)
async def login(user: UserLogin):
    if user.email not in users_db:
        raise HTTPException(status_code=400, detail="Invalid credentials")

    hashed_password = users_db[user.email]

    if not pwd_context.verify(user.password, hashed_password):
        raise HTTPException(status_code=400, detail="Invalid credentials")

    payload = {
        "sub": user.email,
        "exp": datetime.now(timezone.utc) + timedelta(minutes=30)
    }

    token = jwt.encode(
        payload,
        settings.JWT_SECRET,
        algorithm=settings.JWT_ALGORITHM
    )

    return Token(access_token=token)

@router.get("/me")
async def get_me(current_user: str = Depends(get_current_user)):
    return {"email": current_user}
