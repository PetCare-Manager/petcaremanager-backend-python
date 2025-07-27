from app.config.database_config import DatabaseConfig
from app.config.enums import Entorno
from app.config.exceptions import MissingConfigurationError
from sqlalchemy import create_engine
import pytest
import os

def test_config_engine_desarrollo_mysql_default(monkeypatch):
    """
    Test básico que verifica el comportamiento por defecto del sistema:
    
    OBJETIVO: Verificar que obtener_config_engine() funciona correctamente 
    en el escenario más común (desarrollo + MySQL por defecto).
    
    ESCENARIO:
    - Entorno: desarrollo 
    - Backend: MySQL (valor por defecto)
    - Configuración: Completa con pool de conexiones
    
    VERIFICACIONES:
    1. La configuración incluye echo=True (desarrollo)
    2. Incluye todas las configuraciones de pool MySQL
    3. Los valores de pool coinciden con los esperados
    4. No incluye configuraciones innecesarias
    """
    
    # ============ 1. ARRANGE: Preparar entorno por defecto ============
    # Limpiar variables que podrían interferir desde el .env
    monkeypatch.delenv("USE_MYSQL", raising=False)  # Usar valor por defecto (true)
    monkeypatch.delenv("DATABASE_URL", raising=False)  # No custom SQLite URL
    
    # Configurar entorno de desarrollo 
    monkeypatch.setenv("Entorno", "desarrollo")
    
    # Proporcionar credenciales MySQL requeridas
    monkeypatch.setenv("MYSQL_USER", "test_user")
    monkeypatch.setenv("MYSQL_PASSWORD", "test_password")
    monkeypatch.setenv("MYSQL_DATABASE", "test_database")
    
    # Opcional: Configurar algunos valores de pool personalizados para verificar
    monkeypatch.setenv("MYSQL_POOL_SIZE", "15")  # Diferente del default (10)
    monkeypatch.setenv("MYSQL_MAX_OVERFLOW", "25")  # Diferente del default (20)
    
    # ============ 2. ACT: Ejecutar el código a testear ============
    config = DatabaseConfig()
    engine_config = config.obtener_config_engine()
    
    # ============ 3. ASSERT: Verificar resultados ============
    
    # A) Verificar estructura básica
    assert isinstance(engine_config, dict), (
        f"TIPO_ERROR: obtener_config_engine() debe retornar dict. "
        f"Se obtuvo: {type(engine_config)}"
    )
    
    assert len(engine_config) > 1, (
        f"ESTRUCTURA_ERROR: En MySQL debe haber múltiples configuraciones. "
        f"Se obtuvo solo: {engine_config}"
    )
    
    # B) Verificar configuración de desarrollo (echo=True)
    assert engine_config.get("echo") is True, (
        f"ECHO_ERROR: En desarrollo, echo debe ser True. "
        f"Se obtuvo: echo={engine_config.get('echo')}. Config completa: {engine_config}"
    )
    
    # C) Verificar configuraciones de pool requeridas
    configuraciones_pool_requeridas = {
        "pool_size": int,
        "max_overflow": int, 
        "pool_timeout": int,
        "pool_recycle": int,
        "pool_pre_ping": bool
    }
    
    for key, expected_type in configuraciones_pool_requeridas.items():
        assert key in engine_config, (
            f"POOL_MISSING_ERROR: Falta configuración '{key}' en MySQL. "
            f"Config actual: {engine_config}"
        )
        
        assert isinstance(engine_config[key], expected_type), (
            f"POOL_TYPE_ERROR: '{key}' debe ser {expected_type.__name__}. "
            f"Se obtuvo: {type(engine_config[key])} = {engine_config[key]}"
        )
    
    # D) Verificar valores específicos configurados
    assert engine_config["pool_size"] == 15, (
        f"POOL_SIZE_ERROR: Debe usar valor configurado (15). "
        f"Se obtuvo: {engine_config['pool_size']}"
    )
    
    assert engine_config["max_overflow"] == 25, (
        f"MAX_OVERFLOW_ERROR: Debe usar valor configurado (25). "
        f"Se obtuvo: {engine_config['max_overflow']}"
    )
    
    # E) Verificar valores por defecto para configuraciones no especificadas
    assert engine_config["pool_timeout"] == 30, (
        f"POOL_TIMEOUT_ERROR: Sin configuración custom, debe usar default (30). "
        f"Se obtuvo: {engine_config['pool_timeout']}"
    )
    
    assert engine_config["pool_recycle"] == 3600, (
        f"POOL_RECYCLE_ERROR: Sin configuración custom, debe usar default (3600). "
        f"Se obtuvo: {engine_config['pool_recycle']}"
    )
    
    assert engine_config["pool_pre_ping"] is True, (
        f"POOL_PRE_PING_ERROR: Debe estar habilitado por defecto. "
        f"Se obtuvo: {engine_config['pool_pre_ping']}"
    )
    
    # F) Verificar que NO incluya configuraciones incorrectas
    configuraciones_no_esperadas = ["database_url", "charset", "host", "port"]
    for key in configuraciones_no_esperadas:
        assert key not in engine_config, (
            f"CONFIG_EXTRA_ERROR: '{key}' no debe estar en engine_config. "
            f"Config completa: {engine_config}"
        )
    
    # ============ 4. VERIFICACIONES ADICIONALES (Robustez) ============
    
    # G) Verificar que la configuración sea utilizable por SQLAlchemy
    try:
        from sqlalchemy import create_engine
        # Usar una URL de prueba para verificar que la config es válida
        #test_url = "sqlite:///:memory:"
        #test_engine = create_engine(test_url, **engine_config)->estas mezclando MySQL con SQLite esto no es correcto

        configuraciones_sqlite_validas = { # Esto es para probar que la config es válida
           "echo": engine_config["echo"]  # Toma solo la configuración 'echo' de MySQL para SQLite (filtrado)
        }
        test_url = "sqlite:///:memory:" # Crea una base de datos SQLite temporal en memoria (no en archivo)
        test_engine = create_engine(test_url, **configuraciones_sqlite_validas) # Crea engine SQLite con config filtrada
        
        assert test_engine is not None, "La configuración debe ser válida para SQLAlchemy" # Verifica que el engine se creó correctamente a traves de SQLite
    except Exception as e:
        assert False, f"CONFIG_INVALID_ERROR: Configuración inválida para SQLAlchemy: {e}"
    
    # H) Debug info para developers (solo visible con -s)
    print(f"\n=== ✅ TEST EXITOSO: Configuración MySQL en Desarrollo ===")
    print(f"🔧 Configuración generada: {engine_config}")
    print(f"📊 Total de parámetros: {len(engine_config)}")
    print(f"🎯 Echo habilitado: {engine_config['echo']}")
    print(f"🏊 Pool size: {engine_config['pool_size']}")
    print(f"⚡ Max overflow: {engine_config['max_overflow']}")
    
    # ============ 5. DOCUMENTAR COMPORTAMIENTO ESPERADO ============
    """
    CONFIGURACIÓN ESPERADA PARA DESARROLLO + MySQL:
    {
        "echo": True,                    # Debugging en desarrollo
        "pool_size": 15,                # Valor configurado custom
        "max_overflow": 25,             # Valor configurado custom  
        "pool_timeout": 30,             # Valor por defecto
        "pool_recycle": 3600,           # Valor por defecto (1 hora)
        "pool_pre_ping": True           # Verificación de conexiones
    }
    
    JUSTIFICACIÓN DE CADA VALOR:
    - echo=True: En desarrollo necesitamos ver las queries SQL
    - pool_size=15: Configuración custom para este test
    - max_overflow=25: Configuración custom para verificar lectura
    - pool_timeout=30: Default razonable para desarrollo
    - pool_recycle=3600: Reciclar conexiones cada hora
    - pool_pre_ping=True: Verificar que las conexiones estén vivas
    """

