import pandas as pd
import pyodbc


def copy_data_from_sybase_to_sqlserver():
    # Conexión a Sybase
    sybase_conn = pyodbc.connect(
                            DRIVER='{Adaptive Server Enterprise}',
                            SERVER='nombre_servidor',
                            PORT='puerto',
                            DATABASE='nombre_base_de_datos',
                            UID='usuario',
                            PWD='contraseña')

    
    # Consulta a la tabla VBRK en Sybase
    sybase_query = "SELECT * FROM VBRK"
    sybase_data = pd.read_sql_query(sybase_query, sybase_conn)
    
    # Conexión a SQL Server
    sql_server_conn = pyodbc.connect('DRIVER={SQL Server};SERVER=server_name;DATABASE=database_name;UID=username;PWD=password')

    # Insertar datos en SQL Server
    cursor = sql_server_conn.cursor()
    for index, row in sybase_data.iterrows():
        # Insertar cada fila en SQL Server
        cursor.execute("""
            INSERT INTO VBRK (column1, column2, ..., columnN) 
            VALUES (?, ?, ..., ?)
        """, tuple(row))
    
    # Confirmar los cambios
    sql_server_conn.commit()
    
    # Cerrar conexiones
    cursor.close()
    sybase_conn.close()
    sql_server_conn.close()

# Llamar a la función para copiar los datos
copy_data_from_sybase_to_sqlserver()
