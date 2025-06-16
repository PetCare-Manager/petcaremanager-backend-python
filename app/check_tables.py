import sqlite3

"""
Script para verificar la estructura y contenido de la base de datos SQLite.
Este script realiza las siguientes funciones:
1. Conecta a la base de datos 'develop.db'
2. Obtiene una lista de todas las tablas en la base de datos
3. Muestra la estructura de cada tabla (columnas y tipos de datos)
4. Cuenta el número de registros en cada tabla
Razón del script:
- Permite verificar rápidamente si la base de datos contiene las tablas esperadas
- Facilita la identificación de problemas en la estructura de la base de datos
- Ayuda a asegurar que la base de datos está en un estado correcto antes de realizar operaciones adicionales

Con esto tenemos la conclusion de que las tablas se crean cuando se ejecuta el comando `uvicorn app.main:app --reload` y que la base de datos se crea en el directorio actual.
"""

def check_db():
    try:
        # Conectar a la base de datos
        conn = sqlite3.connect('develop.db')
        cursor = conn.cursor()
        
        # Obtener todas las tablas
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()#recupera todas las tablas de la base de datos
        
        if tables:
            print("\n📋 Tablas encontradas:")
            for table in tables:
                print(f"- {table[0]}")
                # Mostrar estructura de la tabla
                cursor.execute(f"PRAGMA table_info({table[0]})")
                columns = cursor.fetchall()
                for col in columns:
                    print(f"  └─ {col[1]} ({col[2]})")
                # Contar registros
                cursor.execute(f"SELECT COUNT(*) FROM {table[0]}")
                count = cursor.fetchone()[0]# obtiene el primer elemento del resultado de la consulta devuelve none si hay menos filas
                print(f"  └─ {count} registros\n")
        else:
            print("❌ No se encontraron tablas en la base de datos")
        
    except Exception as e:
        print(f"❌ Error al verificar la base de datos: {e}")
    finally:
        if 'conn' in locals():
            conn.close()

if __name__ == '__main__':
    check_db()
