from fastapi import Request, status
from fastapi.security import HTTPBearer

from src.modules.auth.utils import decode_token
from src.database.redis import token_in_blocklist
from src.errors import InvalidToken, RevokedToken, AccessTokenRequired, RefreshTokenRequired


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
            raise InvalidToken()

        # Verificación en la lista de bloqueos de Redis
        if await token_in_blocklist(token_data["jti"]):
            raise RevokedToken()

        self.verify_token_data(token_data)
        return token_data

    def verify_token_data(self, token_data: dict) -> None:
        raise NotImplementedError("Por favor, implementa este método en las clases hijas")


class AccessTokenBearer(TokenBearer):
    """Verifica que el token sea de tipo acceso (no refresh)."""
    def verify_token_data(self, token_data: dict) -> None:
        if token_data and token_data.get("refresh"):
            raise AccessTokenRequired()


class RefreshTokenBearer(TokenBearer):
    """Verifica que el token sea de tipo refresh (no acceso)."""
    def verify_token_data(self, token_data: dict) -> None:
        if token_data and not token_data.get("refresh"):
            raise RefreshTokenRequired()
