from fastapi import FastAPI
from contextlib import asynccontextmanager

from src.modules.books.router import book_router
from src.modules.authors.router import author_router
from src.modules.auth.router import auth_router
from src.modules.reviews.router import review_router
from src.modules.tags.router import tag_router
from src.database.main import init_db

<<<<<<< HEAD
from .errors import register_error_handlers
from .middleware import register_middleware  # Importamos nuestra función

=======
>>>>>>> 2106935d3af0aff6b65db4b3bb76c43d52855a89

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Iniciando la aplicacion")
    await init_db()
    yield
    print("Apagando la aplicacion")


<<<<<<< HEAD
description = """
### 🚀 Arquitectura Backend Empresarial - API de Libros y Autores

Esta API REST modular ha sido diseñada por **Albert Mijael Garayar Munive** bajo los principios de **Clean Architecture** y una **Service Layer** robusta para garantizar la escalabilidad, mantenibilidad y el desacoplamiento del sistema.

#### 🛠️ Características Clave:
* **Persistencia Asíncrona**: Acceso a datos altamente eficiente utilizando **SQLAlchemy / SQLModel** y **PostgreSQL**.
* **Seguridad Enterprise**: Autenticación y autorización basada en tokens **JWT** con invalidación activa mediante una lista de bloqueo (**Redis Blocklist**).
* **Control de Acceso basado en Roles (RBAC)**: Restricciones de seguridad avanzadas en endpoints críticos.
* **Procesamiento en Segundo Plano**: Integración con **Celery** y **Redis** para el manejo de tareas asíncronas.
* **Gestión Completa**: Control de libros, autores, reseñas y etiquetas (*tags*).

#### 👤 Información del Desarrollador:
* **Desarrollador**: Albert Mijael Garayar Munive (Tech Lead & Full Stack Software Engineer)
* **Correo**: [mijael.gara@gmail.com](mailto:mijael.gara@gmail.com)
* **GitHub**: [github.com/Gimms11](https://github.com/Gimms11)
* **LinkedIn**: [linkedin.com/in/albert-mijael-garayar-munive/](https://linkedin.com/in/albert-mijael-garayar-munive/)
"""

=======
>>>>>>> 2106935d3af0aff6b65db4b3bb76c43d52855a89
version = "v1"

app = FastAPI(
    version=version,
<<<<<<< HEAD
    title="Arquitectura Backend Empresarial - API de Libros",
    description=description,
    lifespan=lifespan,
    contact={
        "name": "Albert Mijael Garayar Munive",
        "url": "https://github.com/Gimms11",
        "email": "mijael.gara@gmail.com",
    },
    license_info={
        "name": "MIT License",
        "url": "https://opensource.org/licenses/MIT",
    },
    docs_url="/docs",
    redoc_url="/redoc",
)

register_error_handlers(app)
register_middleware(app)  # ¡Registramos nuestros Middlewares aquí!

=======
    title="API de Libros",
    description="API para gestionar libros",
    lifespan=lifespan,
)

>>>>>>> 2106935d3af0aff6b65db4b3bb76c43d52855a89
app.include_router(book_router, prefix=f"/api/{version}", tags=["Books"])
app.include_router(author_router, prefix=f"/api/{version}", tags=["Authors"])
app.include_router(auth_router, prefix=f"/api/{version}/auth", tags=["Auth"])
app.include_router(review_router, prefix=f"/api/{version}/reviews", tags=["Reviews"])
app.include_router(tag_router, prefix=f"/api/{version}/tags", tags=["Tags"])