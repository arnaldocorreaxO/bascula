import pyodbc as po
import jaydebeapi
import jpype
from config.conn import SYBASE_PARAMS as params
from config.settings import BASE_DIR 
import os


# # Ruta al archivo JAR del controlador JDBC
# jdbc_driver_name = "com.sybase.jdbc4.jdbc.SybDriver"
# jdbc_driver_name = "com.sybase.jdbc3.jdbc.SybDriver"
# # jdbc_driver_loc = "/path/to/jconn4.jar"  # Cambia esta ruta por la ubicación de tu archivo JAR
# jdbc_driver_loc = os.path.join(BASE_DIR, 'driver', 'jconn4-16.0.jar')  # Asumiendo que el archivo JAR está en ../driver
# jdbc_driver_loc = os.path.join(BASE_DIR, 'driver', 'jconn3-6.0.jar')  # Asumiendo que el archivo JAR está en ../driver

# Información de conexión a la base de datos
host = params['server']  # Dirección del servidor Sybase
port = params['port']        # Puerto del servidor Sybase (modifica según tu configuración)
database = params['database']   # Nombre de la base de datos
user = params['username']  # Usuario de la base de datos
password =  params['password']   # Contraseña de la base de datos

# Variables globales para la conexión
conn = None
cursor = None

# Función para conectar a la base de datos
def conectar():
    try:
        # Cadena de conexión
        cnxn = po.connect('DRIVER=' + params['driver']+
                        'SERVER=' + params['server'] +
                        ';DATABASE=' + params['database'] +
                        ';UID=' + params['username'] +
                        ';PWD=' + params['password'] +
                        ';PORT=' + params['port'])
        return cnxn
    except Exception as e:
        print("Error al conectar: %s" % e)

# Función para desconectar de la base de datos
def desconectar(cnxn):
    try:
        # Cerrar la conexión a la base de datos
        cnxn.close()
    except Exception as e:
        print("Error al desconectar: %s" % e)

# Ejemplo de uso
if __name__ == "__main__":
    # Conectar a la base de datos
    conexion = conectar()
    if conexion:
        print("Conexión exitosa a SYBASE")
        # Aquí puedes realizar operaciones en la base de datos
        # Por ejemplo, ejecutar consultas
        # Recuerda manejar adecuadamente las excepciones y cerrar la conexión cuando hayas terminado
        desconectar(conexion)
    else:
        print("No se pudo establecer la conexión.")


# Función para conectar a la base de datos

# def conectar2():
#     global conn, cursor
#     try:
#         # Iniciar la JVM si no está corriendo
#         if not jpype.isJVMStarted():
#             jpype.startJVM(jpype.getDefaultJVMPath(), "-Djava.class.path=" + jdbc_driver_loc)

#         # Verificar si la JVM se inició correctamente
#         if not jpype.isJVMStarted():
#             raise RuntimeError("No se pudo iniciar la JVM. Verifica la configuración.")

#         # JDBC URL para conectarse a la base de datos Sybase
#         url = f"jdbc:sybase:Tds:{host}:{port}/{database}"
#         print("###############################################")
#         print(jdbc_driver_name)
#         print(url)
#         print("###############################################")
#         # Conexión a la base de datos
#         conn = jaydebeapi.connect(jdbc_driver_name, url, {'user': user, 'password': password}, jdbc_driver_loc)
#         print("Conexión establecida correctamente")
#         # Retornar la conexión
#         return conn
       

#     except jaydebeapi.DatabaseError as e:
#         print("Error: No se pudo conectar a la base de datos. Verifica los datos de conexión y credenciales.", e)

#     except RuntimeError as e:
#         print("Error crítico:", e)

#     except Exception as e:
#         print("Ocurrió un error inesperado:", e)

#         # Verificar si hay SQLWarnings disponibles
#         if hasattr(e, "args") and len(e.args) > 0:
#             print("Detalles adicionales del error:")
#             for detail in e.args:
#                 print(detail)
        
#         # Intentar obtener información del objeto Java subyacente
#         if jpype.isJVMStarted() and hasattr(e, "_java_exception"):
#             java_exception = e._java_exception
#             print("Excepción Java subyacente:", java_exception)
            
#             # Verificar si la excepción tiene SQLWarnings
#             try:
#                 sql_warning = java_exception.getSQLWarning()  # Método típico en JDBC
#                 if sql_warning:
#                     print("SQLWarnings encontrados:")
#                     while sql_warning:
#                         print(sql_warning.getMessage())
#                         sql_warning = sql_warning.getNextWarning()
#             except AttributeError:
#                 print("El objeto Java no contiene SQLWarnings.")



# # Función para desconectar de la base de datos
# def desconectar2():
#     global conn, cursor

#     if cursor:
#         cursor.close()
#         print("Cursor cerrado.")
#     if conn:
#         conn.close()
#         print("Conexión cerrada.")

#     # Detener la JVM cuando ya no sea necesario
#     if jpype.isJVMStarted():
#         jpype.shutdownJVM()
#         print("JVM apagada.")