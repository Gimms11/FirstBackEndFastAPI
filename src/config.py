from pydantic_settings import BaseSettings, SettingsConfigDict
from datetime import timedelta

<<<<<<< HEAD
from pydantic import EmailStr

=======
>>>>>>> 2106935d3af0aff6b65db4b3bb76c43d52855a89
class Settings(BaseSettings):
    DATABASE_URL: str
    JWT_SECRET: str
    JWT_ALGORITHM: str
    REFRESH_TOKEN_EXPIRY_DAYS: int
    REDIS_HOST: str = "localhost"
    REDIS_PORT: int = 6379
<<<<<<< HEAD
    
    # Tareas en segundo plano (Celery)
    REDIS_URL: str = "redis://localhost:6379/0"

    # Credenciales y servidor SMTP
    MAIL_USERNAME: str
    MAIL_PASSWORD: str
    MAIL_PORT: int
    MAIL_SERVER: str
    MAIL_FROM: EmailStr
    MAIL_FROM_NAME: str
=======
>>>>>>> 2106935d3af0aff6b65db4b3bb76c43d52855a89

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    @property
    def REFRESH_TOKEN_EXPIRY_DAYS(self) -> timedelta:
        return timedelta(days=self.REFRESH_TOKEN_EXPIRY_DAYS)

Config = Settings()