def test_config_engine_desarrollo_sqlite(monkeypatch):
    """
    Verifica que en entorno desarrollo con USE_MYSQL=false:
    1. Se use SQLite (no MySQL).
    2. La configuración del engine sea mínima (solo echo=True).
    3. No exista configuración de pool (incluso si está en DEFAULT_VALUES).
    4. La URL de conexión sea correcta (default o custom).
    5. El constructor no falle por validaciones de MySQL.
    """
    # ============ 1. Configuración del entorno ============
    monkeypatch.setenv("Entorno", "desarrollo")  # Forzar entorno desarrollo
    monkeypatch.setenv("USE_MYSQL", "false")     # Activar SQLite
    
    # Mockear variables obligatorias (el constructor las pide aunque no se usen)
    monkeypatch.setenv("MYSQL_USER", "test_user")
    monkeypatch.setenv("MYSQL_PASSWORD", "test_pass")
    monkeypatch.setenv("MYSQL_DATABASE", "test_db")
    
    # Opcional: Mockear DATABASE_URL para probar custom path
    monkeypatch.setenv("DATABASE_URL", "sqlite:///custom.db")

    # ============ 2. Ejecución ============
    config = DatabaseConfig()
    engine_config = config.obtener_config_engine()
    conexion_url = config.obtener_conexion_url()

    # ============ 3. Verificaciones PRINCIPALES ============
    # A) Configuración del engine
    assert engine_config == {"echo": True}, (
        f"CONFIG_ERROR: En SQLite, la configuración debe ser {{'echo': True}}. "
        f"Se obtuvo: {engine_config}. ¿Hay keys de MySQL?"
    )

    # B) URL de conexión
    assert conexion_url.startswith("sqlite:///"), (
        f"URL_ERROR: Debe empezar con 'sqlite:///'. URL obtenida: {conexion_url}"
    )
    assert "custom.db" in conexion_url, (
        f"URL_CUSTOM_ERROR: Debe usar DATABASE_URL mockeada. URL: {conexion_url}"
    )

    # ============ 4. Verificaciones SECUNDARIAS (pero importantes) ============
    # C) ¿Las keys de pool están ausentes?
    pool_keys = ["pool_size", "max_overflow", "pool_timeout", "pool_recycle"]
    for key in pool_keys:
        assert key not in engine_config, (
            f"POOL_ERROR: Key '{key}' no debe estar en SQLite. Config: {engine_config}"
        )

    # D) ¿La URL por defecto se usaría si no mockeamos DATABASE_URL?
    monkeypatch.delenv("DATABASE_URL", raising=False)
    default_config = DatabaseConfig()
    assert "develop.db" in default_config.obtener_conexion_url(), (
        f"DEFAULT_URL_ERROR: Sin DATABASE_URL, debe usar 'develop.db'. "
        f"URL obtenida: {default_config.obtener_conexion_url()}"
    )

    # E) ¿Las credenciales MySQL no afectan la URL de SQLite?
    monkeypatch.setenv("MYSQL_USER", "no_deberia_aparecer")
    assert "no_deberia_aparecer" not in config.obtener_conexion_url(), (
        f"MYSQL_LEAK_ERROR: Las creds de MySQL no deben afectar la URL de SQLite"
    )


    # Verificar que la URL no contiene credenciales de MySQL
    assert "mysql://" not in conexion_url
    # Verificar que el archivo se crea 
    engine = create_engine(config.obtener_conexion_url())
    engine.connect()  # Esto creará el archivo
    assert os.path.exists("develop.db") 
            
    print("\n=== RESULTADOS ===")
    print(f"URL de conexión: {config.obtener_conexion_url()}")
    print(f"Configuración del engine: {config.obtener_config_engine()}")
    
