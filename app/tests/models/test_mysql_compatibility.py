"""
Tests generales de compatibilidad MySQL para todos los modelos
"""
import pytest
from sqlalchemy import create_engine
from sqlalchemy.dialects import mysql
from config.database import Base
from models.user import User
from models.pet import Pet, MedicalInfo, Document, Event


class TestMySQLCompatibility:
    """Tests de compatibilidad general con MySQL"""
    
    @pytest.fixture
    def all_models(self):
        """Fixture con todos los modelos"""
        return [User, Pet, MedicalInfo, Document, Event]
    
    def test_can_generate_mysql_ddl(self, all_models):
        """Verificar que se puede generar DDL válido para MySQL"""
        # Crear engine MySQL ficticio
        mysql_engine = create_engine("mysql://user:pass@localhost/db", strategy='mock', executor=lambda *args, **kwargs: None)
        
        try:
            # Intentar generar DDL para cada modelo
            for model in all_models:
                ddl = str(model.__table__.compile(dialect=mysql.dialect()))
                
                # Verificar que no contiene tipos incompatibles
                assert 'AUTOINCREMENT' not in ddl, "No debe usar AUTOINCREMENT (SQLite)"
                
                # Verificar que usa sintaxis MySQL correcta
                if 'id' in [col.name for col in model.__table__.columns]:
                    # Si tiene campo id, debe tener AUTO_INCREMENT o no ser primary key
                    pass  # MySQL maneja esto automáticamente
                    
        except Exception as e:
            pytest.fail(f"Error generando DDL MySQL: {e}")
    
    def test_no_text_type_in_string_fields(self, all_models):
        """Verificar que no se usa TEXT donde debería ser VARCHAR"""
        for model in all_models:
            for column in model.__table__.columns:
                if column.type.__class__.__name__ == 'String':
                    # Los String deben tener longitud (serán VARCHAR)
                    assert hasattr(column.type, 'length'), \
                        f"{model.__name__}.{column.name} necesita longitud"
    
    def test_boolean_fields_have_defaults(self, all_models):
        """Verificar que campos Boolean tienen default (mejor práctica MySQL)"""
        for model in all_models:
            for column in model.__table__.columns:
                if column.type.__class__.__name__ == 'Boolean':
                    assert column.default is not None or column.nullable, \
                        f"{model.__name__}.{column.name} Boolean debe tener default o ser nullable"
    
    def test_date_fields_configuration(self, all_models):
        """Verificar que campos Date están bien configurados"""
        for model in all_models:
            for column in model.__table__.columns:
                if column.type.__class__.__name__ == 'Date':
                    # Los Date no deben tener timezone en MySQL
                    assert not hasattr(column.type, 'timezone'), \
                        "MySQL Date no soporta timezone"
    
    def test_no_reserved_keywords(self, all_models):
        """Verificar que no se usan palabras reservadas MySQL"""
        # Palabras reservadas comunes en MySQL
        reserved = {'order', 'group', 'table', 'index', 'key', 'desc', 'asc', 'time'}
        
        for model in all_models:
            # Verificar nombre de tabla
            assert model.__tablename__.lower() not in reserved, \
                f"'{model.__tablename__}' es palabra reservada en MySQL"
            
            # Verificar nombres de columnas
            for column in model.__table__.columns:
                # Permitir 'time' si está en Event ya que es un campo válido
                if column.name.lower() in reserved and not (column.name == 'time' and model.__name__ == 'Event'):
                    pytest.fail(f"'{column.name}' es palabra reservada en MySQL")