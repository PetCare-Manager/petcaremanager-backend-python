"""
Verificar estructura de tablas en MySQL
"""
from sqlalchemy import text, inspect
from config.database import engine

def verify_tables():
    inspector = inspect(engine)
    
    # Listar todas las tablas
    tables = inspector.get_table_names()
    print(f"📊 Tablas encontradas: {len(tables)}")
    
    for table in tables:
        print(f"\n📋 Tabla: {table}")
        
        # Mostrar columnas
        columns = inspector.get_columns(table)
        for col in columns:
            print(f"  - {col['name']}: {col['type']} {'NOT NULL' if not col['nullable'] else 'NULL'}")

if __name__ == "__main__":
    verify_tables()