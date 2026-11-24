# /////////////////////////////////////////
# SISTEMA AGRICOLA - MENU PRINCIPAL
# Ejecuta el proyecto completo desde un solo archivo.
# /////////////////////////////////////////

from control_cosechas import main as registrar_agricultores
from control_cosechas import revisar_pendientes
from validaciones.prueba_validacion import main as probar_validaciones
from database_cosechas import iniciar_bd, consultar_cosechas, total_validos


def ver_registros_guardados():
    conexion = iniciar_bd()
    try:
        registros = consultar_cosechas(conexion)
        print("\n--- REGISTROS GUARDADOS EN SQLITE ---")
        if len(registros) == 0:
            print("No hay registros guardados.")
            return

        for numero, agricultor, dato, kg, estado, fecha, revisor in registros:
            cantidad = dato + " kg" if dato else "Sin dato"
            print("ID:", numero, "|", agricultor, "|", cantidad, "|", estado)
            if revisor:
                print("   Responsable de revision:", revisor)

        print("--------------------------------------------")
        print("TOTAL DE KG VALIDOS GUARDADOS:", total_validos(conexion), "kg")
    finally:
        conexion.close()


def main():
    while True:
        print("\n============================================")
        print("        SISTEMA DE COSECHAS DE PAPA")
        print("              CAJAMARCA - PERU")
        print("============================================")
        print("1. Registrar agricultores y cosechas")
        print("2. Probar las validaciones (6 cosechas)")
        print("3. Ver registros guardados en SQLite")
        print("4. Revision humana de cosechas pendientes")
        print("5. Salir del programa")

        opcion = input("Elige una opcion: ").strip()

        if opcion == "1":
            registrar_agricultores()
        elif opcion == "2":
            probar_validaciones()
        elif opcion == "3":
            ver_registros_guardados()
        elif opcion == "4":
            revisar_pendientes()
        elif opcion == "5":
            print("Gracias por utilizar el sistema.")
            break
        else:
            print("ERROR: Escoge una opcion del 1 al 5.")


if __name__ == "__main__":
    main()