def test_config_engine_falla_sin_variables_mysql(monkeypatch):
    """Verifica que falla cuando faltan variables MySQL ANTES de crear el objeto"""
    # ============ 1. LIMPIAR variables existentes del .env ============
    # IMPORTANTE: Eliminar las variables que podrían venir del .env
    monkeypatch.delenv("MYSQL_USER", raising=False)
    monkeypatch.delenv("MYSQL_PASSWORD", raising=False)  
    monkeypatch.delenv("MYSQL_DATABASE", raising=False)
    monkeypatch.delenv("Entorno", raising=False)
    
    # ============ 2. Configurar entorno SIN variables MySQL ============
    monkeypatch.setenv("Entorno", "desarrollo")
    # NO seteamos MYSQL_USER, MYSQL_PASSWORD, MYSQL_DATABASE
    
    # ============ DEBUG: Verificar estado del entorno ============
    print(f"\n=== DEBUG DESPUÉS DE LIMPIAR ===")
    print(f"MYSQL_USER en entorno: {os.environ.get('MYSQL_USER')}")
    print(f"MYSQL_PASSWORD en entorno: {os.environ.get('MYSQL_PASSWORD')}")
    print(f"MYSQL_DATABASE en entorno: {os.environ.get('MYSQL_DATABASE')}")
    print(f"Entorno: {os.environ.get('Entorno')}")
    
    # ============ 3. Intentar crear DatabaseConfig (debe fallar) ============
    try:
        # CLAVE: cargar_dotenv=False evita que lea el archivo .env
        config = DatabaseConfig(cargar_dotenv=False)  # ← Ahora SÍ debe fallar
        print(f"\n=== PROBLEMA: DatabaseConfig se creó sin error ===")
        print(f"config.config: {config.config}")
        # Si llegamos aquí, algo está mal
        assert False, "DatabaseConfig() debería haber fallado pero no falló"
    except MissingConfigurationError as e:
        print(f"\n=== ÉXITO: MissingConfigurationError lanzada ===")
        print(f"Error: {e}")
        # Verificar que el error contiene las variables faltantes
        error_message = str(e)
        assert 'MYSQL_USER' in error_message, f"Error debe mencionar MYSQL_USER: {error_message}"
        assert 'MYSQL_PASSWORD' in error_message, f"Error debe mencionar MYSQL_PASSWORD: {error_message}"
        assert 'MYSQL_DATABASE' in error_message, f"Error debe mencionar MYSQL_DATABASE: {error_message}"

