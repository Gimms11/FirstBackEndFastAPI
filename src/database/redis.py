import redis.asyncio as redis
from src.config import Config

JTI_EXPIRY = 3600  # Tiempo de vida en la lista (1 hora)

# Inicialización del cliente asíncrono de Redis
token_blocklist = redis.Redis(
    host=Config.REDIS_HOST, 
    port=Config.REDIS_PORT, 
    db=0, 
    decode_responses=True,
    protocol=2
)

async def add_jti_to_blocklist(jti: str) -> None:
    """Añade el JTI del token a Redis con un tiempo de expiración."""
    await token_blocklist.set(name=jti, value="", ex=JTI_EXPIRY)

async def token_in_blocklist(jti: str) -> bool:
    """Verifica si el JTI existe en la lista de bloqueos de Redis."""
    exists = await token_blocklist.get(jti)
    return exists is not None