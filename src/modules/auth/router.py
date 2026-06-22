from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.responses import JSONResponse
from sqlmodel.ext.asyncio.session import AsyncSession
from datetime import timedelta, datetime, timezone

from src.modules.auth.schemas import UserResponse, UserLoginModel, UserCreateModel, UserBooksModel
from src.modules.auth.service import UserService
from src.modules.auth.utils import verify_password, create_access_token
from src.core.security import AccessTokenBearer, RefreshTokenBearer
from src.core.dependencies import get_current_user
from src.database.models import User
from src.database.main import get_session
from src.database.redis import add_jti_to_blocklist
from src.config import Config

auth_router = APIRouter()
user_service = UserService()


@auth_router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def create_user(user_data: UserCreateModel, session: AsyncSession = Depends(get_session)) -> dict:
    """Crea un nuevo usuario, verificando que el correo y username no existan previamente."""
    existing_user = await user_service.get_user_by_email(user_data.email, session)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El correo ya existe"
        )
    existing_username = await user_service.get_user_by_username(user_data.username, session)
    if existing_username:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El username ya existe"
        )
    new_user = await user_service.create_user(user_data, session)
    return {"message": "Usuario creado exitosamente", "user": new_user}


@auth_router.post("/login", response_model=UserResponse, status_code=status.HTTP_202_ACCEPTED)
async def login_user(login_data: UserLoginModel, session: AsyncSession = Depends(get_session)) -> dict:
    """Autentica al usuario y devuelve tokens de acceso."""
    email = login_data.email
    password = login_data.password

    existing_user = await user_service.get_user_by_email(email, session)

    if existing_user:
        password_valid = verify_password(password, existing_user.password_hash)

        if password_valid:
            access_token = create_access_token(
                user_data={"email": existing_user.email, "user_uid": str(existing_user.uid)}
            )

            refresh_token = create_access_token(
                user_data={"email": existing_user.email, "user_uid": str(existing_user.uid)},
                expiry=timedelta(days=Config.REFRESH_TOKEN_EXPIRY_DAYS),
                refresh=True
            )

            return JSONResponse(
                content={
                    "message": "Login Exitoso",
                    "access_token": access_token,
                    "refresh_token": refresh_token,
                    "user": {"email": existing_user.email, "uid": str(existing_user.uid)}
                }
            )

    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Correo o contraseña incorrectos"
    )


@auth_router.get("/refresh_token")
async def get_new_access_token(token_details: dict = Depends(RefreshTokenBearer())):
    """Genera un nuevo access token usando el refresh token."""
    expiry_timestamp = token_details["exp"]

    if datetime.fromtimestamp(expiry_timestamp, timezone.utc) > datetime.now(timezone.utc):
        new_access_token = create_access_token(user_data=token_details["user"])
        return JSONResponse(content={"access_token": new_access_token})

    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail="El token ha expirado o es inválido"
    )


@auth_router.get('/logout')
async def revoke_token(token_details: dict = Depends(AccessTokenBearer())):
    """Revoca el token de acceso actual."""
    jti = token_details['jti']

    await add_jti_to_blocklist(jti)

    return JSONResponse(
        content={"message": "Cierre de sesión exitoso"},
        status_code=status.HTTP_200_OK
    )

@auth_router.get("/me", response_model=UserBooksModel)
async def get_current_user_profile(
    user: User = Depends(get_current_user)
):
    # SQLModel ya cargó 'user.books' gracias a lazy="selectin"
    return user