
import sqlite3
from datetime import datetime
from pathlib import Path

RUTA_DB = Path(__file__).resolve().parent / "dron_geox.db"

# Crear la base de datos
def iniciar_bd():
    conexion = sqlite3.connect(RUTA_DB)

    conexion.execute("""
        CREATE TABLE IF NOT EXISTS lecturas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            operador TEXT,
            fecha_hora TEXT,
            numero_lectura INTEGER,
            altitud REAL,
            temperatura REAL,
            bateria REAL,
            estado TEXT
        )
    """)

    conexion.commit()
    return conexion


# Guardar las lecturas
def guardar_lectura(conexion, operador, numero,
                    altitud, temperatura, bateria, estado):

    fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    conexion.execute("""
        INSERT INTO lecturas (
            operador, fecha_hora, numero_lectura,
            altitud, temperatura, bateria, estado
        )
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (
        operador, fecha, numero,
        altitud, temperatura, bateria, estado
    ))

    conexion.commit()
    print("Lectura guardada correctamente")

#consultar las lecturas guardadas 
def consultar_lecturas(conexion):
    cursor = conexion.execute("SELECT * FROM lecturas")
    return cursor.fetchall()

#buscar lecturas por operador
def buscar_por_operador(conexion, operador):
    cursor = conexion.execute(
    "SELECT * FROM lecturas WHERE operador =?",
    (operador,)
    )
    return cursor.fetchall()
