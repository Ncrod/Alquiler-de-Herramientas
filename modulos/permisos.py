from datetime import datetime

from config import RUTA_USUARIOS, RUTA_SOLICITUDES, RUTA_HERRAMIENTAS
from modulos import almacenamiento
from modulos import utilidades
from modulos import logs


def iniciar_sesion():
    usuarios = almacenamiento.cargar(RUTA_USUARIOS)

    if len(usuarios) == 0:
        print("\nNo hay usuarios registrados en el sistema.")
        return None

    print("\n--- INICIAR SESION ---")
    for u in usuarios:
        print(str(u["id"]) + ". " + u["nombres"] + " " + u["apellidos"] + " (" + u["tipo"] + ")")

    id_usuario = utilidades.pedir_entero("\nIngrese su id (0 para salir): ", 0)

    if id_usuario == 0:
        return None

    usuario = utilidades.buscar_por_id(usuarios, id_usuario)

    if usuario is None:
        print("No existe un usuario con ese id.")
        logs.error("Intento de inicio de sesion con id inexistente " + str(id_usuario))
        return None

    print("\U0001F44B \nBienvenido, " + usuario["nombres"] + " (" + usuario["tipo"] + ").")
    logs.info("Inicio de sesion", usuario=id_usuario)
    return usuario


def es_admin(usuario):
    if usuario is None:
        return False
    return usuario["tipo"] == "Administrador"


def requiere_admin(usuario):
    if es_admin(usuario):
        return True

    print("\U0001F512 \nNo tiene permisos para realizar esta accion.")
    print("Solo el administrador puede hacerlo.")
    logs.advertencia("Intento de acceso sin permisos", usuario=usuario["id"])
    return False


def crear_solicitud(usuario):
    solicitudes = almacenamiento.cargar(RUTA_SOLICITUDES)
    herramientas = almacenamiento.cargar(RUTA_HERRAMIENTAS)

    if len(herramientas) == 0:
        print("\nNo hay herramientas registradas.")
        return

    print("\n--- SOLICITAR HERRAMIENTA ---")
    for h in herramientas:
        print(str(h["id"]) + ". " + h["nombre"] +
              " | disponibles: " + str(h["cantidad"]) +
              " | " + h["estado"])

    id_herramienta = utilidades.pedir_entero("\nId de la herramienta: ", 1)
    herramienta = utilidades.buscar_por_id(herramientas, id_herramienta)

    if herramienta is None:
        print("No existe una herramienta con ese id.")
        return

    if herramienta["estado"] != "Activa":
        print("Esa herramienta no esta disponible (" + herramienta["estado"] + ").")
        return

    cantidad = utilidades.pedir_entero("Cantidad: ", 1)

    if cantidad > herramienta["cantidad"]:
        print("No hay suficiente stock disponible. Disponibles: " +
              str(herramienta["cantidad"]) + ".")
        logs.advertencia("Solicitud rechazada por stock insuficiente de '" +
                         herramienta["nombre"] + "': pidieron " + str(cantidad) +
                         " y hay " + str(herramienta["cantidad"]),
                         usuario=usuario["id"])
        return

    solicitud = {
        "id": utilidades.generar_id(solicitudes),
        "usuario_id": usuario["id"],
        "herramienta_id": id_herramienta,
        "cantidad": cantidad,
        "fecha": datetime.now().strftime("%Y-%m-%d"),
        "estado": "Pendiente"
    }

    solicitudes.append(solicitud)
    almacenamiento.guardar(RUTA_SOLICITUDES, solicitudes)

    print("\U0001F4E8 \nSolicitud #" + str(solicitud["id"]) + " enviada.")
    print("Espere la aprobacion del administrador.")
    logs.info("Solicitud #" + str(solicitud["id"]) + " de '" + herramienta["nombre"] + "'",
              usuario=usuario["id"])


def ver_solicitudes(usuario):
    solicitudes = almacenamiento.cargar(RUTA_SOLICITUDES)
    herramientas = almacenamiento.cargar(RUTA_HERRAMIENTAS)

    if es_admin(usuario):
        propias = solicitudes
        print("\n--- TODAS LAS SOLICITUDES ---")
    else:
        propias = []
        for s in solicitudes:
            if s["usuario_id"] == usuario["id"]:
                propias.append(s)
        print("\n--- MIS SOLICITUDES ---")

    if len(propias) == 0:
        print("No hay solicitudes.")
        return

    for s in propias:
        herramienta = utilidades.buscar_por_id(herramientas, s["herramienta_id"])
        if herramienta is None:
            nombre = "(eliminada)"
        else:
            nombre = herramienta["nombre"]

        print("#" + str(s["id"]) +
              " | usuario: " + str(s["usuario_id"]) +
              " | " + nombre +
              " x" + str(s["cantidad"]) +
              " | " + s["fecha"] +
              " | " + s["estado"])


def aprobar_solicitud(usuario):
    if not requiere_admin(usuario):
        return

    solicitudes = almacenamiento.cargar(RUTA_SOLICITUDES)
    herramientas = almacenamiento.cargar(RUTA_HERRAMIENTAS)

    pendientes = []
    for s in solicitudes:
        if s["estado"] == "Pendiente":
            pendientes.append(s)

    if len(pendientes) == 0:
        print("\nNo hay solicitudes pendientes.")
        return

    print("\n--- SOLICITUDES PENDIENTES ---")
    for s in pendientes:
        herramienta = utilidades.buscar_por_id(herramientas, s["herramienta_id"])
        if herramienta is None:
            nombre = "(eliminada)"
        else:
            nombre = herramienta["nombre"]

        print("#" + str(s["id"]) +
              " | usuario: " + str(s["usuario_id"]) +
              " | " + nombre +
              " x" + str(s["cantidad"]) +
              " | " + s["fecha"])

    id_solicitud = utilidades.pedir_entero("\nId de la solicitud: ", 1)
    solicitud = utilidades.buscar_por_id(solicitudes, id_solicitud)

    if solicitud is None:
        print("No existe una solicitud con ese id.")
        return

    if solicitud["estado"] != "Pendiente":
        print("Esa solicitud ya fue " + solicitud["estado"].lower() + ".")
        return

    print("\n1. Aprobar")
    print("2. Rechazar")
    opcion = utilidades.pedir_entero("Opcion: ", 1)

    if opcion == 1:
        solicitud["estado"] = "Aprobada"
        print("\U00002705 Solicitud aprobada. Ahora registre el prestamo desde el menu.")
        logs.info("Solicitud #" + str(id_solicitud) + " aprobada", usuario=usuario["id"])

    elif opcion == 2:
        solicitud["estado"] = "Rechazada"
        print("\U0000274C Solicitud rechazada.")
        logs.info("Solicitud #" + str(id_solicitud) + " rechazada", usuario=usuario["id"])

    else:
        print("Opcion invalida.")
        return

    almacenamiento.guardar(RUTA_SOLICITUDES, solicitudes)

 
