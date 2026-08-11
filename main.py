from modulos import almacenamiento
from modulos import utilidades
from modulos import logs
from modulos import herramientas
from modulos import usuarios
from modulos import prestamos
from modulos import reportes
from modulos import permisos
from config import RUTA_USUARIOS
import os
import sys

os.system("")  # Activa los colores ANSI en la consola de Windows

# Evita UnicodeEncodeError con los iconos en consolas de Windows
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

RESET = "\033[0m"
NEGRITA = "\033[1m"
ROJO = "\033[31m"
VERDE = "\033[32m"
AMARILLO = "\033[33m"
AZUL = "\033[34m"
MAGENTA = "\033[35m"
CYAN = "\033[36m"


def titulo(texto, color=CYAN):
    linea = "=" * 40
    print("\n" + color + linea + RESET)
    print(color + NEGRITA + "  " + texto + RESET)
    print(color + linea + RESET)


def opcion_menu(numero, texto, color=VERDE):
    print(color + " " + str(numero) + ". " + RESET + texto)


def volver(texto="Volver"):
    print(ROJO + " 0. " + RESET + texto)


def crear_admin_inicial():
    lista = almacenamiento.cargar(RUTA_USUARIOS)

    if len(lista) > 0:
        return

    print("\nNo hay usuarios en el sistema.")
    print("Se creara el primer administrador.\n")

    admin = {
        "id": 1,
        "nombres": utilidades.pedir_texto("Nombres: "),
        "apellidos": utilidades.pedir_texto("Apellidos: "),
        "telefono": utilidades.pedir_texto("Telefono: "),
        "direccion": utilidades.pedir_texto("Direccion: "),
        "tipo": "Administrador"
    }

    lista.append(admin)
    almacenamiento.guardar(RUTA_USUARIOS, lista)

    print("\nAdministrador creado con id 1.")
    logs.info("Administrador inicial creado")


def menu_herramientas(usuario):
    while True:
        titulo("\U0001F527 HERRAMIENTAS", AMARILLO)
        opcion_menu(1, "Crear")
        opcion_menu(2, "Listar")
        opcion_menu(3, "Buscar")
        opcion_menu(4, "Actualizar")
        opcion_menu(5, "Eliminar / Inactivar")
        volver()

        opcion = utilidades.pedir_entero(CYAN + "\nOpcion: " + RESET, 0)

        if opcion == 1:
            herramientas.crear()
        elif opcion == 2:
            herramientas.listar()
        elif opcion == 3:
            herramientas.buscar()
        elif opcion == 4:
            herramientas.actualizar()
        elif opcion == 5:
            herramientas.eliminar()
        elif opcion == 0:
            return
        else:
            print(ROJO + "Opcion invalida." + RESET)

        utilidades.pausar()


def menu_crud_usuarios(usuario):
    while True:
        titulo("\U0001F464 USUARIOS", MAGENTA)
        opcion_menu(1, "Crear")
        opcion_menu(2, "Listar")
        opcion_menu(3, "Buscar")
        opcion_menu(4, "Actualizar")
        opcion_menu(5, "Eliminar")
        volver()

        opcion = utilidades.pedir_entero(CYAN + "\nOpcion: " + RESET, 0)

        if opcion == 1:
            usuarios.crear()
        elif opcion == 2:
            usuarios.listar()
        elif opcion == 3:
            usuarios.buscar()
        elif opcion == 4:
            usuarios.actualizar()
        elif opcion == 5:
            usuarios.eliminar()
        elif opcion == 0:
            return
        else:
            print(ROJO + "Opcion invalida." + RESET)

        utilidades.pausar()


def menu_prestamos(usuario):
    while True:
        titulo("\U0001F4CB PRESTAMOS", AZUL)
        opcion_menu(1, "Registrar prestamo")
        opcion_menu(2, "Registrar devolucion")
        opcion_menu(3, "Listar todos")
        opcion_menu(4, "Solicitudes pendientes")
        volver()

        opcion = utilidades.pedir_entero(CYAN + "\nOpcion: " + RESET, 0)

        if opcion == 1:
            prestamos.registrar()
        elif opcion == 2:
            prestamos.devolver()
        elif opcion == 3:
            prestamos.listar()
        elif opcion == 4:
            permisos.aprobar_solicitud(usuario)
        elif opcion == 0:
            return
        else:
            print(ROJO + "Opcion invalida." + RESET)

        utilidades.pausar()


