# ///////////////////////////////////////////
# VALIDACION DE COSECHAS DE PAPA
# comprovacion de los datos en los modulos 
# ///////////////////////////////////////////

import math
import re

LIMITE_REVISION_KG = 1000.0


def es_dato_numerico(valor):
    # Comprobar que el dato ingresado sea numerico.
    # Se aceptan 1500, 1,500 y 120.5 o 120,5.
    texto = str(valor).strip()
    if texto == "":
        return False, None

    if "," in texto:
        # Coma como separador de miles, por ejemplo 1,500 o 12,500.50.
        if re.fullmatch(r"[+-]?\d{1,3}(,\d{3})+(\.\d+)?", texto):
            texto = texto.replace(",", "")
        # Coma decimal, por ejemplo 85,5 o 120,25.
        elif re.fullmatch(r"[+-]?\d+,\d{1,2}", texto):
            texto = texto.replace(",", ".")
        else:
            return False, None

    try:
        numero = float(texto)
        if not math.isfinite(numero):
            return False, None
        return True, numero
    except (ValueError, OverflowError):
        return False, None


def es_mayor_que_cero(cantidad):
    # Verificar que sea mayor que cero.
    return cantidad > 0


def requiere_revision(cantidad):
    # Si supera 1000 kg, necesita supervision humana.
    return cantidad > LIMITE_REVISION_KG


def validar_cosecha(dato):
    # Devolver el estado del registro y sus kilogramos.
    if str(dato).strip() == "":
        return "INCOMPLETO", 0

    es_numerico, kg = es_dato_numerico(dato)
    if not es_numerico:
        return "INVALIDO", 0

    if not es_mayor_que_cero(kg):
        return "INVALIDO", 0

    if requiere_revision(kg):
        # No borrar ni sumar: conservar para la revision humana.
        return "REVISAR", kg

    return "VALIDO", kg
