<<<<<<< HEAD
from fastapi import APIRouter, status, Depends
=======
from fastapi import APIRouter, HTTPException, status, Depends
>>>>>>> 2106935d3af0aff6b65db4b3bb76c43d52855a89
from sqlmodel.ext.asyncio.session import AsyncSession
from uuid import UUID

from src.modules.books.schemas import BookSchema, BookCreateModel, BookUpdate, GetBooksResponse, BookResponse
from src.modules.books.service import BookService
<<<<<<< HEAD
from src.core.dependencies import RoleChecker, get_current_user
from src.modules.auth.models import UserRole
from src.database.models import User
from src.core.security import AccessTokenBearer
from src.database.main import get_session
from src.errors import BookNotFound, BookAlreadyExists, InvalidToken, AuthorNotFound, InvalidIdBook

from src.celery_task import send_email_task
=======
from src.core.dependencies import RoleChecker
from src.modules.auth.models import UserRole
from src.core.security import AccessTokenBearer
from src.database.main import get_session
>>>>>>> 2106935d3af0aff6b65db4b3bb76c43d52855a89

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
<<<<<<< HEAD
    try:
        book = await book_service.get_book_by_id(session, UUID(book_id))
    except ValueError:
        raise InvalidIdBook()

    if not book:
        raise BookNotFound()
=======
    book = await book_service.get_book_by_id(session, UUID(book_id))
    if not book:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Libro no encontrado")
>>>>>>> 2106935d3af0aff6b65db4b3bb76c43d52855a89
    return {"message": "Libro encontrado", "book": book}


@book_router.post("/book", response_model=BookResponse, status_code=status.HTTP_201_CREATED,
                  dependencies=[_can_write])
async def create_book(
    book_data: BookCreateModel,
    session: AsyncSession = Depends(get_session),
<<<<<<< HEAD
    token_details: dict = Depends(access_token_bearer),
    current_user: User = Depends(get_current_user)
=======
    token_details: dict = Depends(access_token_bearer)
>>>>>>> 2106935d3af0aff6b65db4b3bb76c43d52855a89
) -> dict:
    """Crea un nuevo libro. Requiere rol ADMIN o PRO_USER."""
    books = await book_service.get_all_books(session)
    
    if any(b.title == book_data.title for b in books):
<<<<<<< HEAD
        raise BookAlreadyExists()
=======
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="El libro ya existe.")
>>>>>>> 2106935d3af0aff6b65db4b3bb76c43d52855a89
    
    user = token_details.get("user", {})
    user_uid = user.get("user_uid")
    if not user_uid:
<<<<<<< HEAD
        raise InvalidToken()
=======
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token inválido, falta user_uid")
>>>>>>> 2106935d3af0aff6b65db4b3bb76c43d52855a89
    
    new_book = await book_service.create_book(session, book_data, user_uid)
    
    if not new_book:
<<<<<<< HEAD
        raise AuthorNotFound()
        
    # 1. Definición de la plantilla adaptada a la marca
    html_template = f"""
    <html>
        <body style="font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background-color: #f4f6f9; padding: 20px; color: #2d3748;">
            <div style="max-width: 600px; margin: 0 auto; background-color: #ffffff; border-radius: 8px; padding: 30px; box-shadow: 0 4px 6px rgba(0,0,0,0.05); border-top: 4px solid #3182ce;">
                <h2 style="color: #2b6cb0; border-bottom: 2px solid #edf2f7; padding-bottom: 10px; margin-top: 0;">Creaste un libro maravilloso</h2>
                <p>Hola <strong>{current_user.username}</strong>,</p>
                <p>Has creado un Libro muy interesante.</p>
                
                <div style="background-color: #ebf8ff; border: 1px solid #bee3f8; border-radius: 6px; padding: 15px; margin: 20px 0;">
                    <p style="margin: 0; color: #2b6cb0;"><strong>Detalles del libro:</strong></p>
                    <p style="margin: 5px 0 0 0; font-size: 14px;"><strong>Nombre:</strong> {book_data.title}</p>
                    <p style="margin: 2px 0 0 0; font-size: 14px;"><strong>Autor registrado:</strong> {book_data.author_name}</p>
                </div>
                
                <p style="font-size: 12px; color: #a0aec0; margin-top: 30px; border-top: 1px solid #e2e8f0; padding-top: 15px; text-align: center;">
                    Librería API - Lectura sin límites.
                </p>
            </div>
        </body>
    </html>
    """
    
    # 2. Encolado de la tarea SMTP en segundo plano (tarda < 10ms en responder el endpoint)
    send_email_task.delay(
        email_to=current_user.email,
        subject="Creación Exitosa de Libro",
        html_content=html_template
    )
=======
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Autor no encontrado")
>>>>>>> 2106935d3af0aff6b65db4b3bb76c43d52855a89
    
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
<<<<<<< HEAD
        raise BookNotFound()
=======
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Libro no encontrado")
>>>>>>> 2106935d3af0aff6b65db4b3bb76c43d52855a89
    return {"message": "Libro actualizado exitosamente", "book": book}


@book_router.delete("/book/{book_id}", response_model=BookResponse, status_code=status.HTTP_200_OK,
<<<<<<< HEAD
                     dependencies=[_can_delete])
=======
                    dependencies=[_can_delete])
>>>>>>> 2106935d3af0aff6b65db4b3bb76c43d52855a89
async def delete_book(
    book_id: str,
    session: AsyncSession = Depends(get_session),
) -> dict:
    """Elimina un libro. Requiere rol ADMIN."""
    book = await book_service.delete_book(session, UUID(book_id))
    if not book:
<<<<<<< HEAD
        raise BookNotFound()
=======
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Libro no encontrado")
>>>>>>> 2106935d3af0aff6b65db4b3bb76c43d52855a89
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
<<<<<<< HEAD
        raise InvalidToken()
=======
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token inválido")
>>>>>>> 2106935d3af0aff6b65db4b3bb76c43d52855a89
        
    books = await book_service.get_user_books(user_uid, session)
    return {"total_books": len(books), "books": books}