def menu_reportes(usuario):
    while True:
        titulo("\U0001F4CA REPORTES", VERDE)
        opcion_menu(1, "Herramientas con stock bajo")
        opcion_menu(2, "Prestamos activos y vencidos")
        opcion_menu(3, "Historial de un usuario")
        opcion_menu(4, "Herramientas mas solicitadas")
        opcion_menu(5, "Usuarios mas activos")
        volver()

        opcion = utilidades.pedir_entero(CYAN + "\nOpcion: " + RESET, 0)

        if opcion == 1:
            reportes.stock_bajo()
        elif opcion == 2:
            reportes.prestamos_activos_y_vencidos()
        elif opcion == 3:
            reportes.historial_usuario()
        elif opcion == 4:
            reportes.mas_solicitadas()
        elif opcion == 5:
            reportes.usuarios_mas_activos()
        elif opcion == 0:
            return
        else:
            print(ROJO + "Opcion invalida." + RESET)

        utilidades.pausar()


def menu_admin(usuario):
    while True:
        titulo("\U0001F6E0 MENU ADMINISTRADOR - " + usuario["nombres"], CYAN)
        opcion_menu(1, "Herramientas")
        opcion_menu(2, "Usuarios")
        opcion_menu(3, "Prestamos")
        opcion_menu(4, "Reportes")
        volver("Cerrar sesion")

        opcion = utilidades.pedir_entero(CYAN + "\nOpcion: " + RESET, 0)

        if opcion == 1:
            menu_herramientas(usuario)
        elif opcion == 2:
            menu_crud_usuarios(usuario)
        elif opcion == 3:
            menu_prestamos(usuario)
        elif opcion == 4:
            menu_reportes(usuario)
        elif opcion == 0:
            logs.info("Cierre de sesion", usuario=usuario["id"])
            return
        else:
            print(ROJO + "Opcion invalida." + RESET)
            utilidades.pausar()


def menu_usuarios(usuario):
    while True:
        titulo("\U0001F464 MENU USUARIO - " + usuario["nombres"], MAGENTA)
        opcion_menu(1, "Ver herramientas disponibles")
        opcion_menu(2, "Buscar herramienta")
        opcion_menu(3, "Solicitar una herramienta")
        opcion_menu(4, "Ver mis solicitudes")
        opcion_menu(5, "Ver mi historial de prestamos")
        volver("Cerrar sesion")

        opcion = utilidades.pedir_entero(CYAN + "\nOpcion: " + RESET, 0)

        if opcion == 1:
            herramientas.listar()
        elif opcion == 2:
            herramientas.buscar()
        elif opcion == 3:
            permisos.crear_solicitud(usuario)
        elif opcion == 4:
            permisos.ver_solicitudes(usuario)
        elif opcion == 5:
            mostrar_mi_historial(usuario)
        elif opcion == 0:
            logs.info("Cierre de sesion", usuario=usuario["id"])
            return
        else:
            print(ROJO + "Opcion invalida." + RESET)

        utilidades.pausar()


def mostrar_mi_historial(usuario):
    from config import RUTA_PRESTAMOS, RUTA_HERRAMIENTAS

    lista = almacenamiento.cargar(RUTA_PRESTAMOS)
    lista_h = almacenamiento.cargar(RUTA_HERRAMIENTAS)

    mios = []
    for p in lista:
        if p["usuario_id"] == usuario["id"]:
            mios.append(p)

    print("\n--- MIS PRESTAMOS ---")

    if len(mios) == 0:
        print("No tiene prestamos registrados.")
        return

    for p in mios:
        prestamos.mostrar_uno(p, lista_h)


def main():
    titulo("\U0001F527 PRESTAMO DE HERRAMIENTAS", CYAN)

    logs.info("Programa iniciado")
    crear_admin_inicial()

    while True:
        usuario = permisos.iniciar_sesion()

        if usuario is None:
            if utilidades.confirmar("\nDesea salir del programa?"):
                print("\nHasta pronto.")
                logs.info("Programa finalizado")
                return
            continue

        if permisos.es_admin(usuario):
            menu_admin(usuario)
        else:
            menu_usuarios(usuario)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nPrograma interrumpido por el usuario.")
        logs.info("Programa interrumpido con Ctrl+C")
    except Exception as e:
        print("\nOcurrio un error inesperado: " + str(e))
        logs.error("Error inesperado: " + str(e))
