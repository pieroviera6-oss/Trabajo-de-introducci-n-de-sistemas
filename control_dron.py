#supervicion humana
print("============================================")

from datetime import date, datetime 
from database import iniciar_bd, guardar_lectura

operador= ""
while operador == "":
    operador = input("Ingreas tu codigo de operador: ")
    if operador == "":
        print("Error este campo es obligatorio para la auditoria")


hora_actual = datetime.now()
hora=hora_actual.strftime("(%H:%M) del (%d/%m/%y)")
print("Sesion iniciada por: ",operador,"a las",hora,)
print("============================================")

#DRON_GEOX
conexion = iniciar_bd()
for i in range (1,4):
    print()
    print("----Resvisando lectura #", i,"----")
    alt=float(input("Ingresa la altutud: "))
    tmp=float(input("Ingresa la temperatura: "))
    bateria=float(input("Ingresa la bateria: "))
    if bateria <0 or bateria>100 or alt<500 or alt>5000 or tmp< -15 or tmp>35:
        print("============================================")
        print("DESCARTADO: dato fuera del rango.")
        print("============================================")
    elif bateria>5 and bateria<=25:
        estado = "-Bateria baja"
        print("Bateria baja")
    
    elif bateria<=5:
        estado = "Bateria critico"
        print("Bateria en estado critico")
    
    elif tmp<=0:
        estado = "Riesgo helado"
        print("Riesgo de helada")

    elif alt<=600:
        estado = "Vuela muy bajo"
        print("Vuelo muy bajo")

    else:
        estado = "Normal"
        print("lectura normal")

