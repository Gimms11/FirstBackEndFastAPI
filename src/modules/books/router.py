from fastapi import APIRouter, HTTPException, status, Depends
from sqlmodel.ext.asyncio.session import AsyncSession
from uuid import UUID

from src.modules.books.schemas import BookSchema, BookCreateModel, BookUpdate, GetBooksResponse, BookResponse
from src.modules.books.service import BookService
from src.core.dependencies import RoleChecker
from src.modules.auth.models import UserRole
from src.core.security import AccessTokenBearer
from src.database.main import get_session

book_router = APIRouter()
access_token_bearer = AccessTokenBearer()
book_service = BookService()

# ── Guards de rol ─────────────────────────────────────────
# Crear / Editar: admins y pro_users
_can_write = Depends(RoleChecker([UserRole.ADMIN, UserRole.PRO_USER]))
# Eliminar: solo admins
_can_delete = Depends(RoleChecker([UserRole.ADMIN]))


@book_router.get("/books", response_model=GetBooksResponse, status_code=status.HTTP_200_OK)
async def get_books(session: AsyncSession = Depends(get_session)) -> dict:
    """Obtiene la lista de todos los libros disponibles. Público."""
    books = await book_service.get_all_books(session)
    return {"total_books": len(books), "books": books}


@book_router.get("/book/{book_id}", response_model=BookResponse, status_code=status.HTTP_200_OK)
async def get_book(book_id: str, session: AsyncSession = Depends(get_session)) -> dict:
    """Busca un libro específico por su ID. Público."""
    book = await book_service.get_book_by_id(session, UUID(book_id))
    if not book:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Libro no encontrado")
    return {"message": "Libro encontrado", "book": book}


@book_router.post("/book", response_model=BookResponse, status_code=status.HTTP_201_CREATED,
                  dependencies=[_can_write])
async def create_book(
    book_data: BookCreateModel,
    session: AsyncSession = Depends(get_session),
    token_details: dict = Depends(access_token_bearer)
) -> dict:
    """Crea un nuevo libro. Requiere rol ADMIN o PRO_USER."""
    books = await book_service.get_all_books(session)
    
    if any(b.title == book_data.title for b in books):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="El libro ya existe.")
    
    user = token_details.get("user", {})
    user_uid = user.get("user_uid")
    if not user_uid:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token inválido, falta user_uid")
    
    new_book = await book_service.create_book(session, book_data, user_uid)
    
    if not new_book:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Autor no encontrado")
    
    return {"message": "Libro creado exitosamente", "book": new_book}


@book_router.patch("/book/{book_id}", response_model=BookResponse, status_code=status.HTTP_200_OK,
                   dependencies=[_can_write])
async def update_book(
    book_id: str,
    book_update: BookUpdate,
    session: AsyncSession = Depends(get_session),
) -> dict:
    """Actualiza parcialmente un libro. Requiere rol ADMIN o PRO_USER."""
    book = await book_service.update_book(session, UUID(book_id), book_update)
    if not book:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Libro no encontrado")
    return {"message": "Libro actualizado exitosamente", "book": book}


@book_router.delete("/book/{book_id}", response_model=BookResponse, status_code=status.HTTP_200_OK,
                    dependencies=[_can_delete])
async def delete_book(
    book_id: str,
    session: AsyncSession = Depends(get_session),
) -> dict:
    """Elimina un libro. Requiere rol ADMIN."""
    book = await book_service.delete_book(session, UUID(book_id))
    if not book:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Libro no encontrado")
    return {"message": "Libro eliminado exitosamente", "book": book}


@book_router.get("/user/books", response_model=GetBooksResponse, status_code=status.HTTP_200_OK)
async def get_my_books(
    session: AsyncSession = Depends(get_session),
    token_details: dict = Depends(access_token_bearer)
) -> dict:
    """Obtiene todos los libros creados por el usuario autenticado."""
    user = token_details.get("user", {})
    user_uid = user.get("user_uid")
    if not user_uid:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token inválido")
        
    books = await book_service.get_user_books(user_uid, session)
    return {"total_books": len(books), "books": books}
