from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select, desc

from src.modules.books.models import Book
from src.modules.books.schemas import BookCreateModel, BookUpdate


class BookService:
    async def get_all_books(self, session: AsyncSession):
        statement = select(Book).order_by(desc(Book.created_at))
        result = await session.exec(statement)
        return result.all()

    async def get_book_by_id(self, session: AsyncSession, uid: str):
        statement = select(Book).where(Book.uid == uid)
        result = await session.exec(statement)
        return result.first()

    async def create_book(self, session: AsyncSession, book: BookCreateModel, user_uid: str):
        # Importamos Author aquí para evitar dependencias circulares en models.py
        from src.modules.authors.models import Author

        # 1. Buscamos al autor por su nombre
        statement = select(Author).where(Author.name == book.author_name)
        result = await session.exec(statement)
        author = result.first()

        # Si el autor no existe, devolvemos None para que la ruta lance el error
        if not author:
            return None
        
        # 2. Si el autor existe, armamos el objeto Book manualmente usando su UUID
        new_book = Book(
            title=book.title,
            author_id=author.uid,
            publisher=book.publisher,
            published_date=book.published_date,
            user_uid=user_uid,
            page_count=book.page_count,
            language=book.language
        )

        session.add(new_book)
        await session.commit()
        await session.refresh(new_book)
        return new_book

    async def update_book(self, session: AsyncSession, uid: str, book: BookUpdate):
        from src.modules.authors.models import Author

        # 1. Buscamos el libro que se quiere actualizar
        book_to_update = await self.get_book_by_id(session, uid)
        if not book_to_update:
            return None

        # 2. Obtenemos los campos enviados en la solicitud (excluyendo los no enviados)
        update_data = book.model_dump(exclude_unset=True)

        # 3. Si se incluyó 'author_name', buscamos al autor correspondiente
        if "author_name" in update_data:
            author_name = update_data.pop("author_name")
            if author_name is not None:
                statement = select(Author).where(Author.name == author_name)
                result = await session.exec(statement)
                author = result.first()
                if not author:
                    from src.errors import AuthorNotFound
                    raise AuthorNotFound()
                book_to_update.author_id = author.uid
            else:
                book_to_update.author_id = None

        # 4. Actualizamos el resto de los campos
        for key, value in update_data.items():
            setattr(book_to_update, key, value)

        session.add(book_to_update)
        await session.commit()
        await session.refresh(book_to_update)
        return book_to_update

    async def delete_book(self, session: AsyncSession, uid: str):
        book_to_delete = await self.get_book_by_id(session, uid)
        if not book_to_delete:
            return None
        info_book = book_to_delete.model_dump()
        await session.delete(book_to_delete)
        await session.commit()
        return info_book

    async def get_user_books(self, user_uid: str, session: AsyncSession):
        statement = select(Book).where(Book.user_uid == user_uid).order_by(desc(Book.created_at))
        result = await session.exec(statement)
        return result.all()
    
