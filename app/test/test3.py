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
    cursor.execute(delete_query)
    sql_server_conn.commit()
    
    # Consulta para identificar filas que faltan en SQL Server
    sql_check_query = f"SELECT * FROM [dbo].[{tabla}] WHERE {column}>='{data}'"
    existing_data = pd.read_sql_query(sql_check_query, sql_server_conn)
    
    # Identificar las filas que faltan en SQL Server pero están en Sybase
    missing_data = sybase_data[~sybase_data.isin(existing_data)].dropna()
        
    # Verificar si hay datos faltantes para determinar si se debe insertar
    if not missing_data.empty:
        # Insertar solo las filas que faltan en SQL Server
        cursor = sql_server_conn.cursor()
        
        # Construir la consulta de inserción dinámicamente
        placeholders = ', '.join(['?' for _ in range(len(missing_data.columns))])
        columns = ', '.join(missing_data.columns)
        sql_insert_query = f"INSERT INTO [dbo].[{tabla}] ({columns}) VALUES ({placeholders})"
        
        # Convertir los datos de Pandas DataFrame a una lista de tuplas
        data_tuples = [tuple(row) for row in missing_data.itertuples(index=False)]
        
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
    else:
        print("No hay diferencias entre las tablas. No se requiere inserción.")
    
    sql_server_conn.close()
    print('Proceso completado.')

# Función auxiliar para dividir una lista en trozos de tamaño n
def chunks(lst, n):
    for i in range(0, len(lst), n):
        yield lst[i:i + n]

# Llamar a la función para copiar los datos
copy_data_from_sybase_to_sqlserver('VBRP', 'ERDAT', '20240201')
