from fastapi import FastAPI

from src.auth.router import router as user_router
from src.library.routers.genre import router as genre_router
from src.library.routers.author import router as author_router
from src.library.routers.book import router as book_router
from src.library.routers.automation import router as automation_router


app = FastAPI()
app.include_router(
    user_router,
    prefix="/users",
    tags=["users"]
)
app.include_router(
    genre_router,
    prefix="/genres",
    tags=["genres"],
)
app.include_router(
    author_router,
    prefix="/authors",
    tags=["authors"]
)
app.include_router(
    book_router,
    prefix="/books",
    tags=["books"]
)
app.include_router(
    automation_router,
    prefix="/automations",
    tags=["automations"]
)
