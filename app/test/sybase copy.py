import connsy

try:
    # Conectar a la base de datos
    cxnx = connsy.conectar()

    # Definir la consulta SQL
    storedProc = "SELECT TOP 10 * FROM SAPSR3.LIKP"

    # Crear un cursor
    cursor = cxnx.cursor()

    # Ejecutar la consulta SQL
    cursor.execute(storedProc)

    # Recuperar y procesar los resultados
    rows = cursor.fetchall()
    for row in rows:
        # Imprimir el segundo elemento de la fila (índice 1) si existe
        print(str(row[1] or ''))
        # Imprimir la fila completa
        print(row)

    # Cerrar el cursor y la conexión
    cursor.close()
    connsy.desconectar(cxnx)

except Exception as e:
    print("Error: %s" % e)
