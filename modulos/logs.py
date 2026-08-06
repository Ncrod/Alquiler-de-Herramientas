# Registro de eventos y errores

import os
from datetime import datetime
from config import RUTA_LOGS

def registrar(tipo, mensaje, usuario=None):
    try:
        carpeta = os.path.dirname(RUTA_LOGS)
        if not os.path.exists(carpeta):
            os.makedirs(carpeta)
        fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        linea = f"{fecha} - {tipo.upper()} - {mensaje}"
        if usuario is not None:
            linea = linea + " - Usuario: " + str(usuario)
        linea = linea + "\n"

        archivo = open(RUTA_LOGS, "a", encoding="utf-8")
        archivo.write(linea)
        archivo.close()
    except OSError as e:
        print(f"Error al registrar el log: {e}")


def info(mensaje, usuario=None):
    registrar("INFO", mensaje, usuario)

def advertencia(mensaje, usuario=None):
    registrar("ADVERTENCIA", mensaje, usuario)

def error(mensaje, usuario=None):
    registrar("ERROR", mensaje, usuario)

def leer_log(ultimas=20):
    try:
        archivo = open(RUTA_LOGS, "r", encoding="utf-8")
        lineas = archivo.readlines()
        archivo.close()
        return lineas[-ultimas:]
    except FileNotFoundError:
        return []