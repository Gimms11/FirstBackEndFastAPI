import logging
from typing import Any
from fastapi import Request, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException

logger = logging.getLogger("bookly.errors")

# ==========================================
# 1. JERARQUÍA DE EXCEPCIONES (POLIMORFISMO)
# ==========================================

class BooklyException(Exception):
    """Clase base para todos los errores del ecosistema Bookly."""
    status_code: int = status.HTTP_500_INTERNAL_SERVER_ERROR
    message: str = "Oops! Algo salió mal en el servidor"
    error_code: str = "server_error"
    resolution: str | None = None

    def __init__(self, message: str | None = None, resolution: str | None = None) -> None:
        # Permitimos sobrescribir los mensajes por defecto al lanzar la excepción si es necesario
        if message:
            self.message = message
        if resolution:
            self.resolution = resolution
        super().__init__(self.message)


# --- Errores de Autenticación y Tokens ---

class InvalidToken(BooklyException):
    status_code = status.HTTP_401_UNAUTHORIZED
    message = "El token proporcionado es inválido o ha expirado"
    error_code = "invalid_token"
    resolution = "Por favor, solicita un nuevo token de acceso"

class RevokedToken(BooklyException):
    status_code = status.HTTP_401_UNAUTHORIZED
    message = "El token ha sido revocado"
    error_code = "token_revoked"
    resolution = "Inicia sesión nuevamente"

class AccessTokenRequired(BooklyException):
    status_code = status.HTTP_401_UNAUTHORIZED
    message = "Se requiere un token de acceso, pero se proporcionó un refresh token"
    error_code = "access_token_required"
    resolution = "Envía el token de acceso en el header Authorization"

class RefreshTokenRequired(BooklyException):
    status_code = status.HTTP_403_FORBIDDEN
    message = "Se requiere un token de actualización (refresh token)"
    error_code = "refresh_token_required"
    resolution = "Envía el token de refresco válido para renovar tu sesión"


# --- Errores de Usuarios y Credenciales ---

class UserAlreadyExists(BooklyException):
    status_code = status.HTTP_403_FORBIDDEN
    message = "Ya existe un usuario registrado con este correo electrónico"
    error_code = "user_exists"

class InvalidCredentials(BooklyException):
    status_code = status.HTTP_400_BAD_REQUEST
    message = "Correo electrónico o contraseña incorrectos"
    error_code = "invalid_email_or_password"

class InsufficientPermission(BooklyException):
    status_code = status.HTTP_403_FORBIDDEN # 403 es el estándar correcto para falta de privilegios
    message = "No tienes los permisos necesarios para realizar esta acción"
    error_code = "insufficient_permissions"

class UserNotFound(BooklyException):
    status_code = status.HTTP_404_NOT_FOUND
    message = "El usuario solicitado no existe"
    error_code = "user_not_found"


# --- Errores de Dominio (Libros, Autores, Reseñas y Tags) ---

class InvalidId(BooklyException):
    status_code = status.HTTP_400_BAD_REQUEST
    message = "El ID proporcionado no es válido"
    error_code = "invalid_id"

class BookNotFound(BooklyException):
    status_code = status.HTTP_404_NOT_FOUND
    message = "El libro solicitado no pudo ser encontrado"
    error_code = "book_not_found"

class InvalidIdBook(BooklyException):
    status_code = status.HTTP_400_BAD_REQUEST
    message = "El formato del ID del libro no es válido"
    error_code = "invalid_id_book"

class BookAlreadyExists(BooklyException):
    status_code = status.HTTP_409_CONFLICT
    message = "El libro especificado ya existe"
    error_code = "book_exists"

class AuthorNotFound(BooklyException):
    status_code = status.HTTP_404_NOT_FOUND
    message = "El autor solicitado no existe"
    error_code = "author_not_found"

class ReviewNotFound(BooklyException):
    status_code = status.HTTP_404_NOT_FOUND
    message = "La reseña solicitada no pudo ser encontrada"
    error_code = "review_not_found"

class TagNotFound(BooklyException):
    status_code = status.HTTP_404_NOT_FOUND
    message = "El tag solicitado no existe"
    error_code = "tag_not_found"

class TagAlreadyExists(BooklyException):
    status_code = status.HTTP_409_CONFLICT
    message = "El tag especificado ya existe"
    error_code = "tag_exists"

# ==========================================
# 2. MANEJADORES CENTRALIZADOS
# ==========================================

async def bookly_exception_handler(request: Request, exc: BooklyException) -> JSONResponse:
    """
    Manejador dinámico global. Procesa de forma polimórfica 
    cualquier subclase derivada de BooklyException.
    """
    content = {
        "message": exc.message,
        "error_code": exc.error_code,
    }
    
    # Agrega la resolución solo si el error contiene una ayuda explícita
    if exc.resolution:
        content["resolution"] = exc.resolution
        
    return JSONResponse(
        status_code=exc.status_code,
        content=content
    )

def register_error_handlers(app: Any) -> None:
    """Registra los interceptores de excepciones en la instancia de FastAPI."""
    
    # Captura todas las excepciones personalizadas derivadas de BooklyException
    app.add_exception_handler(BooklyException, bookly_exception_handler)

    # Captura y unifica los errores de validación de esquemas (Pydantic / FastAPI boundaries)
    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(request: Request, exc: RequestValidationError):
        logger.warning(f"Error de validación en {request.url.path}: {exc.errors()}")
        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            content={
                "message": "Los datos proporcionados no son válidos.",
                "error_code": "validation_error",
                "detail": exc.errors()
            }
        )

    # Captura y unifica las excepciones HTTP generales de FastAPI/Starlette
    @app.exception_handler(StarletteHTTPException)
    async def http_exception_handler(request: Request, exc: StarletteHTTPException):
        logger.warning(f"Excepción HTTP en {request.url.path}: {exc.detail}")
        return JSONResponse(
            status_code=exc.status_code,
            content={
                "message": exc.detail,
                "error_code": "http_error"
            }
        )

    # Manejador de respaldo para errores imprevistos (500) del sistema para evitar fuga de información sensible
    @app.exception_handler(Exception)
    async def internal_server_error(request: Request, exc: Exception):
        # Registramos el traceback completo en los archivos de log internos para depuración
        logger.exception("Error crítico no controlado en el servidor:")
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "message": "Ha ocurrido un error inesperado en nuestro servidor",
                "error_code": "server_error"
            }
        )