def test_config_engine_echo_por_entorno(monkeypatch):
    """
    Test simple que verifica el comportamiento de 'echo' según el entorno.
    
    OBJETIVO: Confirmar que echo=True en desarrollo y echo=False en pruebas/producción.
    
    Este test es más eficiente que 3 tests completos separados porque:
    - La única diferencia entre entornos es el valor de 'echo'
    - El resto de configuraciones (pool, etc.) son idénticas
    - Un test focado es más mantenible que 3 tests repetitivos
    """
    
    # Configuración base que todos los entornos necesitan
    monkeypatch.setenv("MYSQL_USER", "test_user")
    monkeypatch.setenv("MYSQL_PASSWORD", "test_password")
    monkeypatch.setenv("MYSQL_DATABASE", "test_database")
    
    # ============ DESARROLLO: echo=True ============
    monkeypatch.setenv("Entorno", "desarrollo")
    config_desarrollo = DatabaseConfig()
    engine_config_dev = config_desarrollo.obtener_config_engine()
    
    assert engine_config_dev["echo"] is True, (
        f"DESARROLLO_ERROR: En desarrollo, echo debe ser True. "
        f"Se obtuvo: {engine_config_dev['echo']}"
    )
    
    # ============ PRUEBAS: echo=False ============
    monkeypatch.setenv("Entorno", "pruebas")
    config_pruebas = DatabaseConfig()
    engine_config_test = config_pruebas.obtener_config_engine()
    
    assert engine_config_test["echo"] is False, (
        f"PRUEBAS_ERROR: En pruebas, echo debe ser False. "
        f"Se obtuvo: {engine_config_test['echo']}"
    )
    
    # ============ PRODUCCIÓN: echo=False ============
    monkeypatch.setenv("Entorno", "produccion")
    config_produccion = DatabaseConfig()
    engine_config_prod = config_produccion.obtener_config_engine()
    
    assert engine_config_prod["echo"] is False, (
        f"PRODUCCION_ERROR: En producción, echo debe ser False. "
        f"Se obtuvo: {engine_config_prod['echo']}"
    )
    
    # ============ VERIFICACIÓN ADICIONAL ============
    # Confirmar que el resto de configuraciones son consistentes
    # (pool_size, max_overflow, etc. deben ser iguales en todos los entornos)
    
    pool_configs = ["pool_size", "max_overflow", "pool_timeout", "pool_recycle", "pool_pre_ping"]
    
    for config_key in pool_configs:
        dev_value = engine_config_dev[config_key]
        test_value = engine_config_test[config_key] 
        prod_value = engine_config_prod[config_key]
        
        assert dev_value == test_value == prod_value, ( # Verifica que los valores sean iguales
            f"CONSISTENCIA_ERROR: '{config_key}' debe ser igual en todos los entornos. "
            f"Desarrollo: {dev_value}, Pruebas: {test_value}, Producción: {prod_value}"
        )
    
    # ============ DEBUG INFO ============
    print(f"\n=== ✅ VERIFICACIÓN DE ECHO POR ENTORNO ===")
    print(f"🏠 Desarrollo - echo: {engine_config_dev['echo']}")
    print(f"🧪 Pruebas - echo: {engine_config_test['echo']}")  
    print(f"🏢 Producción - echo: {engine_config_prod['echo']}")
    print(f"✅ Configuraciones de pool consistentes en todos los entornos")


