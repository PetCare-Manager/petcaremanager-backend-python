"""
PetCareManager Backend built with FastAPI 
"""

from fastapi import FastAPI, HTTPException
from fastapi.exceptions import RequestValidationError
from starlette.middleware.base import BaseHTTPMiddleware

from config.database import engine, Base
from middlewares.cors import setup_cors
from middlewares.error_handler import ErrorHandler
from middlewares.exception_handlers import http_exception_handler, validation_exception_handler
from routers.user import user_router
from routers.password import pass_router
from routers.pet import pet_router

app = FastAPI(
    title="PetCare Manager",
    description="Manage your pets schedules, appointments, medicine",
    version="0.0.1",
)

setup_cors(app)
app.add_exception_handler(HTTPException, http_exception_handler)
app.add_exception_handler(RequestValidationError, validation_exception_handler)
app.add_middleware(ErrorHandler)

app.include_router(user_router, prefix="/api")
app.include_router(pass_router, prefix="/api/auth/password", tags=["Auth"])
app.include_router(pet_router, prefix="/api/pets", tags=["Pets"])

@app.get("/health", tags=["Health"])
def health_check():
    """Health Check"""
    return {"status": "ok"}

Base.metadata.create_all(bind=engine)


"""
Desarrollo para cambiar de SQLite a MySQL
1. Configurar la conexión a la base de datos para que sea dinámica
Usa variables de entorno para que el código detecte si está en local (SQLite) o en producción (MySQL en PythonAnywhere).

Ejemplo en Python (usando SQLAlchemy como referencia):

python
Copiar
Editar
import os

if os.getenv('PYTHONANYWHERE'):
    DB_USER = os.getenv('MYSQL_USER')
    DB_PASS = os.getenv('MYSQL_PASSWORD')
    DB_HOST = os.getenv('MYSQL_HOST')
    DB_NAME = os.getenv('MYSQL_DATABASE')

    DATABASE_URL = f"mysql+pymysql://{DB_USER}:{DB_PASS}@{DB_HOST}/{DB_NAME}"
else:
    DATABASE_URL = "sqlite:///./test.db"  # Desarrollo local
Luego usas DATABASE_URL para la conexión de tu ORM o driver.

2. Eliminar cualquier código que cree o use explícitamente test.db
Revisa que no haya código que fuerce la creación de SQLite.

Usa siempre la conexión configurada por variable de entorno.

3. Adaptar modelos y consultas para MySQL
Revisa tipos de datos, sintaxis y comportamientos SQL específicos.

Ajusta migraciones si usas algún framework (como Alembic).

4. Configurar entorno local para desarrollo
Localmente, dejar SQLite activo para desarrollo rápido y sencillo.

Puedes usar un flag o la variable PYTHONANYWHERE=1 para cambiar el entorno.

5. Configurar entorno de producción (PythonAnywhere y Docker)
Forzar el uso de MySQL a través de variables de entorno.

6. Testing
En pruebas unitarias y de integración, usar base de datos en memoria o mock para evitar usar SQLite o MySQL real.

Evitar crear o escribir en test.db.

7. Verificar que la aplicación:
Se conecta correctamente a MySQL en producción.

No utiliza SQLite ni genera archivos test.db.

Funciona igual o mejor con MySQL.

"""