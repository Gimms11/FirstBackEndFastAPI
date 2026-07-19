<<<<<<< HEAD
from fastapi import APIRouter, status, Depends
=======
from fastapi import APIRouter, HTTPException, status, Depends
>>>>>>> 2106935d3af0aff6b65db4b3bb76c43d52855a89
from sqlmodel.ext.asyncio.session import AsyncSession
from uuid import UUID

from src.modules.authors.schemas import AuthorSchema, AuthorCreateModel, AuthorUpdate, GetAuthorsResponse, AuthorResponse
from src.modules.authors.service import AuthorService
from src.core.dependencies import RoleChecker
from src.modules.auth.models import UserRole
from src.database.main import get_session
<<<<<<< HEAD
from src.errors import AuthorNotFound
=======
>>>>>>> 2106935d3af0aff6b65db4b3bb76c43d52855a89

author_router = APIRouter()
author_service = AuthorService()

# ── Guards de rol ─────────────────────────────────────────
# Crear / Editar / Eliminar: solo admins
_can_manage = Depends(RoleChecker([UserRole.ADMIN]))


@author_router.get("/authors", response_model=GetAuthorsResponse, status_code=status.HTTP_200_OK)
async def get_authors(session: AsyncSession = Depends(get_session)) -> dict:
    """Obtiene la lista de todos los autores. Público."""
    authors = await author_service.get_all_authors(session)
    return {"total_authors": len(authors), "authors": authors}


@author_router.get("/author/{author_id}", response_model=AuthorResponse, status_code=status.HTTP_200_OK)
async def get_author(author_id: str, session: AsyncSession = Depends(get_session)) -> dict:
    """Busca un autor específico por su ID. Público."""
    author = await author_service.get_author_by_id(session, UUID(author_id))
    if not author:
<<<<<<< HEAD
        raise AuthorNotFound()
=======
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Autor no encontrado")
>>>>>>> 2106935d3af0aff6b65db4b3bb76c43d52855a89
    return {"message": "Autor encontrado", "author": author}


@author_router.post("/author", response_model=AuthorResponse, status_code=status.HTTP_201_CREATED,
                    dependencies=[_can_manage])
async def create_author(
    author_data: AuthorCreateModel,
    session: AsyncSession = Depends(get_session),
) -> dict:
    """Crea un nuevo autor. Requiere rol ADMIN."""
    new_author = await author_service.create_author(session, author_data)
    return {"message": "Autor creado exitosamente", "author": new_author}


@author_router.patch("/author/{author_id}", response_model=AuthorResponse, status_code=status.HTTP_200_OK,
                     dependencies=[_can_manage])
async def update_author(
    author_id: str,
    author_update: AuthorUpdate,
    session: AsyncSession = Depends(get_session),
) -> dict:
    """Actualiza parcialmente un autor. Requiere rol ADMIN."""
    author = await author_service.update_author(session, UUID(author_id), author_update)
    if not author:
<<<<<<< HEAD
        raise AuthorNotFound()
=======
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Autor no encontrado")
>>>>>>> 2106935d3af0aff6b65db4b3bb76c43d52855a89
    return {"message": "Autor actualizado exitosamente", "author": author}


@author_router.delete("/author/{author_id}", response_model=AuthorResponse, status_code=status.HTTP_200_OK,
                      dependencies=[_can_manage])
async def delete_author(
    author_id: str,
    session: AsyncSession = Depends(get_session),
) -> dict:
    """Elimina un autor. Requiere rol ADMIN."""
    result = await author_service.delete_author(session, UUID(author_id))
    if not result:
<<<<<<< HEAD
        raise AuthorNotFound()
=======
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Autor no encontrado")
>>>>>>> 2106935d3af0aff6b65db4b3bb76c43d52855a89
    return {"message": "Autor eliminado exitosamente", "author": result}
