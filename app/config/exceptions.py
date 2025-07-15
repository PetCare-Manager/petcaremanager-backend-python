# Nueva clase para excepciones personalizadas
class DatabaseConfigError(Exception):
    """Excepcion base para errores de configuracion de base de datos"""

    def __init__(self, message: str):
        self.message=message #Guarda al mensaje de la instancia
        super().__init__(self.message)# llama al constructor de la clase Excepction

class MissingConfigurationError(DatabaseConfigError):
    """
    Se lanza cuando faltan variables de configuracion necesarias.
    """
    def __init__(self, nombredevariablesquefaltan:str):
        self.nombredevariablesquefaltan = nombredevariablesquefaltan
        super().__init__(f"Faltan las siguientes variables de configuración requeridas: {','.join(nombredevariablesquefaltan)}") #join para poner las variables con comas

class InvalidConfigurationError(DatabaseConfigError):
    """
    Se lanza cuando la configuracion de la base de datos es invalida.
    """
    def __init__(self, variableserroneas: dict):# las variables erroneas van en un diccionario porque podemos asociar el nombre de la variable con el error
        self.variableserroneas = variableserroneas

        mensaje = "\n".join([
           
           f"{variable}: {error} configuracion invalida"

           for variable,error in variableserroneas.items()
        ])

        super().__init__(mensaje)

class ConnectionConfigError(DatabaseConfigError):
    """
    Se lanza cuando hay problemas con los parametros de conexion"""

    def __init__(self, connection_error: str):
        message = f"Error en la configuración de conexión: {connection_error}"
        super().__init__(message)

class PoolConfigError(DatabaseConfigError):
    """Se lanza cuando hay problemas con la configuración del pool de conexiones"""
    def __init__(self, pool_error: str):
        message = f"Error en la configuración del pool: {pool_error}"
        super().__init__(message)

class EnvironmentError(DatabaseConfigError):
    """Se lanza cuando hay problemas con la configuración del entorno"""
    def __init__(self, environment: str):
        message = f"Error en la configuración del entorno: {environment}"
        super().__init__(message)