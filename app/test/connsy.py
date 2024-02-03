import pyodbc as po

# Variables de conexión
server = '10.130.10.101'
database = 'PRD'
username = 'sapsa'
password = 'Info@2015'
port ='4901'
cursor=None

# Función para conectar a la base de datos
def conectar():
    try:
        # Cadena de conexión
        cnxn = po.connect('DRIVER={Devart ODBC Driver for ASE};'
                          'SERVER=' + server +
                          ';DATABASE=' + database +
                          ';UID=' + username +
                          ';PWD=' + password +
                          ';PORT=' + port)
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
        print("Conexión exitosa.")
        # Aquí puedes realizar operaciones en la base de datos
        # Por ejemplo, ejecutar consultas
        # Recuerda manejar adecuadamente las excepciones y cerrar la conexión cuando hayas terminado
        desconectar(conexion)
    else:
        print("No se pudo establecer la conexión.")

