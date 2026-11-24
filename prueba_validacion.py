# ///////////////////////////////////////
# PRUEBA DEL SISTEMA DE VALIDACIONES
# ///////////////////////////////////////

# Funciona desde main.py y tambien si se ejecuta este archivo por separado.
try:
    from validaciones.validar_cosechas import validar_cosecha
except ModuleNotFoundError:
    from validar_cosechas import validar_cosecha


def main():
    total = 0
    print("===================================")
    print("    VALIDADOR DE COSECHAS DE PAPA")
    print("===================================")
    print("Esta es una PRUEBA: no guarda registros en SQLite.")

    for i in range(1, 7):
        print("\n--- COSECHA NUMERO", i, "---")
        dato = input("Ingresa los kg cosechados: ")
        estado, kg = validar_cosecha(dato)

        if estado == "VALIDO":
            print("VALIDO: Registro correcto.")
            total = total + kg
        elif estado == "REVISAR":
            print("REVISAR: Supera los 1000 kg; necesita supervision humana.")
        elif estado == "INCOMPLETO":
            print("INCOMPLETO: Falta ingresar datos.")
        else:
            print("INVALIDO: Corrija la cantidad.")

    print("\n====================================")
    print("           REPORTE FINAL")
    print("====================================")
    print("Total de cosecha valida:", total, "kg")
    print("====================================")


if __name__ == "__main__":
    main()
