<<<<<<< HEAD
import logging
import redis.asyncio as redis
from src.config import Config

logger = logging.getLogger(__name__)

=======
import redis.asyncio as redis
from src.config import Config

>>>>>>> 2106935d3af0aff6b65db4b3bb76c43d52855a89
JTI_EXPIRY = 3600  # Tiempo de vida en la lista (1 hora)

# Inicialización del cliente asíncrono de Redis
token_blocklist = redis.Redis(
    host=Config.REDIS_HOST, 
    port=Config.REDIS_PORT, 
    db=0, 
    decode_responses=True,
    protocol=2
)

<<<<<<< HEAD
# Fallback en memoria para desarrollo/pruebas si Redis no está disponible
_in_memory_blocklist = set()

async def add_jti_to_blocklist(jti: str) -> None:
    """Añade el JTI del token a Redis con un tiempo de expiración."""
    try:
        await token_blocklist.set(name=jti, value="", ex=JTI_EXPIRY)
    except Exception as e:
        logger.warning(f"Redis no está disponible. Usando fallback en memoria para revocar token. Error: {e}")
        _in_memory_blocklist.add(jti)

async def token_in_blocklist(jti: str) -> bool:
    """Verifica si el JTI existe en la lista de bloqueos de Redis."""
    try:
        exists = await token_blocklist.get(jti)
        return exists is not None
    except Exception as e:
        logger.warning(f"Redis no está disponible. Usando fallback en memoria para chequear token. Error: {e}")
        return jti in _in_memory_blocklist
=======
async def add_jti_to_blocklist(jti: str) -> None:
    """Añade el JTI del token a Redis con un tiempo de expiración."""
    await token_blocklist.set(name=jti, value="", ex=JTI_EXPIRY)

async def token_in_blocklist(jti: str) -> bool:
    """Verifica si el JTI existe en la lista de bloqueos de Redis."""
    exists = await token_blocklist.get(jti)
    return exists is not None
>>>>>>> 2106935d3af0aff6b65db4b3bb76c43d52855a89
