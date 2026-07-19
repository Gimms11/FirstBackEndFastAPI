<<<<<<< HEAD
from fastapi import APIRouter, status, Depends
=======
from fastapi import APIRouter, HTTPException, status, Depends
>>>>>>> 2106935d3af0aff6b65db4b3bb76c43d52855a89
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
<<<<<<< HEAD
from src.errors import UserAlreadyExists, InvalidCredentials, InvalidToken

from src.celery_task import send_email_task
=======
>>>>>>> 2106935d3af0aff6b65db4b3bb76c43d52855a89

auth_router = APIRouter()
user_service = UserService()


@auth_router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def create_user(user_data: UserCreateModel, session: AsyncSession = Depends(get_session)) -> dict:
    """Crea un nuevo usuario, verificando que el correo y username no existan previamente."""
    existing_user = await user_service.get_user_by_email(user_data.email, session)
    if existing_user:
<<<<<<< HEAD
        raise UserAlreadyExists()
    existing_username = await user_service.get_user_by_username(user_data.username, session)
    if existing_username:
        raise UserAlreadyExists(message="Ya existe un usuario registrado con este nombre de usuario")
    
    new_user = await user_service.create_user(user_data, session)
    
    # 1. Definición de la plantilla adaptada a la marca
    html_template = f"""
    <html>
        <body style="font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background-color: #f4f6f9; padding: 20px; color: #2d3748;">
            <div style="max-width: 600px; margin: 0 auto; background-color: #ffffff; border-radius: 8px; padding: 30px; box-shadow: 0 4px 6px rgba(0,0,0,0.05); border-top: 4px solid #3182ce;">
                <h2 style="color: #2b6cb0; border-bottom: 2px solid #edf2f7; padding-bottom: 10px; margin-top: 0;">¡Bienvenido/a a nuestra Librería!</h2>
                <p>Hola <strong>{new_user.username}</strong>,</p>
                <p>Tu cuenta ha sido creada con éxito. Ya puedes acceder para explorar y gestionar todo nuestro catálogo literario.</p>
                
                <div style="background-color: #ebf8ff; border: 1px solid #bee3f8; border-radius: 6px; padding: 15px; margin: 20px 0;">
                    <p style="margin: 0; color: #2b6cb0;"><strong>Detalles de tu cuenta:</strong></p>
                    <p style="margin: 5px 0 0 0; font-size: 14px;"><strong>Usuario:</strong> {new_user.username}</p>
                    <p style="margin: 2px 0 0 0; font-size: 14px;"><strong>Correo registrado:</strong> {new_user.email}</p>
                </div>
                
                <p style="font-size: 12px; color: #a0aec0; margin-top: 30px; border-top: 1px solid #e2e8f0; padding-top: 15px; text-align: center;">
                    Librería API - Lectura sin límites.
                </p>
            </div>
        </body>
    </html>
    """
    
    # 2. Encolado de la tarea SMTP en segundo plano (tarda < 10ms en responder el endpoint)
    send_email_task.delay(
        email_to=new_user.email,
        subject="¡Bienvenido a la Librería! - Registro Exitoso",
        html_content=html_template
    )
    
=======
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
>>>>>>> 2106935d3af0aff6b65db4b3bb76c43d52855a89
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

<<<<<<< HEAD
    raise InvalidCredentials()
=======
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Correo o contraseña incorrectos"
    )
>>>>>>> 2106935d3af0aff6b65db4b3bb76c43d52855a89


@auth_router.get("/refresh_token")
async def get_new_access_token(token_details: dict = Depends(RefreshTokenBearer())):
    """Genera un nuevo access token usando el refresh token."""
    expiry_timestamp = token_details["exp"]

    if datetime.fromtimestamp(expiry_timestamp, timezone.utc) > datetime.now(timezone.utc):
        new_access_token = create_access_token(user_data=token_details["user"])
        return JSONResponse(content={"access_token": new_access_token})

<<<<<<< HEAD
    raise InvalidToken()
=======
    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail="El token ha expirado o es inválido"
    )
>>>>>>> 2106935d3af0aff6b65db4b3bb76c43d52855a89


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