from dotenv import load_dotenv
import os

load_dotenv()

class Settings:
    APP_NAME:str=os.getenv("APP_NAME","FastAPI App")
    ENV:str=os.getenv("ENV","production")

settings=Settings()