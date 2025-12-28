from fastapi import APIRouter,HTTPException,Depends,Security
from passlib.context import CryptContext
from app.schemas.user import UserCreate,UserResponse,Token,UserLogin
from app.models.user import users_db
from jose import jwt
from datetime import datetime,timedelta,timezone
from app.core.config import settings
from fastapi.security import HTTPBearer,HTTPAuthorizationCredentials

security=HTTPBearer()

router =APIRouter()

pwd_context=CryptContext(schemes=["argon2"],deprecated="auto")

def get_current_user(credentials:HTTPAuthorizationCredentials=Depends(security)):
    token=credentials.credentials
    try:
        payload=jwt.decode(token,settings.JWT_SECRET,algorithms=[settings.JWT_ALGORITHM])
        user_email=payload.get("sub")
        if user_email is None:
            raise HTTPException(status_code=401,details="Invalid token")
        return user_email
    except Exception:
        raise HTTPException(status_code=401,details="Invalid token")
    

@router.post("/register",response_model=UserResponse)
async def register(user:UserCreate):
    if user.email in users_db:
        raise HTTPException(status_code=400,detail="User Already Exits")
    hashed_password=pwd_context.hash(user.password)
    users_db[user.email]=hashed_password
    return UserResponse(email=user.email)

@router.post("/login",response_model=Token)
async def login(user:UserLogin):
    #Check user Exits
    if user.email not in users_db:
        raise HTTPException(status_code=400,detail="Invalid credentials")
    hashed_password=users_db[user.email]

    #Verify Password
    if not pwd_context.verify(user.password,hashed_password):
        raise HTTPException(status_code=400,detail="Invalid credentials")
    
    #Create JWT
    payload={
        "sub":user.email,
        "exp":datetime.now(timezone.utc)+timedelta(minutes=30)
    }
    
    token= jwt.encode(payload,settings.JWT_SECRET,algorithm=settings.JWT_ALGORITHM)

    return Token(access_token=token)


@router.get("/me")
async def get_me(current_user: str = Depends(get_current_user)):
    return {"email": current_user}