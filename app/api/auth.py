from fastapi import APIRouter,HTTPException
from passlib.context import CryptContext
from app.schemas.user import UserCreate,UserResponse
from app.models.user import users_db

router =APIRouter()

pwd_context=CryptContext(schemes=["argon2"],deprecated="auto")

@router.post("/register",response_model=UserResponse)
async def register(user:UserCreate):
    if user.email in users_db:
        raise HTTPException(status_code=400,detail="User Already Exits")
    hashed_password=pwd_context.hash(user.password)
    users_db[user.email]=hashed_password
    return UserResponse(email=user.email)