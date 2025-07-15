import os
from typing import Dict,Any
from .exceptions import (
    DatabaseConfigError,
    MissingConfigurationError,  
    InvalidConfigurationError,
    ConnectionConfigError,
    PoolConfigError,
    EnvironmentError
)
from .enums import Entorno 
from dotenv import load_dotenv

class DatabaseConfig:
    """
    Clase para manejar la configuracion de base de datos
    """
    REQUIRED_VARS = [

        "MYSQL_USER",
        "MYSQL_PASSWORD",
        "MYSQL_DATABASE",
    ]

    DEFAULT_VALUES = {
        "MYSQL_HOST": "petcaremysql.mysql.pythonanywhere-services.com",
        "MYSQL_PORT": "3306",
        "MYSQL_CHARSET": "utf8mb4",
        "USE_MYSQL": "true",
        #Un pool de conexiones es un conjunto de conexiones abiertas a la base de datos que se mantienen disponibles para que las aplicaciones las reutilicen, en lugar de abrir y cerrar conexiones repetidamente
        "MYSQL_POOL_SIZE": 10,        # Suficiente para MVP
        "MYSQL_MAX_OVERFLOW": 40,     # 4x pool_size para picos
        "MYSQL_POOL_TIMEOUT": 30,     # 30 segundos es razonable
        "MYSQL_POOL_RECYCLE": 3600,   # Reciclar cada hora
        "POOL_PRE_PING": True   # Verificar conexiones
    }

    def __init__(self):
        """Inicializa y valida la configuración"""
        load_dotenv() 
        self.config = {} # Diccionario para almacenar la configuración
        self.cargar_config()
        self.validar_config()

    def cargar_config(self) -> None:

        # Primero, cargar valores requeridos
        for var in self.REQUIRED_VARS:
            self.config[var] = os.getenv(var)

        # Luego, cargar valores con defaults
        for var, default in self.DEFAULT_VALUES.items():
            self.config[var] = os.getenv(var, default)
        
    def validar_config(self) -> None:
        self._validar_variables_requeridas()
        self._validar_parametros_conexion()
        self._validar_config_pool()

    # Método privados solo para uso interno de la clase _
    def _validar_variables_requeridas(self):
        """Valida que existan todas las variables requeridas"""
        
        # Verificar si faltan variables requeridas a partir del diccionario de configuración 
        variables_inexistentes = [  # Se crea una lista con los nombres de las variables requeridas que no están definidas.Esto es una lista por comprensión creas listas  a patir de un for con opc una condición
            var for var in self.REQUIRED_VARS  # Se recorre cada variable requerida definida en self.REQUIRED_VARS
            if not self.config.get(var)  # Se verifica si la variable no existe o tiene un valor "falsy" en self.config (por ejemplo: None, '', 0)
        ]#"Recorre cada var en self.REQUIRED_VARS, y si self.config.get(var) es falsy (None, '', 0...), entonces añade var a la lista."
        
        # Si hay variables que faltan, lanzar excepción
        if variables_inexistentes:  # Si la lista no está vacía, significa que hay variables faltantes
            raise MissingConfigurationError(variables_inexistentes)  # Se lanza una excepción personalizada con la lista de variables faltantes
            
    def _validar_parametros_conexion(self) -> None:
        """Valida los parámetros de conexión"""
        # Validar host
        host = self.config.get("MYSQL_HOST")
        if host and (";" in host or "'" in host or '"' in host):
            raise ConnectionConfigError("Host contiene caracteres no permitidos")

        # Validar puerto
        try:
            port = int(self.config.get("MYSQL_PORT", "3306"))
            if not (1024 <= port <= 65535):
                raise ConnectionConfigError(f"Puerto {port} fuera del rango válido (1024-65535)")
        except ValueError:
            raise InvalidConfigurationError({"MYSQL_PORT": "Debe ser un número válido"})

    def _validar_config_pool(self) -> None:
        """Valida la configuración del pool de conexiones"""
        try:
            pool_size = int(self.config.get("MYSQL_POOL_SIZE", "10"))
            max_overflow = int(self.config.get("MYSQL_MAX_OVERFLOW", "20"))
            pool_timeout = int(self.config.get("MYSQL_POOL_TIMEOUT", "30"))
            pool_recycle = int(self.config.get("MYSQL_POOL_RECYCLE", "3600"))
            
            if pool_size < 1:
                raise PoolConfigError("pool_size debe ser mayor que 0")
            if max_overflow < 0:
                raise PoolConfigError("max_overflow no puede ser negativo")
            if pool_timeout < 1:
                raise PoolConfigError("pool_timeout debe ser mayor que 0")
            if pool_recycle < 60:
                raise PoolConfigError("pool_recycle debe ser al menos 60 segundos")
                
        except ValueError as e:
            raise InvalidConfigurationError({
                "pool_config": f"Valores numéricos inválidos: {str(e)}"
            })
        

    def _validar_entorno(self) -> Entorno:
        """Determina y valida el entorno actual basado en variables de entorno"""
        
        # Verificar si existe la variable PYTHONANYWHERE
        pythonanywhere_value = os.getenv("PYTHONANYWHERE")
        
        # Verificar si existe la variable Entorno
        entorno_value = os.getenv("Entorno")
        
        # Si no existe ninguna variable de entorno, lanzar excepción
        if pythonanywhere_value is None and entorno_value is None:
            raise MissingConfigurationError(["PYTHONANYWHERE", "Entorno"])
        
        # Priorizar la variable Entorno si está definida porque es más explícita porque define el entorno directamente para el usuario para que no tenga que adivinar si está en PythonAnywhere o no
        if entorno_value is not None:
            entorno_value = entorno_value.lower().strip()
            
            # Obtener valores válidos directamente del enum Entorno
            entornos_validos = [entorno.value for entorno in Entorno]
            
            if entorno_value not in entornos_validos:
                raise InvalidConfigurationError({
                    "Entorno": f"Valor '{entorno_value}' no válido. Valores permitidos: {', '.join(entornos_validos)}"
                })
            
            # Buscar y retornar el enum correspondiente
            for entorno in Entorno:
                if entorno.value == entorno_value:
                    return entorno
        
        # Si no hay variable Entorno, usar PYTHONANYWHERE
        if pythonanywhere_value is not None:
            if pythonanywhere_value == "1":
                return Entorno.PRODUCCION
            elif pythonanywhere_value == "0":
                return Entorno.DESARROLLO
            else:
                raise InvalidConfigurationError({
                    "PYTHONANYWHERE": f"Valor '{pythonanywhere_value}' no válido. Valores permitidos: '0' (desarrollo) o '1' (producción)"
                })
        
        # Si llegamos aquí, hay un problema con la configuración
        raise EnvironmentError("No se pudo determinar el entorno. Verifique las variables PYTHONANYWHERE o Entorno")
        

    def obtener_conexion_url(self) -> str:
        """Construye y retorna la URL de conexión basada en el entorno"""
        entorno = self.obtener_entorno() # Llama al método para validar el entorno para obtener el entorno actual
        
        # En desarrollo, permitir SQLite si USE_MYSQL es false
        if entorno == Entorno.DESARROLLO and self.config.get("USE_MYSQL", "true").lower() == "false": #"Si el entorno es de desarrollo y la variable de configuración USE_MYSQL está definida como 'false' (ignorando mayúsculas), entonces..."
            return os.getenv("DATABASE_URL", "sqlite:///./develop.db") # Usa la URL de SQLite definida en el .env o una por defecto
        
        # En cualquier otro caso, usar MySQL
        return (
            f"mysql://{self.config['MYSQL_USER']}:{self.config['MYSQL_PASSWORD']}"
            f"@{self.config['MYSQL_HOST']}:{self.config['MYSQL_PORT']}"
            f"/{self.config['MYSQL_DATABASE']}?charset={self.config['MYSQL_CHARSET']}"
        )

    # Método para obtener la configuración del motor de base de datos
    # Este método retorna un diccionario con los parámetros necesarios para crear el engine de SQLAlchemy
    # Que es una herramienta que permite interactuar con bases de datos de manera más sencilla para los desarrolladores

    #El engine es el núcleo de la conexión a la base de datos
    #Funciona como un "motor" que gestiona las conexiones
    #Es el puente entre tu código Python y la base de datos MySQL
    #¿Qué hace?

    #Maneja el pool de conexiones
    #Traduce código Python a SQL
    #Gestiona las transacciones
    #Optimiza el rendimiento
    #Analogía: Imagina un hotel:

    #El engine es como el sistema de gestión del hotel
    #El pool son las habitaciones disponibles
    #Las conexiones son como los huéspedes
    #El pool_size es el número de habitaciones base
    #El max_overflow son habitaciones extra para emergencias
    
    def obtener_config_engine(self) -> Dict[str, Any]:
        """
        Retorna la configuración para create_engine.
        Este método construye y devuelve un diccionario con los parámetros necesarios
        para crear el engine de SQLAlchemy, que es el componente que permite conectar 
        la aplicación con la base de datos.
        Dependiendo del entorno (desarrollo o producción) y si se usa MySQL o SQLite, 
        se agregan configuraciones específicas como el tamaño del pool de conexiones, 
        tiempo de espera, etc.
        """
        
        # Determina el entorno actual (DESARROLLO o PRODUCCION) a través del método privado.
        entorno = self.obtener_entorno()

        # Diccionario base de configuración del engine.
        # La clave "echo" activa la impresión de todas las queries SQL en consola, 
        # lo cual es útil en desarrollo para debug.
        config = {
            "echo": True if entorno == Entorno.DESARROLLO else False,
        }

        # Verifica si se está en PRODUCCIÓN o si explícitamente se indicó usar MySQL.
        # Esto incluye también el caso en desarrollo donde USE_MYSQL está en "true".
        # En ese caso, se agregan parámetros específicos para el pool de conexiones.
        if entorno != Entorno.DESARROLLO or self.config.get("USE_MYSQL", "true").lower() == "true":

            # Agrega la configuración del pool al diccionario:
            config.update({
                # Número máximo de conexiones simultáneas mantenidas activas en el pool.
                "pool_size": int(self.config.get("MYSQL_POOL_SIZE", "10")),

                # Número máximo de conexiones adicionales que se pueden crear temporalmente
                # cuando el pool está lleno.
                "max_overflow": int(self.config.get("MYSQL_MAX_OVERFLOW", "20")),

                # Tiempo máximo en segundos que se espera para obtener una conexión del pool
                # antes de lanzar un error.
                "pool_timeout": int(self.config.get("MYSQL_POOL_TIMEOUT", "30")),

                # Tiempo (en segundos) después del cual una conexión del pool se recicla 
                # (se cierra y se abre una nueva). Ayuda a evitar desconexiones inactivas.
                "pool_recycle": int(self.config.get("MYSQL_POOL_RECYCLE", "3600")),

                # Verifica que la conexión esté viva antes de usarla. Evita errores con
                # conexiones muertas.
                "pool_pre_ping": True
            })

        # Devuelve el diccionario completo de configuración para el engine.
        return config
    
    def obtener_entorno(self) -> Entorno:
        # método público para obtener el entorno validado
        return self._validar_entorno()

def database_config() -> DatabaseConfig:
    """
    Función helper para facilitar el uso. Factory function para crear una instancia de DatabaseConfig
    Te da una forma clara y reutilizable de obtener la config de base de datos. Permite encapsular lógica futura si lo necesitás
    Mejora la legibilidad y mantenibilidad del código
    """
    return DatabaseConfig()