from fastapi import FastAPI
from contextlib import asynccontextmanager

from src.modules.books.router import book_router
from src.modules.authors.router import author_router
from src.modules.auth.router import auth_router
from src.modules.reviews.router import review_router
from src.modules.tags.router import tag_router
from src.database.main import init_db


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Iniciando la aplicacion")
    await init_db()
    yield
    print("Apagando la aplicacion")


version = "v1"

app = FastAPI(
    version=version,
    title="API de Libros",
    description="API para gestionar libros",
    lifespan=lifespan,
)

app.include_router(book_router, prefix=f"/api/{version}", tags=["Books"])
app.include_router(author_router, prefix=f"/api/{version}", tags=["Authors"])
app.include_router(auth_router, prefix=f"/api/{version}/auth", tags=["Auth"])
app.include_router(review_router, prefix=f"/api/{version}/reviews", tags=["Reviews"])
app.include_router(tag_router, prefix=f"/api/{version}/tags", tags=["Tags"])