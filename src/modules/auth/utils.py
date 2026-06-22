from pwdlib import PasswordHash
from pwdlib.hashers.bcrypt import BcryptHasher
from datetime import datetime, timedelta, timezone
import logging
import uuid
import jwt
from src.config import Config

# ==========================================
# HASHING DE CONTRASEÑAS
# ==========================================
pass_context = PasswordHash((BcryptHasher(),))


def hash_password(password: str) -> str:
    return pass_context.hash(password)


def verify_password(password: str, hash_password: str) -> bool:
    return pass_context.verify(password, hash_password)


# ==========================================
# MANEJO DE JWT
# ==========================================
def create_access_token(user_data: dict, expiry: timedelta = None, refresh: bool = False) -> str:
    """
    Genera el token de acceso
    """
    payload = {
        'user': user_data,
        'exp': datetime.now(timezone.utc) + (expiry if expiry is not None else timedelta(minutes=60)),
        'jti': str(uuid.uuid4()),
        'refresh': refresh
    }

    token = jwt.encode(
        payload=payload,
        key=Config.JWT_SECRET,
        algorithm=Config.JWT_ALGORITHM
    )

    return token


def decode_token(token: str) -> dict | None:
    """
    Decodifica un token y retorna su carga util
    """
    try:
        token_data = jwt.decode(
            jwt=token,
            key=Config.JWT_SECRET,
            algorithms=[Config.JWT_ALGORITHM]
        )
        return token_data
    except jwt.PyJWTError as jwte:
        logging.exception(f"JWT error: {jwte}")
        return None
    except Exception as e:
        logging.exception(f"Error: {e}")
        return None
