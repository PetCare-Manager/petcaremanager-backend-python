"""
Mantiene la conexion y sesiones a la base de datos

create_engine usa la URL y config de tu clase para conectar.

sessionmaker crea sesiones para manejar transacciones y consultas.

scoped_session asegura que la sesión sea segura para contextos concurrentes.

get_db es una función generadora típica para frameworks web, para abrir y cerrar sesiones automáticamente.

"""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session, declarative_base
from app.config.database_config import database_config  # Importa la factory de configuración

# Crear instancia de configuración
config = database_config()

# Obtener la URL de conexión (MySQL o SQLite según entorno)
DATABASE_URL = config.obtener_conexion_url()

# Obtener la configuración para el engine (pool, echo, etc)
ENGINE_CONFIG = config.obtener_config_engine()

# Crear el engine de SQLAlchemy
engine = create_engine(DATABASE_URL, **ENGINE_CONFIG)

# Crear la sesión para interacción con la DB
SessionLocal = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))
#sessionmaker(...) define cómo crear sesiones configuradas.
#scoped_session(...) garantiza que cada hilo/request use su propia sesión segura.
#La variable SessionLocal es un objeto que cuando se llama crea o retorna la sesión adecuada para ese contexto.

# Crear la clase base para los modelos
Base = declarative_base()

"""

Base = lista de tus tablas.

ORM = traductor entre Python y SQL.

Alembic = aplica cambios (migraciones) usando la info de Base.

💥 Si no defines Base, nada de esto funciona.

"""

def get_db():
    """
    Dependency para usar en frameworks (FastAPI, Flask, etc)
    Genera una sesión para cada request y la cierra después.
    """
    db = SessionLocal()
    try:
        yield db # Devuelve la sesión para el request actual
    finally:
        db.close() # Esta línea cierra la sesión después del request
