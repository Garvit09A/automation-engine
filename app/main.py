from fastapi import FastAPI

app=FastAPI(title="Automation Engine")

@app.get('/health')
async def health_check():
    return {'status':'ok'}
