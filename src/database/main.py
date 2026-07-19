from sqlmodel import SQLModel
from sqlalchemy.ext.asyncio import create_async_engine
from sqlmodel.ext.asyncio.session import AsyncSession
from src.config import Config
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import NullPool

engine = create_async_engine(
    url=Config.DATABASE_URL,
    echo=True,
    poolclass=NullPool,
    connect_args={
        "statement_cache_size": 0,
        "prepared_statement_cache_size": 0,
    }
)


async def init_db():
    async with engine.begin() as conn:
        # Importamos todos los modelos para que SQLModel los registre
        from src.modules.auth.models import User  # noqa: F401
        from src.modules.authors.models import Author  # noqa: F401
        from src.modules.books.models import Book  # noqa: F401
        await conn.run_sync(SQLModel.metadata.create_all)
        print("Base de datos creada exitosamente")


async def get_session() -> AsyncSession:
    Session = sessionmaker(
        bind=engine,
        class_=AsyncSession,
        expire_on_commit=False
    )

    async with Session() as session:
        yield session