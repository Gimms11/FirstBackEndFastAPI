from pydantic import BaseModel, field_validator
from typing import List, Optional
from uuid import UUID
from datetime import datetime, date

from src.modules.tags.schemas import TagSchema
from src.modules.reviews.schemas import ReviewSchema


class BookSchema(BaseModel):
    uid: UUID
    title: str
    author_id: UUID
    publisher: str
    published_date: str
    page_count: int
    language: str
    created_at: datetime
    updated_at: datetime
    tags: List[TagSchema] = []
    reviews: List[ReviewSchema] = []

    @field_validator("published_date", mode="before")
    @classmethod
    def transform_date_to_string(cls, value):
        if isinstance(value, (date, datetime)):
            return value.isoformat()
        return value


class BookCreateModel(BaseModel):
    title: str
    author_name: str
    publisher: str
    published_date: date
    page_count: int
    language: str


class BookUpdate(BaseModel):
    title: Optional[str] = None
    author_name: Optional[str] = None
    publisher: Optional[str] = None
    page_count: Optional[int] = None
    language: Optional[str] = None


class GetBooksResponse(BaseModel):
    total_books: int
    books: List[BookSchema]


class BookResponse(BaseModel):
    message: str
    book: BookSchema
