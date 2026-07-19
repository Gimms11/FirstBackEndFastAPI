<<<<<<< HEAD
from fastapi import APIRouter, status, Depends
=======
from fastapi import APIRouter, HTTPException, status, Depends
>>>>>>> 2106935d3af0aff6b65db4b3bb76c43d52855a89
from sqlmodel.ext.asyncio.session import AsyncSession
from uuid import UUID

from src.modules.tags.schemas import TagCreateModel, TagResponse
from src.modules.tags.service import TagService
from src.core.dependencies import RoleChecker
from src.database.models import UserRole
from src.database.main import get_session
<<<<<<< HEAD
from src.errors import BookNotFound, TagNotFound, InvalidId
=======
>>>>>>> 2106935d3af0aff6b65db4b3bb76c43d52855a89

tag_router = APIRouter()
tag_service = TagService()

_can_write = Depends(RoleChecker([UserRole.ADMIN, UserRole.PRO_USER]))
_can_delete = Depends(RoleChecker([UserRole.ADMIN]))

@tag_router.get("/", status_code=status.HTTP_200_OK)
async def get_all_tags(session: AsyncSession = Depends(get_session)) -> dict:
    """Obtiene todos los tags creados."""
    tags = await tag_service.get_all_tags(session)
    return {"total_tags": len(tags), "tags": tags}

@tag_router.post("/", response_model=TagResponse, status_code=status.HTTP_201_CREATED, dependencies=[_can_write])
async def create_tag(
    tag_data: TagCreateModel,
    session: AsyncSession = Depends(get_session)
) -> dict:
    """Crea un nuevo tag (Requiere ADMIN o PRO_USER)."""
    new_tag = await tag_service.create_tag(session, tag_data)
    return {"message": "Tag creado/obtenido exitosamente", "tag": new_tag}

@tag_router.post("/book/{book_id}", response_model=TagResponse, status_code=status.HTTP_201_CREATED, dependencies=[_can_write])
async def add_tag_to_book(
    book_id: str,
    tag_data: TagCreateModel,
    session: AsyncSession = Depends(get_session)
) -> dict:
    """Crea/Obtiene un tag y se lo asocia a un libro (Requiere ADMIN o PRO_USER)."""
    try:
        book_uuid = UUID(book_id)
    except ValueError:
<<<<<<< HEAD
        raise InvalidId(message="ID de libro inválido")
=======
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="ID de libro inválido")
>>>>>>> 2106935d3af0aff6b65db4b3bb76c43d52855a89

    # Primero aseguramos que el tag exista o lo creamos
    tag = await tag_service.create_tag(session, tag_data)
    
    # Vinculamos al libro
    result = await tag_service.add_tag_to_book(session, tag.uid, book_uuid)
    if not result:
<<<<<<< HEAD
        raise BookNotFound(message="Libro o tag no encontrado")
=======
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Libro o tag no encontrado")
>>>>>>> 2106935d3af0aff6b65db4b3bb76c43d52855a89

    return {"message": "Tag asociado exitosamente al libro", "tag": tag}

@tag_router.delete("/{tag_id}/book/{book_id}", status_code=status.HTTP_200_OK, dependencies=[_can_delete])
async def remove_tag_from_book(
    tag_id: str,
    book_id: str,
    session: AsyncSession = Depends(get_session)
) -> dict:
    """Quita la asociación de un tag a un libro (Requiere ADMIN)."""
    try:
        tag_uuid = UUID(tag_id)
        book_uuid = UUID(book_id)
    except ValueError:
<<<<<<< HEAD
        raise InvalidId(message="IDs inválidos")

    result = await tag_service.remove_tag_from_book(session, tag_uuid, book_uuid)
    if not result:
        raise BookNotFound(message="Libro o tag no encontrado")
=======
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="IDs inválidos")

    result = await tag_service.remove_tag_from_book(session, tag_uuid, book_uuid)
    if not result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Libro o tag no encontrado")
>>>>>>> 2106935d3af0aff6b65db4b3bb76c43d52855a89

    return {"message": "Tag removido del libro exitosamente"}

@tag_router.delete("/{tag_id}", status_code=status.HTTP_200_OK, dependencies=[_can_delete])
async def delete_tag(
    tag_id: str,
    session: AsyncSession = Depends(get_session)
) -> dict:
    """Elimina globalmente un tag de la base de datos (Requiere ADMIN)."""
    try:
        tag_uuid = UUID(tag_id)
    except ValueError:
<<<<<<< HEAD
        raise InvalidId(message="ID de tag inválido")

    tag = await tag_service.delete_tag(session, tag_uuid)
    if not tag:
        raise TagNotFound()
=======
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="ID de tag inválido")

    tag = await tag_service.delete_tag(session, tag_uuid)
    if not tag:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Tag no encontrado")
>>>>>>> 2106935d3af0aff6b65db4b3bb76c43d52855a89

    return {"message": "Tag eliminado exitosamente"}
