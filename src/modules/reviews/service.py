from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select, desc
from uuid import UUID

from src.database.models import Review, Book
from src.modules.reviews.schemas import ReviewCreateModel, ReviewUpdateModel


class ReviewService:
    async def get_reviews_for_book(self, session: AsyncSession, book_uid: UUID):
        statement = select(Review).where(Review.book_uid == book_uid).order_by(desc(Review.created_at))
        result = await session.exec(statement)
        return result.all()

    async def get_review_by_id(self, session: AsyncSession, uid: UUID):
        statement = select(Review).where(Review.uid == uid)
        result = await session.exec(statement)
        return result.first()

    async def create_review(self, session: AsyncSession, review_data: ReviewCreateModel, user_uid: str):
        # Verificar que el libro exista
        statement = select(Book).where(Book.uid == review_data.book_uid)
        result = await session.exec(statement)
        book = result.first()

        if not book:
            return None

        new_review = Review(
            rating=review_data.rating,
            review_text=review_data.review_text,
            user_uid=UUID(user_uid),
            book_uid=review_data.book_uid
        )
<<<<<<< HEAD
        
=======
>>>>>>> 2106935d3af0aff6b65db4b3bb76c43d52855a89
        session.add(new_review)
        await session.commit()
        await session.refresh(new_review)
        return new_review

    async def update_review(self, session: AsyncSession, uid: UUID, review_update: ReviewUpdateModel):
        review_to_update = await self.get_review_by_id(session, uid)
        if not review_to_update:
            return None

        update_data = review_update.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(review_to_update, key, value)

        session.add(review_to_update)
        await session.commit()
        await session.refresh(review_to_update)
        return review_to_update

    async def delete_review(self, session: AsyncSession, uid: UUID):
        review_to_delete = await self.get_review_by_id(session, uid)
        if not review_to_delete:
            return None
        info_review = review_to_delete.model_dump()
        await session.delete(review_to_delete)
        await session.commit()
        return info_review
