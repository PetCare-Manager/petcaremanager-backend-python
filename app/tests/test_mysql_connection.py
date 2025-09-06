"""
Script para verificar conexión a MySQL antes de crear tablas
"""
from sqlalchemy import text
from config.database import engine, DATABASE_URL

def test_connection():
    print(f"🔍 Probando conexión a: {DATABASE_URL}")
    try:
        with engine.connect() as conn:
            result = conn.execute(text("SELECT 1"))
            print("✅ Conexión exitosa a MySQL")
            
            # Verificar base de datos
            result = conn.execute(text("SELECT DATABASE()"))
            db_name = result.scalar()
            print(f"📊 Base de datos actual: {db_name}")
            
    except Exception as e:
        print(f"❌ Error de conexión: {e}")
        return False
    return True

if __name__ == "__main__":
    test_connection()