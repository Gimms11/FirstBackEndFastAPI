import time
import logging
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.middleware.gzip import GZipMiddleware

# 1. Configuramos nuestro logger profesional
logger = logging.getLogger("bookly.access")
logger.setLevel(logging.INFO)
handler = logging.StreamHandler()
handler.setFormatter(logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s"))
logger.addHandler(handler)

def register_middleware(app: FastAPI) -> None:
    """Registra todos los middlewares de la aplicación."""
    
    # 2. Nuestro Custom Logging Middleware
    @app.middleware("http")
    async def custom_logging(request: Request, call_next):
        # Iniciamos el cronómetro de alta precisión
        start_time = time.perf_counter()
        
        # Pasamos la petición al siguiente middleware o a la ruta final
        response = await call_next(request)
        
        # Calculamos el tiempo total transcurrido
        processing_time = time.perf_counter() - start_time
        
        # Construimos el mensaje de registro
        client_ip = request.client.host if request.client else "Unknown"
        message = (
            f"{client_ip}:{request.client.port if request.client else 0} - "
            f"{request.method} - {request.url.path} - "
            f"{response.status_code} - completado en {processing_time:.4f}s"
        )
        
        # Imprimimos en consola utilizando el logger oficial
        logger.info(message)
        
        return response
    # ... código de custom_logging anterior ...

    # 3. Añadiendo CORS Middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  # En producción, reemplaza "*" por los dominios de tu frontend (ej. ["https://midominio.com"])
        allow_methods=["*"],  # Permite todos los métodos (GET, POST, PUT, DELETE, etc.)
        allow_headers=["*"],  # Permite todas las cabeceras
        allow_credentials=True,
    )

    # 4. Añadiendo Trusted Host Middleware
    app.add_middleware(
        TrustedHostMiddleware,
        allowed_hosts=["localhost", "127.0.0.1"], # Dominios válidos para procesar peticiones
    )

    # 5. Añadiendo GZip Middleware para compresión de respuestas
    app.add_middleware(
        GZipMiddleware,
        minimum_size=1000, # Comprime respuestas mayores a 1KB
    )