from fastapi_mail import FastMail, ConnectionConfig
from src.config import Config

mail_config = ConnectionConfig(
    MAIL_USERNAME=Config.MAIL_USERNAME,
    MAIL_PASSWORD=Config.MAIL_PASSWORD,
    MAIL_FROM=Config.MAIL_FROM,
    MAIL_PORT=Config.MAIL_PORT,
    MAIL_SERVER=Config.MAIL_SERVER,
    MAIL_FROM_NAME=Config.MAIL_FROM_NAME,
    MAIL_STARTTLS=True,      # Requerido por Gmail en puerto 587
    MAIL_SSL_TLS=False,      # TLS se inicia mediante STARTTLS en el puerto 587
    USE_CREDENTIALS=True,    # Autenticar con usuario y contraseña
    VALIDATE_CERTS=True      # Validar certificados SSL para evitar ataques Man-In-The-Middle
)

mail_client = FastMail(mail_config)