from config import RUTA_USUARIOS, TIPOS_USUARIO
from modulos import almacenamiento
from modulos import utilidades
from modulos import logs

def crear():
    lista = almacenamiento.cargar(RUTA_USUARIOS)

    print("\n--- NUEVO USUARIO ---")
    nombres = utilidades.pedir_texto("Nombre: ")
    apellidos = utilidades.pedir_texto("Apellidos: ")
    telefono = utilidades.pedir_texto("Telefono: ")
    direccion = utilidades.pedir_texto("Direccion: ")
    tipo = utilidades.pedir_opcion("Tipo de usuario:", TIPOS_USUARIO)

    usuario = {
        "id": utilidades.generar_id(lista),
        "nombres": nombres,
        "apellidos": apellidos,
        "telefono": telefono,
        "direccion": direccion,
        "tipo": tipo
    }

    lista.append(usuario)
    almacenamiento.guardar(RUTA_USUARIOS, lista)

    print("\U00002705 Usuario creado con id " + str(usuario["id"]) + ".")
    logs.info("Usuario '" + nombres + " " + apellidos + "' creado con id " + str(usuario["id"]))


def mostrar_uno(u):
    print(str(u["id"]) + ". " + u["nombres"] + " " + u["apellidos"] +
          " | tel: " + u["telefono"] +
          " | " + u["direccion"] +
          " | " + u["tipo"])

def listar():
    lista = almacenamiento.cargar(RUTA_USUARIOS)

    if len(lista) == 0:
        print("\nNo hay usuarios registrados.")
        return

    print("\n--- USUARIOS ---")
    for u in lista:
        mostrar_uno(u)


def buscar():
    lista = almacenamiento.cargar(RUTA_USUARIOS)

    if len(lista) == 0:
            print("\U0001F4EC \nNo hay usuarios registrados.")
            return

    texto = utilidades.pedir_texto("Buscar (nombre, apellido o telefono): ").lower()

    encontrados = []
    for u in lista:
         if (texto in u["nombres"].lower() or
             texto in u["apellidos"].lower() or
             texto in u["telefono"]):
            encontrados.append(u)

    if len(encontrados) == 0:
        print("\nNo se encontro ningun usuario registrado.")
        return

    print("\n--- RESULTADOS ---")
    for u in encontrados:
        mostrar_uno(u)


def actualizar():
    lista = almacenamiento.cargar(RUTA_USUARIOS)

    if len(lista) == 0:
        print("\nNo hay usuarios registrados.")
        return

    listar()
    id_buscado = utilidades.pedir_entero("\nId del usuario a actualizar: ", 1)
    usuario = utilidades.buscar_por_id(lista, id_buscado)

    if usuario is None:
        print("\U0000274C No existe un usuario con ese id.")
        logs.error("Intento de actualizar usuario inexistente id " + str(id_buscado))
        return

    print("\nDeje vacio para no cambiar el dato.")

    nombres = input("Nombres [" + usuario["nombres"] + "]: ").strip()
    if nombres != "":
        usuario["nombres"] = nombres

    apellidos = input("Apellidos [" + usuario["apellidos"] + "]: ").strip()
    if apellidos != "":
        usuario["apellidos"] = apellidos

    telefono = input("Telefono [" + usuario["telefono"] + "]: ").strip()
    if telefono != "":
        usuario["telefono"] = telefono

    direccion = input("Direccion [" + usuario["direccion"] + "]: ").strip()
    if direccion != "":
        usuario["direccion"] = direccion

    usuario["tipo"] = utilidades.pedir_opcion("Tipo de usuario:", TIPOS_USUARIO)

    almacenamiento.guardar(RUTA_USUARIOS, lista)

    print("\U0000270F Usuario actualizado.")
    logs.info("Usuario id " + str(id_buscado) + " actualizado")


def eliminar():
    lista = almacenamiento.cargar(RUTA_USUARIOS)

    if len(lista) == 0:
        print("\U0001F4EC \nNo hay usuarios registrados.")
        return

    listar()
    id_buscado = utilidades.pedir_entero("\nId del usuario a eliminar: ", 1)
    usuario = utilidades.buscar_por_id(lista, id_buscado)

    if usuario is None:
        print("No existe un usuario con ese id.")
        logs.error("Intento de eliminar usuario inexistente id " + str(id_buscado))
        return

    nombre_completo = usuario["nombres"] + " " + usuario["apellidos"]

    if utilidades.confirmar("Seguro que desea eliminar a '" + nombre_completo + "'?"):
        lista.remove(usuario)
        almacenamiento.guardar(RUTA_USUARIOS, lista)
        print("\U0001F5D1 Usuario eliminado.")
        logs.info("Usuario id " + str(id_buscado) + " eliminado")
    else:
        print("Operacion cancelada.")

    
