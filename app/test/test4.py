import pandas as pd
from conn import sap, mssql

def copy_data_from_sybase_to_sqlserver(tabla, column, data):
    # Conexión a Sybase
    sybase_conn = sap.conectar()
    
    # Consulta a la tabla especificada en Sybase
    sybase_query = f"SELECT * FROM SAPSR3.{tabla} WHERE {column}>='{data}'"
    sybase_data = pd.read_sql_query(sybase_query, sybase_conn)
    
    # Cerrar conexión a Sybase
    sybase_conn.close()
    
    # Conexión a SQL Server
    sql_server_conn = mssql.conectar()

    # Eliminar primero los datos según el criterio WHERE en SQL Server
    delete_query = f"DELETE FROM [dbo].[{tabla}] WHERE {column}>='{data}'"
    cursor = sql_server_conn.cursor()
    cursor.execute(delete_query)
    sql_server_conn.commit()
    
    # Insertar los nuevos datos desde Sybase a SQL Server
    cursor = sql_server_conn.cursor()
    placeholders = ', '.join(['?' for _ in range(len(sybase_data.columns))])
    columns = ', '.join(sybase_data.columns)
    sql_insert_query = f"INSERT INTO [dbo].[{tabla}] ({columns}) VALUES ({placeholders})"
    
    # Convertir los datos de Pandas DataFrame a una lista de tuplas
    data_tuples = [tuple(row) for row in sybase_data.itertuples(index=False)]
    
    total_rows = len(data_tuples)
    rows_inserted = 0
    
    # Ejecutar la consulta de inserción de manera masiva
    for chunk in chunks(data_tuples, 1000):  # Dividir los datos en lotes de 1000 filas
        cursor.executemany(sql_insert_query, chunk)
        rows_inserted += len(chunk)
        print(f'Progreso: {rows_inserted}/{total_rows} filas insertadas')
    
    # Confirmar los cambios
    sql_server_conn.commit()
    
    # Cerrar conexiones
    cursor.close()
    sql_server_conn.close()
    
    print('Proceso completado.')

# Función auxiliar para dividir una lista en trozos de tamaño n
def chunks(lst, n):
    for i in range(0, len(lst), n):
        yield lst[i:i + n]

# Llamar a la función para copiar los datos
copy_data_from_sybase_to_sqlserver('VBRP', 'ERDAT', '20240101')
