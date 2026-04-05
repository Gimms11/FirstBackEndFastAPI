from typing import List
from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel

app = FastAPI()

# ==========================================
# BASE DE DATOS EN MEMORIA (Simulada)
# ==========================================
books = [
    {
        "id": 1,
        "title": "Think Python",
        "author": "Allen B. Downey",
        "publisher": "O'Reilly Media",
        "published_date": "2021-01-01",
        "page_count": 1234,
        "language": "English",
    },
    {
        "id": 2,
        "title": "Django By Example",
        "author": "Antonio Mele",
        "publisher": "Packt Publishing Ltd",
        "published_date": "2022-01-19",
        "page_count": 1023,
        "language": "English",
    },
    {
        "id": 3,
        "title": "The web socket handbook",
        "author": "Alex Diaconu",
        "publisher": "Xinyu Wang",
        "published_date": "2021-01-01",
        "page_count": 3677,
        "language": "English",
    },
    {
        "id": 4,
        "title": "Head first Javascript",
        "author": "Hellen Smith",
        "publisher": "Oreilly Media",
        "published_date": "2021-01-01",
        "page_count": 540,
        "language": "English",
    },
    {
        "id": 5,
        "title": "Algorithms and Data Structures In Python",
        "author": "Kent Lee",
        "publisher": "Springer, Inc",
        "published_date": "2021-01-01",
        "page_count": 9282,
        "language": "English",
    },
    {
        "id": 6,
        "title": "Head First HTML5 Programming",
        "author": "Eric T Freeman",
        "publisher": "O'Reilly Media",
        "published_date": "2011-21-01",
        "page_count": 3006,
        "language": "English",
    },
]

# ==========================================
# MODELOS DE PYDANTIC (Esquemas de validación)
# ==========================================
class Book(BaseModel):
    id: int
    title: str
    author: str
    publisher: str
    published_date: str
    page_count: int
    language: str

class BookUpdate(BaseModel):
    title: str | None = None
    author: str | None = None
    publisher: str | None = None
    page_count: int | None = None
    language: str | None = None

class GetBooksResponse(BaseModel):
    total_books: int
    books: List[Book]

class BookResponse(BaseModel):
    message: str
    book: Book

# ==========================================
# RUTAS / ENDPOINTS (Operaciones CRUD)
# ==========================================

@app.get("/books", response_model=GetBooksResponse, status_code=status.HTTP_200_OK)
async def get_books() -> dict:
    """Obtiene la lista de todos los libros disponibles."""
    total_books = len(books)
    return {"total_books": total_books, "books": books}

@app.get("/book/{book_id}", response_model=BookResponse, status_code=status.HTTP_200_OK)
async def get_book(book_id: int) -> dict:
    """Busca un libro específico por su ID."""
    for book in books:
        if book["id"] == book_id:
            return {"message": "Libro encontrado", "book": book}
            
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, 
        detail="Libro no encontrado"
    )

@app.post("/book", response_model=BookResponse, status_code=status.HTTP_201_CREATED)
async def create_book(book_data: Book) -> dict:
    """Crea un nuevo libro, verificando que el ID no exista previamente."""
    for book in books:
        if book["id"] == book_data.id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, 
                detail="El libro ya existe"
            )
            
    new_book = book_data.model_dump()
    books.append(new_book)
    return {"message": "Libro creado exitosamente", "book": new_book}

@app.patch("/book/{book_id}", response_model=BookResponse, status_code=status.HTTP_200_OK)
async def update_book(book_id: int, book_update: BookUpdate) -> dict:
    """Actualiza parcialmente los datos de un libro existente."""
    for book in books:
        if book["id"] == book_id:
            # Se usa exclude_none=True para evitar sobreescribir datos con nulos
            book.update(book_update.model_dump(exclude_none=True))
            return {"message": "Libro actualizado exitosamente", "book": book}
            
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, 
        detail="Libro no encontrado"
    )

@app.delete("/book/{book_id}", response_model=BookResponse, status_code=status.HTTP_200_OK)
async def delete_book(book_id: int) -> dict:
    """Elimina un libro del sistema usando su ID."""
    for book in books:
        if book["id"] == book_id:
            books.remove(book)
            return {"message": "Libro borrado exitosamente", "book": book}
            
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, 
        detail="Libro no encontrado"
    )