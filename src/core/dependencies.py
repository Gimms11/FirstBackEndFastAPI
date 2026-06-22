from fastapi import Depends, status
from fastapi.exceptions import HTTPException
from sqlmodel.ext.asyncio.session import AsyncSession

from typing import List

from src.core.security import AccessTokenBearer
from src.database.main import get_session
from src.modules.auth.models import User, UserRole
from src.modules.auth.service import UserService

_user_service = UserService()
_access_token_bearer = AccessTokenBearer()


async def get_current_user(
    token_details: dict = Depends(_access_token_bearer),
    session: AsyncSession = Depends(get_session),
) -> User:
    """
    Dependencia global que extrae el usuario autenticado desde el Access Token.
    Úsala en cualquier ruta que necesite saber quién está haciendo la petición.
    """
    user_email = token_details["user"]["email"]
    user = await _user_service.get_user_by_email(user_email, session)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuario no encontrado en el sistema"
        )

    return user


class RoleChecker:
    def __init__(self, allowed_roles: List[UserRole]) -> None:
        # Recibe la lista de roles permitidos para un recurso específico
        self.allowed_roles = allowed_roles

    def __call__(self, current_user: User = Depends(get_current_user)) -> bool:
        """
        Se ejecuta automáticamente cuando FastAPI procesa la dependencia en la ruta.
        """
        if current_user.role in self.allowed_roles:
            return True
            
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tienes permisos suficientes para realizar esta acción"
        )