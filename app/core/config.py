from dotenv import load_dotenv
import os

load_dotenv()

class Settings:
    APP_NAME:str=os.getenv("APP_NAME","FastAPI App")
    ENV:str=os.getenv("ENV","production")
    JWT_SECRET: str =os.getenv("JWT_SECRET","supersecret")
    JWT_ALGORITHM:str ="HS256"

settings=Settings()