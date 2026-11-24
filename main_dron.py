import serial 
import json
import math
from database import datetime
from database import iniciar_bd, guardar_lectura


Puerto = "COM3" # cambiar 
velocidad = 115200

#Superversion_humana

print("========================================")

operador = ""
while operador == "":
    operador = input("Ingresa tu codigo de operador:").strip()
    if operador == "":
        print ("Error: campo obligatorio para auditoria")

hora = datetime.now().strftime("(%H:%M) del (%d/%m/%y)")
print("Sesion iniciada por:", operador, "a las", hora)

#inicar sSQLite 

conexion = iniciar_bd()

numero_lectura = 0
try:
    #conectarse al ESP por USB
    with serial.Serial(Puerto, velocidad, timeout=1) as esp:
        print("Esperando lecturas del ESP...")
        while True:
            linea = esp.readline()
            if not linea:
                continue

            datos = json.loads(linea.decode("utf-8").strip())
            numero_lectura += 1
            print("Lectura", numero_lectura, ":", datos)
except serial.SerialException as error:
    print("Error al conectar con el ESP:", error)
except json.JSONDecodeError:
    print("Error: el ESP envio datos que no son JSON valido")
except KeyboardInterrupt:
    print("Lectura detenida por el operador")
finally:
    if conexion:
        conexion.close()
        