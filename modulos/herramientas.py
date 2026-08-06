# CRUD de herramientas

from config import RUTA_HERRAMIENTAS, CATEGORIAS, ESTADOS_HERRAMIENTA
from modulos import almacenamiento
from modulos import utilidades
from modulos import logs


def crear():
    
    lista = almacenamiento.cargar(RUTA_HERRAMIENTAS)

    print("\n--- NUEVA HERRAMIENTA ---")
    nombre = utilidades.pedir_texto("Nombre: ")
    categoria = utilidades.pedir_opcion("Categoria:", CATEGORIAS)
    cantidad = utilidades.pedir_entero("Cantidad disponible: ", 0)
    estado = utilidades.pedir_opcion("Estado:", ESTADOS_HERRAMIENTA)
    valor = utilidades.pedir_entero("Valor estimado: ", 0)

    herramienta = {
        "id": utilidades.generar_id(lista),
        "nombre": nombre,
        "categoria": categoria,
        "cantidad": cantidad,
        "estado": estado,
        "valor": valor
    }

    lista.append(herramienta)
    almacenamiento.guardar(RUTA_HERRAMIENTAS, lista)

    print("Herramienta creada con id " + str(herramienta["id"]) + ".")
    logs.info("Herramienta '" + nombre + "' creada con id " + str(herramienta["id"]))


def mostrar_una(h):
    print(str(h["id"]) + ". " + h["nombre"] +
          " | " + h["categoria"] +
          " | cantidad: " + str(h["cantidad"]) +
          " | " + h["estado"] +
          " | $" + str(h["valor"]))


def listar():
    lista = almacenamiento.cargar(RUTA_HERRAMIENTAS)

    if len(lista) == 0:
        print("\nNo hay herramientas registradas.")
        return

    print("\n--- HERRAMIENTAS ---")
    for h in lista:
        mostrar_una(h)


def buscar():
    lista = almacenamiento.cargar(RUTA_HERRAMIENTAS)

    if len(lista) == 0:
        print("\nNo hay herramientas registradas.")
        return

    texto = utilidades.pedir_texto("Buscar (nombre o categoria): ").lower()

    encontradas = []
    for h in lista:
        if texto in h["nombre"].lower() or texto in h["categoria"].lower():
            encontradas.append(h)

    if len(encontradas) == 0:
        print("No se encontro ninguna herramienta.")
        return

    print("\n--- RESULTADOS ---")
    for h in encontradas:
        mostrar_una(h)


def actualizar():
    lista = almacenamiento.cargar(RUTA_HERRAMIENTAS)

    if len(lista) == 0:
        print("\nNo hay herramientas registradas.")
        return

    listar()
    id_buscado = utilidades.pedir_entero("\nId de la herramienta a actualizar: ", 1)
    herramienta = utilidades.buscar_por_id(lista, id_buscado)

    if herramienta is None:
        print("No existe una herramienta con ese id.")
        logs.error("Intento de actualizar herramienta inexistente id " + str(id_buscado))
        return

    print("\nDeje vacio para no cambiar el nombre.")
    nombre = input("Nombre [" + herramienta["nombre"] + "]: ").strip()
    if nombre != "":
        herramienta["nombre"] = nombre

    herramienta["categoria"] = utilidades.pedir_opcion("Categoria:", CATEGORIAS)
    herramienta["cantidad"] = utilidades.pedir_entero("Cantidad: ", 0)
    herramienta["estado"] = utilidades.pedir_opcion("Estado:", ESTADOS_HERRAMIENTA)
    herramienta["valor"] = utilidades.pedir_entero("Valor estimado: ", 0)

    almacenamiento.guardar(RUTA_HERRAMIENTAS, lista)

    print("Herramienta actualizada.")
    logs.info("Herramienta id " + str(id_buscado) + " actualizada")


def eliminar():
    lista = almacenamiento.cargar(RUTA_HERRAMIENTAS)

    if len(lista) == 0:
        print("\nNo hay herramientas registradas.")
        return

    listar()
    id_buscado = utilidades.pedir_entero("\nId de la herramienta: ", 1)
    herramienta = utilidades.buscar_por_id(lista, id_buscado)

    if herramienta is None:
        print("No existe una herramienta con ese id.")
        logs.error("Intento de eliminar herramienta inexistente id " + str(id_buscado))
        return

    print("\n1. Inactivar")
    print("2. Eliminar definitivamente")
    opcion = utilidades.pedir_entero("Opcion: ", 1)

    if opcion == 1:
        herramienta["estado"] = "Inactiva"
        almacenamiento.guardar(RUTA_HERRAMIENTAS, lista)
        print("Herramienta inactivada.")
        logs.info("Herramienta id " + str(id_buscado) + " inactivada")

    elif opcion == 2:
        if utilidades.confirmar("Seguro que desea eliminar '" + herramienta["nombre"] + "'?"):
            lista.remove(herramienta)
            almacenamiento.guardar(RUTA_HERRAMIENTAS, lista)
            print("Herramienta eliminada.")
            logs.info("Herramienta id " + str(id_buscado) + " eliminada")
        else:
            print("Operacion cancelada.")

    else:
        print("Opcion invalida.")