from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select

from src.modules.authors.models import Author
from src.modules.authors.schemas import AuthorCreateModel, AuthorUpdate


class AuthorService:
    async def get_all_authors(self, session: AsyncSession):
        statement = select(Author)
        result = await session.exec(statement)
        return result.all()

    async def get_author_by_id(self, session: AsyncSession, uid: str):
        statement = select(Author).where(Author.uid == uid)
        result = await session.exec(statement)
        return result.first()

    async def create_author(self, session: AsyncSession, author: AuthorCreateModel):
        author_data = author.model_dump()
        new_author = Author(**author_data)
        session.add(new_author)
        await session.commit()
        await session.refresh(new_author)
        return new_author

    async def update_author(self, session: AsyncSession, uid: str, author_update: AuthorUpdate):
        author_to_update = await self.get_author_by_id(session, uid)
        if not author_to_update:
            return None

        author_data = author_update.model_dump(exclude_unset=True)
        for key, value in author_data.items():
            setattr(author_to_update, key, value)

        session.add(author_to_update)
        await session.commit()
        await session.refresh(author_to_update)
        return author_to_update

    async def delete_author(self, session: AsyncSession, uid: str):
        author_to_delete = await self.get_author_by_id(session, uid)
        if not author_to_delete:
            return None
        info_author = author_to_delete.model_dump()
        await session.delete(author_to_delete)
        await session.commit()
        return info_author
