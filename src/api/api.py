from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.database.database import SessionLocal
from src.api.controllers.user_controller import router as user_router
from src.api.controllers.book_controller import router as book_router
from src.api.controllers.rating_controller import router as rating_router
from src.api.controllers.recommendation_controller import router as recommendation_router
from sqlalchemy import text

app = FastAPI(title="Book Recommender API")

@app.on_event("startup")
def startup():
    db = SessionLocal()
    try:
        db.execute(text("PRAGMA journal_mode=WAL;"))
        db.execute(text("PRAGMA synchronous=NORMAL;"))
        db.execute(text("PRAGMA busy_timeout=30000;"))
    finally:
        db.close()

origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,     
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(user_router)
app.include_router(book_router)
app.include_router(rating_router) 
app.include_router(recommendation_router)


