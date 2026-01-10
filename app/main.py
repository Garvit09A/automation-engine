from fastapi import FastAPI
from app.core.config import settings
from app.api import auth
from app.api import workflows
app=FastAPI(title=settings.APP_NAME)

app.include_router(auth.router,prefix="/auth")
app.include_router(workflows.router, prefix="/workflows")

@app.get('/health')
async def health_check():
    return {'status':'ok',
            'environment':settings.ENV}
