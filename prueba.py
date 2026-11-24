from database import iniciar_bd, guardar_lectura, consultar_lecturas, buscar_por_operador

# la conexion con SQLite
conexion = iniciar_bd()

# Guarda una lectura de prueba
guardar_lectura(
    conexion,
    "OP001",
    1,
    1200,
    25,
    80,
    "NORMAL"
)

# Muestra los datos guardados
registros = consultar_lecturas(conexion)

for registro in registros:
    print(registro)

#busca las lecturas del operador OP001
print("Lecturas del operador OP001:")

resultados = buscar_por_operador(conexion, "OP001")

for registro in resultados:
    print(registro)
    
conexion.close()