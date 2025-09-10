import sqlite3
import os
from pathlib import Path


"""
Script para exportar la base de datos SQLite a un archivo SQL compatible con MySQL.

Este script realiza las siguientes funciones:
1. Crea un volcado (dump) completo de la base de datos 'develop.db'
2. Guarda el contenido en 'backup_sqlite.sql' incluyendo:
   - Estructura de las tablas
   - Datos almacenados
   - Índices y restricciones
3. Realiza ajustes para compatibilidad con MySQL:
   - Ajusta tipos de datos
   - Maneja correctamente las claves foráneas
   - Asegura la codificación UTF-8

El resultado (backup_sqlite.sql) contendrá todas las sentencias SQL
necesarias para recrear la base de datos en MySQL posteriormente.
"""

def adjust_for_mysql(line):
    """Ajusta las sentencias SQL para hacerlas compatibles con MySQL."""
    # Reemplazar tipos de datos SQLite por equivalentes MySQL
    line = line.replace('AUTOINCREMENT', 'AUTO_INCREMENT')
    line = line.replace('INTEGER PRIMARY KEY', 'INTEGER PRIMARY KEY AUTO_INCREMENT')
    line = line.replace('DATETIME DEFAULT CURRENT_TIMESTAMP', 'DATETIME DEFAULT CURRENT_TIMESTAMP')
    
    # Ajustar sintaxis específica de SQLite
    if line.startswith('CREATE TABLE'):
        line = line.replace('CREATE TABLE', 'CREATE TABLE IF NOT EXISTS')
    
    return line

def dump_db():
    try:
        # Obtener la ruta absoluta del directorio actual
        base_dir = Path(__file__).parent.absolute()
        db_path = base_dir / 'develop.db'
        backup_path = base_dir / 'backup_sqlite.sql'
        
        if not db_path.exists():
            raise FileNotFoundError(f"No se encontró la base de datos en {db_path}")
        
        # Conectar a la base de datos
        conn = sqlite3.connect(str(db_path))
        
        # Configurar la codificación UTF-8
        conn.text_factory = str
        
        print(f"📦 Iniciando exportación de la base de datos desde {db_path}")
        print(f"📝 El archivo de respaldo se guardará en {backup_path}")
        
        # Abrir el archivo de salida
        with open(backup_path, 'w', encoding='utf-8') as f:
            # Agregar configuración inicial de MySQL
            f.write("SET FOREIGN_KEY_CHECKS=0;\n")
            f.write("SET SQL_MODE='NO_AUTO_VALUE_ON_ZERO';\n")
            f.write("SET NAMES utf8mb4;\n\n")
            
            # Procesar cada línea del dump
            for line in conn.iterdump():
                # Ajustar la línea para compatibilidad con MySQL
                adjusted_line = adjust_for_mysql(line)
                f.write(f'{adjusted_line}\n')
            
            # Restaurar configuración de MySQL
            f.write("\nSET FOREIGN_KEY_CHECKS=1;\n")
        
        print("✅ Base de datos exportada exitosamente a backup_sqlite.sql")
        print("🔍 Verificando el archivo de respaldo...")
        
        # Verificar que el archivo se creó correctamente
        if backup_path.exists() and backup_path.stat().st_size > 0:
            print(f"📊 Tamaño del archivo de respaldo: {backup_path.stat().st_size / 1024:.2f} KB")
        else:
            raise Exception("El archivo de respaldo está vacío o no se creó correctamente")
        
    except FileNotFoundError as e:
        print(f"❌ Error: {e}")
        print("💡 Asegúrate de que el archivo develop.db existe en el directorio correcto")
    except Exception as e:
        print(f"❌ Error al exportar la base de datos: {e}")
    finally:
        if 'conn' in locals():
            conn.close()

if __name__ == '__main__':
    dump_db()
