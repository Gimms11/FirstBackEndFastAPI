from sqlalchemy import text
from sqlmodel import SQLModel, Field, Column, Relationship
from typing import Optional, List
import sqlalchemy.dialects.postgresql as pg
from datetime import datetime, date, timezone
from uuid import UUID, uuid4
from enum import Enum

# --- Auth Models ---

class UserRole(str, Enum):
    ADMIN = "admin"
    USER = "user"
    PRO_USER = "pro_user"

class BookTag(SQLModel, table=True):
    __tablename__="book_tags"
    book_uid: UUID = Field(
        default = None,
        foreign_key = "books.uid",
        primary_key = True
    )
    tag_uid: UUID = Field(
        default=None,
        foreign_key="tags.uid",
        primary_key=True
    )

class User(SQLModel, table=True):
    __tablename__ = "users"
    uid: UUID = Field(
        sa_column=Column(
            pg.UUID,
            primary_key=True,
            unique=True,
            nullable=False,
            default=uuid4,
            info={"descripción": "Identificador unico para el usuario."}
        )
    )
    username: str = Field(unique=True, nullable=False)
    first_name: str = Field(nullable=False)
    last_name: str = Field(nullable=False)

    role: UserRole = Field(
        sa_column=Column(
            pg.VARCHAR,
            nullable=False,
            server_default=UserRole.USER.value
        )
    )

    is_verified: bool = Field(default=False)
    email: str = Field(unique=True, nullable=False)
    password_hash: str = Field(exclude=True)
    created_at: datetime = Field(
        sa_column=Column(
            pg.TIMESTAMP,
            server_default=text("now()")
        )
    )

    books: List["Book"] = Relationship(
        back_populates="user",
        sa_relationship_kwargs={
            "lazy": "selectin"
        }
    )

    reviews: List["Review"] = Relationship(
        back_populates="user",
        sa_relationship_kwargs={
            "lazy": "selectin"
        }
    )

    def __repr__(self) -> str:
        return f"<User {self.username}>"

# --- Author Models ---

class Author(SQLModel, table=True):
    __tablename__ = "authors"
    uid: UUID = Field(
        sa_column=Column(
            pg.UUID,
            nullable=False,
            primary_key=True,
            default=uuid4
        )
    )
    name: str
    country: str
    books: List["Book"] = Relationship(back_populates="author")  # noqa: F821

# --- Book Models ---

class Book(SQLModel, table=True):
    __tablename__ = "books"
    uid: UUID = Field(
        sa_column=Column(
            pg.UUID,
            nullable=False,
            primary_key=True,
            default=uuid4
        )
    )
    title: str
    author_id: Optional[UUID] = Field(default=None, foreign_key="authors.uid", ondelete="SET NULL")
    publisher: str
    published_date: date
    page_count: int
    language: str
    user_uid: Optional[UUID] = Field(default=None, foreign_key="users.uid")
    created_at: datetime = Field(sa_column=Column(pg.TIMESTAMP, server_default=text("now()")))
    updated_at: datetime = Field(sa_column=Column(pg.TIMESTAMP, server_default=text("now()"), onupdate=text("now()")))

    # Relación con el módulo authors
    author: Optional["Author"] = Relationship(back_populates="books")  # noqa: F821
    user: Optional[User] = Relationship(back_populates="books")
    reviews: List["Review"] = Relationship(back_populates="book", sa_relationship_kwargs={"lazy":"selectin"})
    tags: List["Tag"] = Relationship(link_model=BookTag, back_populates="books", sa_relationship_kwargs={"lazy":"selectin"})


    def __repr__(self) -> str:
        return f"Book(uid={self.uid}, title={self.title}, author={self.author})"

class Review(SQLModel, table=True):
    __tablename__ = "reviews"
    uid: UUID = Field(sa_column=Column(pg.UUID, nullable=False, primary_key=True, default=uuid4))
<<<<<<< HEAD
    rating: int = Field(le=5)
=======
    rating: int = Field(le=5) # 'le' significa less than or equal (<= 5)
>>>>>>> 2106935d3af0aff6b65db4b3bb76c43d52855a89
    review_text: str = Field(sa_column=Column(pg.VARCHAR, nullable=False))
    user_uid: Optional[UUID] = Field(default=None, foreign_key="users.uid")
    book_uid: Optional[UUID] = Field(default=None, foreign_key="books.uid")
    created_at: datetime = Field(sa_column=Column(pg.TIMESTAMP(timezone=True), default=lambda: datetime.now(timezone.utc)))
    updated_at: datetime = Field(sa_column=Column(pg.TIMESTAMP(timezone=True), default=lambda: datetime.now(timezone.utc)))

    # Relaciones de navegación
    user: Optional[User] = Relationship(back_populates="reviews")
    book: Optional[Book] = Relationship(back_populates="reviews")

class Tag(SQLModel, table=True):
    __tablename__ = "tags"
    uid: UUID = Field(sa_column=Column(pg.UUID, nullable=False, primary_key=True, default=uuid4))
    name: str = Field(sa_column=Column(pg.VARCHAR, nullable=False, unique=True))
    created_at: datetime = Field(sa_column=Column(pg.TIMESTAMP(timezone=True), default=lambda: datetime.now(timezone.utc)))
    
    # Relaciones de navegación
    books: List["Book"] = Relationship(link_model=BookTag, back_populates="tags", sa_relationship_kwargs={"lazy": "selectin"})