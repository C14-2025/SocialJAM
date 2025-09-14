import uvicorn
from app.api.routes_album import router as album_router
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.routes_user import router as user_router
from app.api.routes_artist import router as artist_router
from app.api.routes_posts import router as post_router
from app import models_sql as models
from app.database import engine
from app.core.mongo import connect_mongo, disconnect_mongo, get_mongo_db
from contextlib import asynccontextmanager


# connect to mongo db right after starting the server and disconnect before closing the server
@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        await connect_mongo()
        db = get_mongo_db()
        if db is None:
            raise RuntimeError('Falha ao inciar o mongo')

        await db.command('ping')
        yield
    finally:
        await disconnect_mongo()
    
app = FastAPI(
    title="SocialJAM",
    description="API para socializar baseado no seu gosto musical",
    lifespan=lifespan
)


origins = [
    "http://localhost:5173"
]

# adds the cors middleware responsible to menage the conection betwen front-end and back-end
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_methods=["*"],
    allow_headers=["*"],
)

models.base.metadata.create_all(engine)
app.include_router(user_router)
app.include_router(artist_router)
app.include_router(album_router)
app.include_router(post_router)

if __name__ == "__main__":
    uvicorn.run("main:app", port=8000, reload=True)
