"""
Tests para verificar que el modelo Pet y relacionados son compatibles con MySQL
"""
import pytest
from models.pet import Pet, MedicalInfo, Document, Event, Gender


class TestPetModel:
    """Tests para el modelo Pet"""
    
    def test_all_string_fields_have_length(self):
        """Verificar que todos los String tienen longitud para MySQL"""
        models_to_check = [Pet, MedicalInfo, Document, Event]
        
        for model in models_to_check:
            for column in model.__table__.columns:
                if column.type.__class__.__name__ == 'String':
                    assert hasattr(column.type, 'length'), \
                        f"Modelo {model.__name__}, campo {column.name} sin longitud"
    
    def test_enum_configuration(self):
        """Verificar que el enum Gender está bien configurado"""
        gender_column = Pet.__table__.columns['gender']
        
        # Verificar que es un Enum
        assert gender_column.type.__class__.__name__ == 'Enum'
        
        # Verificar que tiene nombre (importante para MySQL)
        assert hasattr(gender_column.type, 'name'), "Enum debe tener nombre para MySQL"
    
    def test_foreign_keys_have_cascade(self):
        """Verificar que las foreign keys tienen CASCADE"""
        pet_user_fk = Pet.__table__.columns['user_id']
        
        # Buscar la foreign key
        for fk in Pet.__table__.foreign_keys:
            if fk.parent == pet_user_fk:
                assert fk.ondelete == 'CASCADE', "Foreign key debe tener ON DELETE CASCADE"
    
    def test_table_args_for_mysql(self):
        """Verificar __table_args__ para MySQL"""
        assert hasattr(Pet, '__table_args__'), "Pet debe tener __table_args__"
        
        table_args = Pet.__table_args__
        assert 'mysql_engine' in table_args, "Debe especificar engine MySQL"
        assert table_args['mysql_engine'] == 'InnoDB', "Debe usar InnoDB"
        assert 'mysql_charset' in table_args, "Debe especificar charset"
        assert table_args['mysql_charset'] == 'utf8mb4', "Debe usar utf8mb4"
    
    def test_text_fields_for_long_content(self):
        """Verificar que campos de texto largo usan Text no String"""
        # medication y allergies deberían ser Text
        medication = MedicalInfo.__table__.columns['medication']
        allergies = MedicalInfo.__table__.columns['allergies']
        
        assert medication.type.__class__.__name__ == 'Text', \
            "medication debe ser Text para contenido largo"
        assert allergies.type.__class__.__name__ == 'Text', \
            "allergies debe ser Text para contenido largo"