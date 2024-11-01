"""
Creation of session for database connection
"""

import os
from sqlalchemy import create_engine
from sqlalchemy.orm.session import sessionmaker
from sqlalchemy.orm import declarative_base
from dotenv import load_dotenv

load_dotenv()

base_dir = os.path.dirname(os.path.realpath(__file__))
database_url = os.getenv("DATABASE_URL", f"sqlite:///{os.path.join(base_dir, '../dev.db')}")

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
