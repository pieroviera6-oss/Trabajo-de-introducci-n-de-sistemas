# ///////////////////////////////////////////
# BASE DE DATOS DEL SISTEMA AGRICOLA - SQLITE
# Se guarda por separado de la base de datos del dron.
# ///////////////////////////////////////////

import sqlite3
from datetime import datetime
from pathlib import Path

RUTA_DB = Path(__file__).resolve().parent / "cosechas.db"


def iniciar_bd():
    conexion = sqlite3.connect(RUTA_DB)
    conexion.execute("""
        CREATE TABLE IF NOT EXISTS cosechas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            agricultor TEXT NOT NULL,
            fecha_hora TEXT NOT NULL,
            entrada_original TEXT,
            entrada_final TEXT,
            kilogramos REAL,
            estado TEXT NOT NULL,
            revisor TEXT
        )
    """)
    conexion.commit()
    return conexion


def guardar_cosecha(conexion, agricultor, entrada, kg, estado):
    fecha = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    cursor = conexion.execute("""
        INSERT INTO cosechas (
            agricultor, fecha_hora, entrada_original,
            entrada_final, kilogramos, estado, revisor
        ) VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (
        agricultor, fecha, entrada, entrada, kg, estado, ""
    ))
    conexion.commit()
    return cursor.lastrowid


def consultar_cosechas(conexion):
    cursor = conexion.execute("""
        SELECT id, agricultor, entrada_final, kilogramos,
               estado, fecha_hora, revisor
        FROM cosechas ORDER BY id
    """)
    return cursor.fetchall()


def consultar_pendientes(conexion):
    cursor = conexion.execute("""
        SELECT id, agricultor, entrada_final, kilogramos
        FROM cosechas WHERE estado = 'REVISAR' ORDER BY id
    """)
    return cursor.fetchall()


def actualizar_revision(conexion, numero, entrada, kg, estado, revisor):
    conexion.execute("""
        UPDATE cosechas
        SET entrada_final = ?, kilogramos = ?, estado = ?, revisor = ?
        WHERE id = ? AND estado = 'REVISAR'
    """, (entrada, kg, estado, revisor, numero))
    conexion.commit()


def total_validos(conexion):
    cursor = conexion.execute("""
        SELECT COALESCE(SUM(kilogramos), 0)
        FROM cosechas WHERE estado IN ('VALIDO', 'VALIDO REVISADO')
    """)
    return cursor.fetchone()[0]
