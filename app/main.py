from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.core.config import settings
from app.db.session import engine


@asynccontextmanager
async def lifespan(app:FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(lambda _:None)
        print('App started successfully')
        yield
        print('App stopped successfully')
        
def create_app():
    app = FastAPI(title=settings.APP_NAME , lifespan=lifespan)
    @app.get('/health')
    async def health(): # type: ignore
        return {'status':'ok' }
    return app
app = create_app()