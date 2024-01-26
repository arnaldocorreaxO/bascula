#!/usr/bin/python
import os
import time
import serial
from core.views import print_separador

def leer_puerto_serial(configuracion):
    puerto_serial = serial.Serial()

    puerto_serial.port = configuracion.puerto
    puerto_serial.baudrate = configuracion.bits_por_segundo
    puerto_serial.bytesize = configuracion.bits_de_datos
    puerto_serial.parity = configuracion.paridad
    puerto_serial.stopbits = configuracion.bits_de_parada
    puerto_serial.timeout = 0

    try:
        if not puerto_serial.isOpen():
            puerto_serial.open()
            print_separador()
            print(puerto_serial)

    except Exception as error:
        print(f"ERROR ABRIENDO PUERTO SERIAL: {error}")
        return f"error:{str(error)}"

    if puerto_serial.isOpen():
        print_separador()
        print(f"CONECTADO A: {puerto_serial.portstr}")
        print_separador()
        try:
            puerto_serial.flushInput()

            numero_lineas = 0
            datos_recibidos = b''

            while numero_lineas <= 10:
                time.sleep(0.5)
                datos_recibidos = puerto_serial.readlines()
                print(f"LEYENDO BUFFER: {datos_recibidos}")

                numero_lineas += 1

                if datos_recibidos:
                    break

            puerto_serial.close()
            return str(datos_recibidos[:])

        except Exception as error:
            print(f"ERROR DE COMUNICACION: {error}")
            return f"error:{str(error)}"

    else:
        mensaje_error = "NO SE PUEDE ABRIR EL PUERTO SERIAL"
        print(mensaje_error)
        return f"error:{mensaje_error}"






""" ORIGINAL 26.01.2024
	ACORREA
"""
# #!/usr/bin/python
# import os
# import time

# import serial
# from core.views import printSeparador

# #initialization and open the port

# #possible timeout values:
# #    1. None: wait forever, block call
# #    2. 0: non-blocking mode, return immediately
# #    3. x, x is bigger than 0, float allowed, timeout block call
# def leerPuertoSerial(config):
# 	ser = serial.Serial()
# 			# port='COM1',\
# 			# baudrate=4800,\
# 			# parity=serial.PARITY_EVEN,\
# 			# stopbits=serial.STOPBITS_ONE,\
# 			# bytesize=serial.SEVENBITS,\
# 			# timeout=1
			
# 	#ser.port = "/dev/ttyUSB0"	
# 	ser.port = config.puerto
# 	#ser.port = "/dev/ttyS2"
# 	# ser.baudrate = config.baudios
# 	ser.baudrate = config.bits_por_segundo
# 	# ser.bytesize = serial.SEVENBITS #number of bits per bytes
# 	ser.bytesize = config.bits_de_datos
# 	# ser.parity = serial.PARITY_EVEN #set parity check: no parity
# 	ser.parity = config.paridad
# 	ser.stopbits = config.bits_de_parada #number of stop bits
# 	ser.timeout = 0          #block read
# 	#ser.timeout = 1            #non-block read
# 	#ser.timeout = 2              #timeout block read
# 	ser.xonxoff = False     #disable software flow control
# 	#ser.rtscts = False     #disable hardware (RTS/CTS) flow control
# 	#ser.dsrdtr = False       #disable hardware (DSR/DTR) flow control
# 	#ser.writeTimeout = 2     #timeout for write

# 	try:
# 		#BORRAMOS EL ARCHIVO DE PESO 
# 		# if os.path.exists("peso.txt"):
# 		# 	os.remove("peso.txt")
# 		# printSeparador()
# 		# print('ESTADO PUERTO {}'.format(ser.isOpen()))
	
# 		if not ser.isOpen():
# 			ser.open()
# 			printSeparador()
# 			print(ser)
		

# 	except Exception as e:
# 		print ("ERROR ABRIENDO PUERTO SERIAL: " + str(e))
# 		return f'error:{str(e)}'

# 	if ser.isOpen():
# 		printSeparador()
# 		print("CONECTADO A: " + ser.portstr)
# 		printSeparador()
# 		try:
# 			ser.flushInput() #flush input buffer, discarding all its contents
# 			# ser.flushOutput()#flush output buffer, aborting current output 
# 			#and discard all that is in buffer

# 			#write dato
# 			#ser.write("AT+CSQ".encode())
# 			#print("write dato: AT+CSQ")

# 			#time.sleep(0.5)  #give the serial port sometime to receive the data

# 			nro_lineas = 0
# 			data=b''	
# 			while True:						
# 				time.sleep(0.5)
# 				respuesta = ser.readlines()
# 				print("LEYENDO BUFFER: " + str(respuesta))

# 				nro_lineas = nro_lineas + 1

# 				if (nro_lineas > 10):
# 					break

# 				if respuesta:
# 					data = respuesta				
# 					# with open("peso.txt", "w") as archivo:
# 					# 	# archivo.writelines(dato.decode())
# 					# 	archivo.writelines(str(data))
# 						# print(archivo.tell())
# 						# print(type(archivo))
# 					break
	
# 			ser.close()
# 			return str(data[:])
# 		except Exception as e:
# 			print ("ERROR DE COMUNICACION...: " + str(e))
# 			return f'error:{str(e)}'
# 	else:
# 		e = "NO SE PUEDE ABRIR EL PUERTO SERIAL"
# 		print (e)
# 		return f'error:{str(e)}'
