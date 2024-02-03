import pandas as pd
from conn import sap,mssql


def copy_data_from_sybase_to_sqlserver():
    # Conexión a Sybase
    sybase_conn = sap.conectar()

    
    # Consulta a la tabla VBRK en Sybase
    sybase_query = "SELECT * FROM SAPSR3.VBRK"
    sybase_data = pd.read_sql_query(sybase_query, sybase_conn)
    
    # Conexión a SQL Server
    sql_server_conn = mssql.conectar()

    # Insertar datos en SQL Server
    cursor = sql_server_conn.cursor()

    placeholders = ', '.join(['?' for _ in range(114)])
    print(placeholders)

    for index, row in sybase_data.iterrows():
        # Insertar cada fila en SQL Server
        cursor.execute(f"""
            INSERT INTO [dbo].[VBRK]
           ([MANDT]
           ,[VBELN]
           ,[FKART]
           ,[FKTYP]
           ,[VBTYP]
           ,[WAERK]
           ,[VKORG]
           ,[VTWEG]
           ,[KALSM]
           ,[KNUMV]
           ,[VSBED]
           ,[FKDAT]
           ,[BELNR]
           ,[GJAHR]
           ,[POPER]
           ,[KONDA]
           ,[KDGRP]
           ,[BZIRK]
           ,[PLTYP]
           ,[INCO1]
           ,[INCO2]
           ,[EXPKZ]
           ,[RFBSK]
           ,[MRNKZ]
           ,[KURRF]
           ,[CPKUR]
           ,[VALTG]
           ,[VALDT]
           ,[ZTERM]
           ,[ZLSCH]
           ,[KTGRD]
           ,[LAND1]
           ,[REGIO]
           ,[COUNC]
           ,[CITYC]
           ,[BUKRS]
           ,[TAXK1]
           ,[TAXK2]
           ,[TAXK3]
           ,[TAXK4]
           ,[TAXK5]
           ,[TAXK6]
           ,[TAXK7]
           ,[TAXK8]
           ,[TAXK9]
           ,[NETWR]
           ,[ZUKRI]
           ,[ERNAM]
           ,[ERZET]
           ,[ERDAT]
           ,[STAFO]
           ,[KUNRG]
           ,[KUNAG]
           ,[MABER]
           ,[STWAE]
           ,[EXNUM]
           ,[STCEG]
           ,[AEDAT]
           ,[SFAKN]
           ,[KNUMA]
           ,[FKART_RL]
           ,[FKDAT_RL]
           ,[KURST]
           ,[MSCHL]
           ,[MANSP]
           ,[SPART]
           ,[KKBER]
           ,[KNKLI]
           ,[CMWAE]
           ,[CMKUF]
           ,[HITYP_PR]
           ,[BSTNK_VF]
           ,[VBUND]
           ,[FKART_AB]
           ,[KAPPL]
           ,[LANDTX]
           ,[STCEG_H]
           ,[STCEG_L]
           ,[XBLNR]
           ,[ZUONR]
           ,[MWSBK]
           ,[LOGSYS]
           ,[FKSTO]
           ,[XEGDR]
           ,[RPLNR]
           ,[LCNUM]
           ,[J_1AFITP]
           ,[KURRF_DAT]
           ,[AKWAE]
           ,[AKKUR]
           ,[KIDNO]
           ,[BVTYP]
           ,[NUMPG]
           ,[BUPLA]
           ,[VKONT]
           ,[FKK_DOCSTAT]
           ,[NRZAS]
           ,[SPE_BILLING_IND]
           ,[VTREF]
           ,[FK_SOURCE_SYS]
           ,[FKTYP_CRM]
           ,[STGRD]
           ,[VBTYP_EXT]
           ,[J_1TPBUPL]
           ,[INCOV]
           ,[INCO2_L]
           ,[INCO3_L]
           ,[DPC_REL]
           ,[MNDID]
           ,[PAY_TYPE]
           ,[SEPON]
           ,[MNDVG]
           ,[SPPAYM]
           ,[SPPORD])
     VALUES ({placeholders})
        """, tuple(row))
    
    # Confirmar los cambios
    sql_server_conn.commit()
    
    # Cerrar conexiones
    cursor.close()
    sybase_conn.close()
    sql_server_conn.close()

# Llamar a la función para copiar los datos
copy_data_from_sybase_to_sqlserver()
