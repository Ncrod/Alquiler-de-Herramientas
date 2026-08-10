import json

import os

def cargar(ruta):
    try:
        with open(ruta, "r", encoding="utf-8") as archivo:
            datos = json.load(archivo)

            if not isinstance(datos, list):
                return []
            return datos
    except FileNotFoundError:
        return []
    except json.JSONDecodeError:
        return []



def guardar(ruta, datos):
    try:
        carpeta = os.path.dirname(ruta)
        if not os.path.exists(carpeta):
            os.makedirs(carpeta)
        with open(ruta, "w", encoding="utf-8") as archivo:
            json.dump(datos, archivo, indent=4, ensure_ascii=False)
        return True
    except (OSError, TypeError) as e:
        print(f"Error al guardar el archivo: {e}")
        return False