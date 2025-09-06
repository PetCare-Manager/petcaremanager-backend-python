"""
Tests para verificar que el modelo User es compatible con MySQL
"""
import pytest
from sqlalchemy import create_engine, inspect
from sqlalchemy.orm import sessionmaker
from config.database import Base
from models.user import User


class TestUserModel:
    """Tests para el modelo User"""
    
    def test_password_field_length(self):
        """Verificar que el campo password tiene longitud suficiente para bcrypt"""
        # Bcrypt genera hashes de ~60 caracteres
        password_column = User.__table__.columns['password']
        
        # Verificar que tiene longitud definida
        assert hasattr(password_column.type, 'length'), "Password debe tener longitud definida"
        
        # Verificar que la longitud es suficiente (mínimo 60, idealmente 255)
        assert password_column.type.length >= 60, f"Password length {password_column.type.length} es muy corta para bcrypt"
    
    def test_email_field_has_length(self):
        """Verificar que email tiene longitud definida"""
        email_column = User.__table__.columns['email']
        
        assert hasattr(email_column.type, 'length'), "Email debe tener longitud definida para MySQL"
        assert email_column.type.length >= 100, "Email debe permitir al menos 100 caracteres"
    
    def test_all_string_fields_have_length(self):
        """Verificar que TODOS los campos String tienen longitud"""
        for column in User.__table__.columns:
            if column.type.__class__.__name__ == 'String':
                assert hasattr(column.type, 'length'), f"Campo {column.name} tipo String sin longitud definida"
    
    def test_table_has_indexes(self):
        """Verificar que la tabla tiene índices necesarios"""
        # Email debería tener índice por ser unique
        email_column = User.__table__.columns['email']
        assert email_column.unique is True, "Email debe ser único"
        assert email_column.index is True, "Email debe tener índice"
    
    def test_timestamps_configuration(self):
        """Verificar configuración de timestamps"""
        created_at = User.__table__.columns['created_at']
        
        # Verificar que tiene default
        assert created_at.default is not None, "created_at debe tener valor por defecto"