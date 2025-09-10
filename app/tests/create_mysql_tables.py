"""
Script para crear las tablas en MySQL
"""
import sys
import os

# Agregar el directorio padre al path para permitir importaciones absolutas
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from app.config.database import engine, Base, DATABASE_URL
from app.models.user import User
from app.models.pet import Pet, MedicalInfo, Document, Event

def create_tables():
    print(f"🔨 Creando tablas en: {DATABASE_URL}")
    
    try:
        # Esto creará TODAS las tablas definidas
        Base.metadata.create_all(bind=engine)
        print("✅ Tablas creadas exitosamente")
        
        # Mostrar las tablas creadas
        print("\n📋 Tablas creadas:")
        for table in Base.metadata.tables:
            print(f"  - {table}")
            
    except Exception as e:
        print(f"❌ Error al crear tablas: {e}")
        print("\n💡 Verifica que:")
        print("  - Los modelos tengan longitudes en campos String")
        print("  - Las credenciales MySQL sean correctas")
        print("  - La base de datos exista")

if __name__ == "__main__":
    create_tables()

 #uvicorn main:app --reload
# Verificar http://localhost:8000/health