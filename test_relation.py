import asyncio
import uuid
from sqlalchemy.ext.asyncio import create_async_engine
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select

from src.database.models import Book, Tag, User, Review, UserRole
from src.config import Config
from src.modules.tags.schemas import TagCreateModel
from src.modules.tags.service import TagService
from src.modules.books.service import BookService
from src.modules.books.schemas import BookCreateModel

async def main():
    engine = create_async_engine(Config.DATABASE_URL, echo=False)
    async with AsyncSession(engine, expire_on_commit=False) as session:
        # Create a mock user
        test_user = User(
            username=f"tester_{uuid.uuid4().hex[:6]}",
            first_name="Test",
            last_name="User",
            email=f"tester_{uuid.uuid4().hex[:6]}@test.com",
            password_hash="fake",
            role=UserRole.ADMIN
        )
        session.add(test_user)
        await session.commit()
        await session.refresh(test_user)
        print(f"[OK] Usuario creado: {test_user.username}")

        # Create author directly in db
        from src.database.models import Author
        test_author = Author(name=f"Author_{uuid.uuid4().hex[:6]}", country="PE")
        session.add(test_author)
        await session.commit()
        await session.refresh(test_author)
        
        # Create a book
        book_svc = BookService()
        book_data = BookCreateModel(
            title=f"Book of Testing {uuid.uuid4().hex[:6]}",
            author_name=test_author.name,
            publisher="TestPub",
            published_date="2023-10-10",
            page_count=100,
            language="es"
        )
        book = await book_svc.create_book(session, book_data, str(test_user.uid))
        if not book:
            print("[FAIL] No se pudo crear el libro")
            return
        print(f"[OK] Libro creado: {book.title}")

        # Create a tag and link it
        tag_svc = TagService()
        tag_data = TagCreateModel(name=f"TestingTag_{uuid.uuid4().hex[:6]}")
        tag = await tag_svc.create_tag(session, tag_data)
        print(f"[OK] Tag creado: {tag.name}")

        linked_tag = await tag_svc.add_tag_to_book(session, tag.uid, book.uid)
        print(f"[OK] Tag {linked_tag.name} vinculado al libro {book.title}")

        # Re-fetch the book using the service to see if relations load
        fetched_book = await book_svc.get_book_by_id(session, str(book.uid))
        
        print("\n--- RESULTADOS DE RELACIONES ---")
        print(f"Tags del libro: {[t.name for t in fetched_book.tags]}")
        
        if len(fetched_book.tags) > 0 and fetched_book.tags[0].name == tag.name:
            print(">> ÉXITO: Relación Muchos-a-Muchos funciona perfectamente.")
        else:
            print(">> FALLO: El libro no tiene el tag.")

if __name__ == "__main__":
    asyncio.run(main())
