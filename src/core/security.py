from fastapi import Request, status
from fastapi.security import HTTPBearer
from fastapi.exceptions import HTTPException

from src.modules.auth.utils import decode_token
from src.database.redis import token_in_blocklist


class TokenBearer(HTTPBearer):
    """
    Clase base para la verificación de tokens JWT.
    Valida que el token exista, no esté expirado y no esté en la blocklist de Redis.
    Las clases hijas deben implementar `verify_token_data` para definir el tipo de token esperado.
    """
    def __init__(self, auto_error=True):
        super().__init__(auto_error=auto_error)

    async def __call__(self, request: Request) -> dict:
        creds = await super().__call__(request)
        token = creds.credentials

        token_data = decode_token(token)

        if not token_data:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail={"error": "Token inválido o expirado", "resolution": "Obtén un nuevo token"}
            )

        # Verificación en la lista de bloqueos de Redis
        if await token_in_blocklist(token_data["jti"]):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail={
                    "error": "Este token ha sido revocado o es inválido",
                    "resolution": "Por favor, inicia sesión nuevamente"
                }
            )

        self.verify_token_data(token_data)
        return token_data

    def verify_token_data(self, token_data: dict) -> None:
        raise NotImplementedError("Por favor, implementa este método en las clases hijas")


class AccessTokenBearer(TokenBearer):
    """Verifica que el token sea de tipo acceso (no refresh)."""
    def verify_token_data(self, token_data: dict) -> None:
        if token_data and token_data.get("refresh"):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Por favor, proporciona un token de acceso (Access Token)",
            )


class RefreshTokenBearer(TokenBearer):
    """Verifica que el token sea de tipo refresh (no acceso)."""
    def verify_token_data(self, token_data: dict) -> None:
        if token_data and not token_data.get("refresh"):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Por favor, proporciona un token de refresco (Refresh Token)",
            )
