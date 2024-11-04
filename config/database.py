"""
Creation of session for database connection
"""

import os
from sqlalchemy import create_engine
from sqlalchemy.orm.session import sessionmaker
from sqlalchemy.orm import declarative_base, configure_mappers
from sqlalchemy.exc import ArgumentError, InvalidRequestError
from dotenv import load_dotenv

load_dotenv()

base_dir = os.path.dirname(os.path.realpath(__file__))
database_url = os.getenv("DB_URL", f"sqlite:///{os.path.join(base_dir, '../develop.db')}")
db_url_develop = f"sqlite:///{os.path.join(base_dir, '../develop.db')}"

# if os.getenv("TESTING") == "1":
#     database_url = "sqlite:///:memory:"

engine = create_engine(database_url, echo=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    """Provides a database session for dependency injection."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

try:
    configure_mappers()
except (ArgumentError, InvalidRequestError) as e:
    print(f"Error configuring mappers: {e}")
