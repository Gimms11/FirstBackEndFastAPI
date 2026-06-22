from pydantic import BaseModel, Field
from uuid import UUID
from typing import Optional
from datetime import datetime

class ReviewSchema(BaseModel):
    uid: UUID
    rating: int
    review_text: str
    user_uid: UUID
    book_uid: UUID
    created_at: datetime
    updated_at: datetime

class ReviewCreateModel(BaseModel):
    book_uid: UUID
    rating: int = Field(le=5, ge=1)
    review_text: str

class ReviewUpdateModel(BaseModel):
    rating: Optional[int] = Field(None, le=5, ge=1)
    review_text: Optional[str] = None

class ReviewResponse(BaseModel):
    message: str
    review: ReviewSchema
