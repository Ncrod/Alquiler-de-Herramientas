from datetime import datetime, timedelta

from config import ESTADOS_PRESTAMO, RUTA_PRESTAMOS, RUTA_USUARIOS, RUTA_HERRAMIENTAS, DIAS_PRESTAMO, ESTADOS_HERRAMIENTA
from modulos import almacenamiento
from modulos import utilidades
from modulos import logs

def registrar():
    prestamos = almacenamiento.cargar(RUTA_PRESTAMOS)
    herramientas = almacenamiento.cargar(RUTA_HERRAMIENTAS)
    usuarios = almacenamiento.cargar(RUTA_USUARIOS)

    if len(herramientas) == 0:
        print("\nNo hay herramientas registradas.")
        return

    if len(usuarios) == 0:
        print("\nNo hay usuarios registrados.")
        return

    print("\n--- NUEVO PRÉSTAMO ---")
    for u in usuarios:
        print(str(u["id"]) + ". " + u["nombres"] + " " + u["apellidos"])

    id_usuario = utilidades.pedir_entero("Seleccione el id del usuario: ", 1)
    usuario = utilidades.buscar_por_id(usuarios, id_usuario)

    if usuario is None:
        print("Usuario no encontrado.")
        logs.error("Usuario con id " + str(id_usuario) + " no encontrado al intentar crear un préstamo")
        return

    print("\n--- HERRAMIENTAS DISPONIBLES ---")
    for h in herramientas:
        print(str(h["id"]) + ". " + h["nombre"] +
              " | disponibles: " + str(h["cantidad"]) +
              " | " + h["estado"])

    id_herramienta = utilidades.pedir_entero("Id de la herramienta: ", 1)
    herramienta = utilidades.buscar_por_id(herramientas, id_herramienta)

    if herramienta is None:
        print("Herramienta no encontrada.")
        logs.error("Herramienta con id " + str(id_herramienta) + " no encontrada al intentar crear un préstamo")
        return

    if herramienta["estado"] != ESTADOS_HERRAMIENTA[0]: 
        print("La herramienta no está disponible para préstamo.")
        logs.error("Intento de préstamo de herramienta inactiva id " + str(id_herramienta))
        return

    cantidad = utilidades.pedir_entero("Cantidad a prestar: ", 1)

    if cantidad > herramienta["cantidad"]:
        print("No hay suficiente stock disponible.")
        logs.error("Stock insuficiente para préstamo de herramienta id " + str(id_herramienta) +
                   ": pidieron " + str(cantidad) + " y hay " + str(herramienta["cantidad"]))
        return

    observaciones = input("Observaciones (opcional): ").strip()

    hoy = datetime.now()
    fecha_inicio = hoy.strftime("%Y-%m-%d")
    fecha_estimada = (hoy + timedelta(days=DIAS_PRESTAMO)).strftime("%Y-%m-%d")

    prestamo = {
        "id": utilidades.generar_id(prestamos),
        "usuario_id": usuario["id"],
        "herramienta_id": herramienta["id"],
        "cantidad": cantidad,
        "fecha_inicio": fecha_inicio,
        "fecha_estimada": fecha_estimada,
        "fecha_devolucion": None,
        "estado": ESTADOS_PRESTAMO[0],
        "observaciones": observaciones,
    }

    herramienta["cantidad"] -= cantidad

    prestamos.append(prestamo)
    almacenamiento.guardar(RUTA_PRESTAMOS, prestamos)
    almacenamiento.guardar(RUTA_HERRAMIENTAS, herramientas)

    print("\nPréstamo #" + str(prestamo["id"]) + " registrado.")
    print("Fecha estimada de devolución: " + fecha_estimada)
    logs.info("Prestamo #" + str(prestamo["id"]) + ": " + str(cantidad) + " de '" +
              herramienta["nombre"] + "'", usuario=id_usuario)


def devolver():
    prestamos = almacenamiento.cargar(RUTA_PRESTAMOS)
    herramientas = almacenamiento.cargar(RUTA_HERRAMIENTAS)

    activos = []
    for p in prestamos:
        if p["estado"] == "Activo":
            activos.append(p)

    if len(activos) == 0:
        print("\nNo hay prestamos activos.")
        return

    print("\n--- PRESTAMOS ACTIVOS ---")
    for p in activos:
        mostrar_uno(p, herramientas)

    id_prestamo = utilidades.pedir_entero("\nId del prestamo a devolver: ", 1)
    prestamo = utilidades.buscar_por_id(prestamos, id_prestamo)

    if prestamo is None:
        print("No existe un prestamo con ese id.")
        logs.error("Devolucion fallida: prestamo inexistente id " + str(id_prestamo))
        return

    if prestamo["estado"] != ESTADOS_PRESTAMO[0]:
        print("Ese prestamo ya fue devuelto.")
        return

    
    herramienta = utilidades.buscar_por_id(herramientas, prestamo["herramienta_id"])

    if herramienta is not None:
        herramienta["cantidad"] = herramienta["cantidad"] + prestamo["cantidad"]
        almacenamiento.guardar(RUTA_HERRAMIENTAS, herramientas)
    else:
        logs.advertencia("Devolucion del prestamo #" + str(id_prestamo) +
                         ": la herramienta ya no existe")

    prestamo["estado"] = ESTADOS_PRESTAMO[1]
    prestamo["fecha_devolucion"] = datetime.now().strftime("%Y-%m-%d")

    almacenamiento.guardar(RUTA_PRESTAMOS, prestamos)

    print("Prestamo #" + str(id_prestamo) + " devuelto.")
    logs.info("Prestamo #" + str(id_prestamo) + " devuelto",
              usuario=prestamo["usuario_id"])


def esta_vencido(prestamo):
    if prestamo["estado"] != ESTADOS_PRESTAMO[0]:
        return False
    
    hoy = datetime.now().strftime("%Y-%m-%d")

    return prestamo["fecha_estimada"] < hoy


def mostrar_uno(p, herramientas):
    herramienta = utilidades.buscar_por_id(herramientas, p["herramienta_id"])

    if herramienta is None:
        nombre = "(herramienta eliminada)"
    else:
        nombre = herramienta["nombre"]

    linea = ("#" + str(p["id"]) +
             " | usuario: " + str(p["usuario_id"]) +
             " | " + nombre +
             " x" + str(p["cantidad"]) +
             " | desde " + p["fecha_inicio"] +
             " | vence " + p["fecha_estimada"] +
             " | " + p["estado"])

    if esta_vencido(p):
        linea = linea + "  *** VENCIDO ***"

    print(linea)


def listar():
    prestamos = almacenamiento.cargar(RUTA_PRESTAMOS)
    herramientas = almacenamiento.cargar(RUTA_HERRAMIENTAS)

    if len(prestamos) == 0:
        print("\nNo hay prestamos registrados.")
        return

    print("\n--- PRESTAMOS ---")
    for p in prestamos:
        mostrar_uno(p, herramientas)