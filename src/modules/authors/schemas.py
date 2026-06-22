from pydantic import BaseModel
from typing import List, Optional
from uuid import UUID


class AuthorCreateModel(BaseModel):
    name: str
    country: str


class AuthorUpdate(BaseModel):
    name: Optional[str] = None
    country: Optional[str] = None


class AuthorSchema(BaseModel):
    uid: UUID
    name: str
    country: str


class GetAuthorsResponse(BaseModel):
    total_authors: int
    authors: List[AuthorSchema]


class AuthorResponse(BaseModel):
    message: str
    author: AuthorSchema
