"""
Script para crear las tablas en MySQL
"""
from ..config.database import engine, Base, DATABASE_URL
from ..models.user import User
from ..models.pet import Pet, MedicalInfo, Document, Event

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