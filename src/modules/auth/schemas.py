from pydantic import BaseModel, Field
from uuid import UUID
from datetime import datetime
from typing import List
from src.modules.books.schemas import BookSchema

class UserSchema(BaseModel):
    uid: UUID
    username: str
    first_name: str
    last_name: str
    email: str
    created_at: datetime


class UserResponse(BaseModel):
    message: str
    user: UserSchema


class UserCreateModel(BaseModel):
    username: str = Field(max_length=15, min_length=3)
    first_name: str = Field(max_length=20)
    last_name: str = Field(max_length=20)
    email: str = Field(max_length=80)
    password: str = Field(min_length=8)


class UserLoginModel(BaseModel):
    email: str = Field(max_length=40)
    password: str = Field(min_length=6)


class LoginUser(BaseModel):
    email: str
    password: str


class UserTokenResponse(BaseModel):
    access_token: str
    token_type: str
    user: dict  # Opcional: incluir info básica del usuario

# Heredamos para añadir la lista de libros
class UserBooksModel(UserSchema):
    books: List[BookSchema] = []
