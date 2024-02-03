import pandas as pd
from conn import sap, mssql

def copy_data_from_sybase_to_sqlserver(tabla):
    # Conexión a Sybase
    sybase_conn = sap.conectar()
    
    # Consulta para contar la cantidad de columnas en Sybase
    column_count_query  = f"""SELECT COUNT(*) AS cantidad_de_columnas
                                  FROM syscolumns
                                  WHERE id = OBJECT_ID('SAPSR3.{tabla}')"""
    # Ejecutar la consulta para obtener la cantidad de columnas
    cursor = sybase_conn.cursor()
    cursor.execute(column_count_query )
    column_count  = cursor.fetchone()[0]
    cursor.close()

    # Consulta a la tabla especificada en Sybase
    sybase_query = f"SELECT * FROM SAPSR3.{tabla}"
    sybase_data = pd.read_sql_query(sybase_query, sybase_conn)
    
    # Cerrar conexión a Sybase
    sybase_conn.close()
    
    # Conexión a SQL Server
    sql_server_conn = mssql.conectar()
    
    # Insertar datos en SQL Server
    cursor = sql_server_conn.cursor()

    # Generar placeholders para la consulta de inserción
    placeholders = ', '.join(['?' for _ in range(column_count )])
    
    # Preparar la consulta de inserción
    sql_insert_query = f"INSERT INTO [dbo].[{tabla}] VALUES ({placeholders})"
    
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
    print('Proceso de inserción completado.')

# Función auxiliar para dividir una lista en trozos de tamaño n
def chunks(lst, n):
    for i in range(0, len(lst), n):
        yield lst[i:i + n]

# Llamar a la función para copiar los datos
copy_data_from_sybase_to_sqlserver('VBRP')
