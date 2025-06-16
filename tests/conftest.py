import os
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.config.database import Base

# Usar base de datos en memoria para pruebas
@pytest.fixture(scope="session")
def engine():
    engine = create_engine("sqlite:///:memory:", echo=True)
    Base.metadata.create_all(bind=engine)
    return engine

@pytest.fixture(scope="session")
def TestingSessionLocal(engine):
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    return SessionLocal

@pytest.fixture
def db_session(TestingSessionLocal):
    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.rollback()
        session.close()