def test_config_engine_pythonanywhere_desarrollo(monkeypatch):
    """
    Verifica configuración MySQL PythonAnywhere en desarrollo via detección PYTHONANYWHERE.
    
    OBJETIVO: Confirmar que cuando desarrollamos localmente pero queremos conectar
    a la base de datos real de PythonAnywhere, la configuración funcione correctamente
    usando la variable PYTHONANYWHERE="0" en lugar de Entorno="desarrollo".
    
    ESCENARIO:
    - Detección: PYTHONANYWHERE="0" (desarrollo en PythonAnywhere)
    - Variable Entorno: No configurada (para que PYTHONANYWHERE tenga precedencia)
    - Backend: MySQL forzado (credenciales específicas de PythonAnywhere)
    - Configuración: echo=True + pool completo con valores custom
    - Aislamiento: cargar_dotenv=False para evitar interferencia del .env
    
    VERIFICACIONES:
    1. Detección correcta del entorno como DESARROLLO via PYTHONANYWHERE="0"
    2. echo=True porque está en desarrollo (debugging habilitado)
    3. Configuraciones de pool presentes y con valores configurados (no defaults)
    4. URL de conexión MySQL con credenciales específicas de PythonAnywhere
    5. Formato correcto de host, base de datos y charset de PythonAnywhere
    
    DIFERENCIAS CON test_config_engine_desarrollo_mysql_default:
    - Usa PYTHONANYWHERE="0" vs Entorno="desarrollo" (diferentes métodos de detección)
    - Credenciales reales de PythonAnywhere vs credenciales genéricas de test
    - Valida URL completa para verificar integración con credenciales reales
    - Documenta el escenario real de desarrollo con base de datos en la nube
    
    VALOR DEL TEST:
    - Valida que las credenciales reales de PythonAnywhere funcionen
    - Documenta cómo configurar el proyecto para desarrollo con PA
    - Verifica que la detección por PYTHONANYWHERE funcione correctamente
    - Asegura que no hay conflictos entre variables de entorno
    """
    
    # ============ 1. ARRANGE: Preparar entorno PythonAnywhere desarrollo ============
    # Limpiar variables que podrían interferir con la detección
    monkeypatch.delenv("USE_MYSQL", raising=False)      # Usar valor por defecto (true)
    monkeypatch.delenv("DATABASE_URL", raising=False)   # No custom SQLite URL
    monkeypatch.delenv("Entorno", raising=False)        # Permitir detección por PYTHONANYWHERE
    
    # Configurar PythonAnywhere en modo desarrollo
    monkeypatch.setenv("PYTHONANYWHERE", "0")           # 0 = desarrollo en PA
    
    # Configurar credenciales específicas de PythonAnywhere
    monkeypatch.setenv("MYSQL_USER", "petcaremysql2")
    monkeypatch.setenv("MYSQL_PASSWORD", "Mheily88")
    monkeypatch.setenv("MYSQL_HOST", "petcaremysql2.mysql.pythonanywhere-services.com")
    monkeypatch.setenv("MYSQL_DATABASE", "petcaremysql2$default")
    
    # Configurar valores custom de pool para verificar lectura correcta
    monkeypatch.setenv("MYSQL_POOL_SIZE", "15")         # Diferente del default (10)
    monkeypatch.setenv("MYSQL_MAX_OVERFLOW", "25")      # Diferente del default (40)
    
    # ============ 2. ACT: Ejecutar código con aislamiento ============
    config = DatabaseConfig(cargar_dotenv=False)       # Evitar interferencia del .env
    engine_config = config.obtener_config_engine()
    conexion_url = config.obtener_conexion_url()
    
    # ============ 3. ASSERT: Verificar configuración completa ============
    
    # A) Verificar detección correcta del entorno
    assert config.obtener_entorno() == Entorno.DESARROLLO, (
        f"ENTORNO_ERROR: PYTHONANYWHERE='0' debe detectar DESARROLLO. "
        f"Se detectó: {config.obtener_entorno()}"
    )
    
    # B) Verificar configuración del engine
    """
    isinstance(objeto, tipo) → ¿Es engine_config un diccionario?

    ✅ Si es dict: isinstance({"echo": True}, dict) → True → test continúa
    ❌ Si NO es dict: isinstance("error", dict) → False → test falla
    """
    assert isinstance(engine_config, dict), (
        f"TIPO_ERROR: obtener_config_engine() debe retornar dict. "
        f"Se obtuvo: {type(engine_config)}"
    )
    
    assert engine_config["echo"] is True, (
        f"ECHO_ERROR: En desarrollo debe ser True para debugging. "
        f"Se obtuvo: {engine_config['echo']}"
    )
    
    assert engine_config["pool_size"] == 15, (
        f"POOL_SIZE_ERROR: Debe usar valor configurado (15). "
        f"Se obtuvo: {engine_config['pool_size']}"
    )
    
    assert engine_config["max_overflow"] == 25, (
        f"MAX_OVERFLOW_ERROR: Debe usar valor configurado (25). "
        f"Se obtuvo: {engine_config['max_overflow']}"
    )
    
    assert engine_config["pool_timeout"] == 30, (
        f"POOL_TIMEOUT_ERROR: Debe usar valor default (30). "
        f"Se obtuvo: {engine_config['pool_timeout']}"
    )
    
    assert engine_config["pool_pre_ping"] is True, (
        f"POOL_PRE_PING_ERROR: Debe estar habilitado para verificar conexiones. "
        f"Se obtuvo: {engine_config['pool_pre_ping']}"
    )
    
    # C) Verificar URL de conexión de PythonAnywhere
    assert isinstance(conexion_url, str), (
        f"URL_TIPO_ERROR: URL debe ser string. Se obtuvo: {type(conexion_url)}"
    )
    
    assert conexion_url.startswith("mysql://"), (
        f"URL_PROTOCOLO_ERROR: Debe usar protocolo MySQL. URL: {conexion_url}"
    )
    
    assert "petcaremysql2" in conexion_url, (
        f"URL_USER_ERROR: Debe contener usuario de PA. URL: {conexion_url}"
    )
    
    assert "pythonanywhere-services.com" in conexion_url, (
        f"URL_HOST_ERROR: Debe usar host de PA. URL: {conexion_url}"
    )
    
    assert "petcaremysql2$default" in conexion_url, (
        f"URL_DB_ERROR: Debe usar base de datos específica de PA. URL: {conexion_url}"
    )
    
    assert "charset=utf8mb4" in conexion_url, (
        f"URL_CHARSET_ERROR: Debe incluir charset. URL: {conexion_url}"
    )
    
    assert ":3306" in conexion_url, (
        f"URL_PORT_ERROR: Debe incluir puerto MySQL. URL: {conexion_url}"
    )
    
    # ============ 4. DEBUG INFO (visible con pytest -s) ============
    print(f"\n=== ✅ TEST EXITOSO: PythonAnywhere Desarrollo ===")
    print(f"🌍 Entorno detectado: {config.obtener_entorno()}")
    print(f"🔧 Configuración engine: {engine_config}")
    print(f"🔗 URL de conexión: {conexion_url}")
    print(f"✅ Detección via PYTHONANYWHERE funcionando correctamente")
    
    # ============ 5. DOCUMENTAR COMPORTAMIENTO ESPERADO ============
    """
    CONFIGURACIÓN ESPERADA PARA PYTHONANYWHERE DESARROLLO:
    
    Engine Config:
    {
        "echo": True,                    # Debugging en desarrollo
        "pool_size": 15,                # Valor configurado custom
        "max_overflow": 25,             # Valor configurado custom
        "pool_timeout": 30,             # Valor por defecto
        "pool_recycle": 3600,           # Valor por defecto
        "pool_pre_ping": True           # Verificación de conexiones
    }
    
    URL de Conexión:
    mysql://petcaremysql2:Mheily88@petcaremysql2.mysql.pythonanywhere-services.com:3306/petcaremysql2$default?charset=utf8mb4
    
    JUSTIFICACIÓN DE CADA VALOR:
    - echo=True: En desarrollo necesitamos ver las queries SQL
    - pool_size=15: Configuración custom para este test
    - credenciales reales: Verifican que la integración con PA funcione
    - cargar_dotenv=False: Aislamiento total del archivo .env
    """

def test_config_engine_pythonanywhere_produccion(monkeypatch):
    """
    Verifica configuracion MySQL PythonAnywhere en producción:
    configuración final para el deploy
    """

    # ============ 1. ARRANGE ============
    # Limpiar variables...
    # Configurar PYTHONANYWHERE...
    # Configurar credenciales...
    
    # ============ 2. ACT ============
    # config = DatabaseConfig()
    # engine_config = ...
    
    # ============ 3. ASSERT ============
    # Tus 5 asserts...

def test_config_engine_pythonanywhere_pruebas(monkeypatch):
    """
    Verifica configuracion MySQL PythonAnywhere en pruebas:
    configuración para pruebas unitarias con base de datos en PythonAnywhere
    """

    # ============ 1. ARRANGE ============
    # Limpiar variables...
    # Configurar PYTHONANYWHERE...
    # Configurar credenciales...
    
    # ============ 2. ACT ============
    # config = DatabaseConfig()
    # engine_config = ...
    
    # ============ 3. ASSERT ============
    # Tus 5 asserts...

