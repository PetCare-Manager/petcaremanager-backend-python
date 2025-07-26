# tests/config/conftest.py
import os
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from unittest.mock import patch
from app.config.database import Base

@pytest.fixture(scope="session")
def engine():
    """Fixture para crear motor SQLite en memoria"""
    return create_engine("sqlite:///:memory:", echo=True)

@pytest.fixture(scope="session")
def setup_database(engine):
    """Configuración inicial de la base de datos"""
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)

@pytest.fixture
def db_session(engine, setup_database):
    """Sesión de base de datos para tests"""
    Session = sessionmaker(bind=engine)
    session = Session()
    try:
        yield session
    finally:
        session.rollback()
        session.close()

@pytest.fixture
def mock_env(monkeypatch):
    """Fixture para mockear variables de entorno"""
    monkeypatch.setenv("MYSQL_USER", "test_user")
    monkeypatch.setenv("MYSQL_PASSWORD", "test_pass")
    monkeypatch.setenv("MYSQL_DATABASE", "test_db")
    monkeypatch.setenv("Entorno", "desarrollo")
    return monkeypatch

@pytest.fixture
def database_config(mock_env):
    """Fixture para DatabaseConfig con mocks"""
    with patch('dotenv.load_dotenv'):
        from app.config.database_config import DatabaseConfig
        return DatabaseConfig(cargar_dotenv=False)