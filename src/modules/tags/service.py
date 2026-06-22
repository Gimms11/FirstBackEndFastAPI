from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select, desc
from uuid import UUID

from src.database.models import Tag, Book
from src.modules.tags.schemas import TagCreateModel


class TagService:
    async def get_all_tags(self, session: AsyncSession):
        statement = select(Tag).order_by(desc(Tag.created_at))
        result = await session.exec(statement)
        return result.all()

    async def get_tag_by_id(self, session: AsyncSession, uid: UUID):
        statement = select(Tag).where(Tag.uid == uid)
        result = await session.exec(statement)
        return result.first()

    async def get_tag_by_name(self, session: AsyncSession, name: str):
        statement = select(Tag).where(Tag.name == name)
        result = await session.exec(statement)
        return result.first()

    async def create_tag(self, session: AsyncSession, tag_data: TagCreateModel):
        existing_tag = await self.get_tag_by_name(session, tag_data.name)
        if existing_tag:
            return existing_tag  # Si ya existe, simplemente lo retornamos

        new_tag = Tag(name=tag_data.name)
        session.add(new_tag)
        await session.commit()
        await session.refresh(new_tag)
        return new_tag

    async def delete_tag(self, session: AsyncSession, uid: UUID):
        tag_to_delete = await self.get_tag_by_id(session, uid)
        if not tag_to_delete:
            return None
        info_tag = tag_to_delete.model_dump()
        await session.delete(tag_to_delete)
        await session.commit()
        return info_tag

    async def add_tag_to_book(self, session: AsyncSession, tag_uid: UUID, book_uid: UUID):
        tag = await self.get_tag_by_id(session, tag_uid)
        
        # Obtener el libro
        statement = select(Book).where(Book.uid == book_uid)
        result = await session.exec(statement)
        book = result.first()

        if not tag or not book:
            return None

        # Si el tag no está ya en el libro, lo agregamos
        if tag not in book.tags:
            book.tags.append(tag)
            session.add(book)
            await session.commit()
            await session.refresh(book)
        
        return tag

    async def remove_tag_from_book(self, session: AsyncSession, tag_uid: UUID, book_uid: UUID):
        tag = await self.get_tag_by_id(session, tag_uid)
        
        statement = select(Book).where(Book.uid == book_uid)
        result = await session.exec(statement)
        book = result.first()

        if not tag or not book:
            return None

        if tag in book.tags:
            book.tags.remove(tag)
            session.add(book)
            await session.commit()
            await session.refresh(book)
            
        return tag
