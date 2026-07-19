from celery import Celery
from asgiref.sync import async_to_sync
from fastapi_mail import MessageSchema, MessageType
from src.mail import mail_client
from src.config import Config

# Inicialización de la aplicación Celery
celery_app = Celery(
    "bookstore_tasks",
    broker=Config.REDIS_URL,
    backend=Config.REDIS_URL
)

# Configuración adicional para estabilidad y zona horaria
celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="America/Lima",
    enable_utc=True,
    broker_connection_retry_on_startup=True
)

@celery_app.task(
    name="send_transactional_email_task",
    bind=True,               # Permite acceder a la instancia de la tarea (self)
    max_retries=5,           # Reintentos máximos ante caídas de conexión o rate limit
    default_retry_delay=15   # Segundos de espera base entre reintentos
)
def send_email_task(self, email_to: str, subject: str, html_content: str):
    """
    Tarea síncrona de Celery que ejecuta de forma segura el envío asíncrono
    de correos a través de async_to_sync de asgiref.
    """
    message = MessageSchema(
        subject=subject,
        recipients=[email_to],
        body=html_content,
        subtype=MessageType.html
    )
    
    try:
        # async_to_sync bloquea el hilo del worker hasta que se complete la operación SMTP
        async_to_sync(mail_client.send_message)(message)
        return {"status": "success", "recipient": email_to}
    
    except Exception as exc:
        # En caso de fallo temporal, auto-reintentar con backoff
        raise self.retry(exc=exc)
