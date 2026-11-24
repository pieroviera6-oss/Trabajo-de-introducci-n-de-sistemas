# ///////////////////////////////////////////
# SISTEMA DE COSECHAS - REGISTRO Y SUPERVISION HUMANA
# ///////////////////////////////////////////

from datetime import datetime
from validaciones.validar_cosechas import (
    validar_cosecha, es_dato_numerico, LIMITE_REVISION_KG
)
from database_cosechas import (
    iniciar_bd, guardar_cosecha, consultar_pendientes,
    actualizar_revision
)

def registrar_cosecha(agricultor, hora, conexion):
    # El nombre del agricultor se recibe de la funcion main().
    print("\n--- REGISTRO DE COSECHA ---")
    entrada_kg = input("Ingrese los kilogramos de papa: ").strip()

    estado, kg = validar_cosecha(entrada_kg)

    if estado == "INCOMPLETO":
        print("INCOMPLETO: No ingresaste una cantidad. Necesita correccion.")
        kg_guardar = None

    elif estado == "INVALIDO":
        es_numerico, numero = es_dato_numerico(entrada_kg)
        if not es_numerico:
            print("INVALIDO: Ingresa una cantidad numerica valida.")
        else:
            print("INVALIDO: La cantidad debe ser mayor que cero.")
        print("Este registro necesita correccion.")
        kg_guardar = None

    elif estado == "REVISAR":
        print("REVISAR: Cantidad superior al limite de", LIMITE_REVISION_KG, "kg.")
        print("Queda pendiente de supervision humana; no se suma todavia.")
        kg_guardar = kg

    else:
        print("VALIDO: Cosecha registrada correctamente.")
        print("Agricultor:", agricultor)
        print("Fecha y hora:", hora)
        print("Papa cosechada:", kg, "kg")
        kg_guardar = kg

    numero = guardar_cosecha(conexion, agricultor, entrada_kg, kg_guardar, estado)
    print("Registro guardado en SQLite con ID:", numero)
    return estado, kg if estado == "VALIDO" else 0, entrada_kg


def main():
    print("===============================================")
    print("       REGISTRO DE COSECHAS DE PAPA            ")
    print("             CAJAMARCA - PERU                  ")
    print("===============================================")

    total = 0
    registros = []
    conexion = iniciar_bd()

    try:
        while True:
            agricultor = ""
            while agricultor == "":
                agricultor = input(
                    "\nNombre del agricultor (FIN para terminar): "
                ).strip()
                if agricultor == "":
                    print("ERROR: Este campo es obligatorio.")

            if agricultor.upper() == "FIN":
                break

            hora_actual = datetime.now()
            hora = hora_actual.strftime("(%H:%M) del (%d/%m/%Y)")

            print("==============================================")
            print("Agricultor registrado:", agricultor)
            print("Fecha y hora:", hora)
            print("==============================================")

            estado, kg_validos, entrada = registrar_cosecha(agricultor, hora, conexion)
            if estado == "VALIDO":
                total = total + kg_validos

            registros.append((agricultor, entrada, estado))

        print("\n==============================================")
        print("                REPORTE FINAL")
        print("==============================================")

        if len(registros) == 0:
            print("No se registraron cosechas.")

        for nombre, dato, estado in registros:
            cantidad_mostrada = dato + " kg" if dato else "Sin dato"
            print(nombre, "|", cantidad_mostrada, "|", estado)

        print("----------------------------------------------")
        print("TOTAL DE KG VALIDOS (ESTA SESION):", total, "kg")
        print("Los registros en REVISAR se conservan para supervision humana.")
        print("Todos los registros se guardan en backend/cosechas.db")
        print("==============================================")

    finally:
        conexion.close()


def revisar_pendientes():
    
    conexion = iniciar_bd()
    try:
        pendientes = consultar_pendientes(conexion)
        print("\n--- REGISTROS PENDIENTES DE REVISION ---")

        if len(pendientes) == 0:
            print("No hay registros pendientes.")
            return

        for numero, agricultor, entrada, kg in pendientes:
            print("ID:", numero, "|", agricultor, "|", entrada, "kg")

        opcion = input("\nID a revisar (0 para volver): ").strip()
        if opcion == "0":
            return
        if not opcion.isdigit():
            print("ERROR: Ingresa un ID numerico.")
            return

        numero = int(opcion)
        registro = None
        for fila in pendientes:
            if fila[0] == numero:
                registro = fila

        if registro is None:
            print("ERROR: Ese ID no esta pendiente de revision.")
            return

        print("\n1. Confirmar que la cantidad es correcta")
        print("2. Corregir la cantidad")
        print("3. Dejar pendiente de revision")
        decision = input("Selecciona una opcion: ").strip()

        if decision == "3":
            print("El registro permanece pendiente, sin eliminarse.")
            return

        if decision != "1" and decision != "2":
            print("Opcion no valida. El registro sigue pendiente.")
            return

     
        revisor = ""
        while revisor == "":
            revisor = input("Nombre del responsable de la revision: ").strip()
            if revisor == "":
                print("ERROR: Debes indicar un responsable.")

        if decision == "1":
            
            actualizar_revision(
                conexion, numero, registro[2], registro[3],
                "VALIDO REVISADO", revisor
            )
            print("Registro confirmado por:", revisor)
            print("Ahora se incluye en el total de kilogramos validos.")

        else:
            nueva_entrada = input("Ingresa los kg corregidos: ").strip()
            nuevo_estado, nuevos_kg = validar_cosecha(nueva_entrada)

            if nuevo_estado == "VALIDO":
                actualizar_revision(
                    conexion, numero, nueva_entrada, nuevos_kg,
                    "VALIDO REVISADO", revisor
                )
                print("Cantidad corregida y validada:", nuevos_kg, "kg")

            elif nuevo_estado == "REVISAR":
                
                actualizar_revision(
                    conexion, numero, nueva_entrada, nuevos_kg,
                    "REVISAR", revisor
                )
                print("Sigue superando el limite; permanece pendiente.")

            else:
                print("La correccion no es valida. No se modifico el registro.")

    finally:
        conexion.close()


if __name__ == "__main__":
    main()
