from fastapi import FastAPI

from src.database.database import SessionLocal
from src.api.controllers.user_controller import router as user_router
from src.api.controllers.book_controller import router as book_router
from src.api.controllers.rating_controller import router as rating_router


app = FastAPI(title="Book Recommender API")

app.include_router(user_router)
app.include_router(book_router)
app.include_router(rating_router) 


