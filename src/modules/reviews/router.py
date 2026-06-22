from fastapi import APIRouter, HTTPException, status, Depends
from sqlmodel.ext.asyncio.session import AsyncSession
from uuid import UUID

from src.modules.reviews.schemas import ReviewCreateModel, ReviewUpdateModel, ReviewResponse
from src.modules.reviews.service import ReviewService
from src.core.dependencies import get_current_user, RoleChecker
from src.database.models import User, UserRole
from src.database.main import get_session

review_router = APIRouter()
review_service = ReviewService()

_can_delete_any = RoleChecker([UserRole.ADMIN])

@review_router.get("/book/{book_id}", status_code=status.HTTP_200_OK)
async def get_book_reviews(book_id: str, session: AsyncSession = Depends(get_session)) -> dict:
    """Obtiene las reseñas de un libro."""
    try:
        book_uuid = UUID(book_id)
    except ValueError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="ID de libro inválido")
        
    reviews = await review_service.get_reviews_for_book(session, book_uuid)
    return {"total_reviews": len(reviews), "reviews": reviews}

@review_router.post("/", response_model=ReviewResponse, status_code=status.HTTP_201_CREATED)
async def create_review(
    review_data: ReviewCreateModel,
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user)
) -> dict:
    """Crea una reseña (Requiere autenticación)."""
    new_review = await review_service.create_review(session, review_data, str(current_user.uid))
    
    if not new_review:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Libro no encontrado")
        
    return {"message": "Reseña creada exitosamente", "review": new_review}

@review_router.patch("/{review_id}", response_model=ReviewResponse, status_code=status.HTTP_200_OK)
async def update_review(
    review_id: str,
    review_update: ReviewUpdateModel,
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user)
) -> dict:
    """Actualiza una reseña (Solo el autor)."""
    try:
        review_uuid = UUID(review_id)
    except ValueError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="ID de reseña inválido")

    review = await review_service.get_review_by_id(session, review_uuid)
    if not review:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Reseña no encontrada")
        
    if str(review.user_uid) != str(current_user.uid):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="No puedes modificar la reseña de otro usuario")
        
    updated_review = await review_service.update_review(session, review_uuid, review_update)
    return {"message": "Reseña actualizada", "review": updated_review}

@review_router.delete("/{review_id}", status_code=status.HTTP_200_OK)
async def delete_review(
    review_id: str,
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user)
) -> dict:
    """Elimina una reseña (Autor o ADMIN)."""
    try:
        review_uuid = UUID(review_id)
    except ValueError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="ID de reseña inválido")

    review = await review_service.get_review_by_id(session, review_uuid)
    if not review:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Reseña no encontrada")
        
    if str(review.user_uid) != str(current_user.uid) and current_user.role != UserRole.ADMIN:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="No tienes permisos para eliminar esta reseña")
        
    await review_service.delete_review(session, review_uuid)
    return {"message": "Reseña eliminada"}
