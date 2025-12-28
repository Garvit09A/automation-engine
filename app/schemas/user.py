from pydantic import BaseModel,EmailStr

class UserCreate(BaseModel):
    email :EmailStr
    password: str

class UserResponse(BaseModel):
    email:EmailStr

class Token(BaseModel):
    access_token:str
    token_type:str ='bearer'

class UserLogin(BaseModel):
    email: EmailStr
    password: str