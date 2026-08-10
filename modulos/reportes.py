from config import RUTA_PRESTAMOS, RUTA_HERRAMIENTAS, RUTA_USUARIOS, STOCK_MINIMO
from modulos import almacenamiento
from modulos import utilidades
from modulos import logs
from modulos import prestamos

def stock_bajo():
    herramientas = almacenamiento.cargar(RUTA_HERRAMIENTAS)

    if len(herramientas) == 0:
        print("\nNo hay herramientas registradas.")
        return

    bajas = []
    for h in herramientas:
        if h["cantidad"] < STOCK_MINIMO:
            bajas.append(h)

    if len(bajas) == 0:
        print("\nTodas las herramientas tienen stock suficiente.")
        return

    print("\n--- STOCK BAJO (menos de " + str(STOCK_MINIMO) + ") ---")
    for h in bajas:
        print(str(h["id"]) + ". " + h["nombre"] +
              " | quedan: " + str(h["cantidad"]) +
              " | " + h["estado"])

    logs.advertencia("Reporte de stock bajo generado. " + str(len(bajas)) + " herramientas.")


def prestamos_activos_y_vencidos():
    lista = almacenamiento.cargar(RUTA_PRESTAMOS)
    herramientas = almacenamiento.cargar(RUTA_HERRAMIENTAS)

    activos = []
    vencidos = []

    for p in lista:
        if p["estado"] == "Activo":
            if prestamos.esta_vencido(p):
                vencidos.append(p)
            else:
                activos.append(p)

    print("\n--- PRESTAMOS ACTIVOS (" + str(len(activos)) + ") ---")
    if len(activos) == 0:
        print("No hay prestamos activos.")
    else:
        for p in activos:
            prestamos.mostrar_uno(p, herramientas)

    print("\n--- PRESTAMOS VENCIDOS (" + str(len(vencidos)) + ") ---")
    if len(vencidos) == 0:
        print("No hay prestamos vencidos.")
    else:
        for p in vencidos:
            prestamos.mostrar_uno(p, herramientas)

    if len(vencidos) > 0:
        logs.advertencia("Hay " + str(len(vencidos)) + " prestamos vencidos.")


def historial_usuario():
    usuarios = almacenamiento.cargar(RUTA_USUARIOS)
    lista = almacenamiento.cargar(RUTA_PRESTAMOS)
    herramientas = almacenamiento.cargar(RUTA_HERRAMIENTAS)

    if len(usuarios) == 0:
        print("\nNo hay usuarios registrados.")
        return

    print("\nUsuarios:")
    for u in usuarios:
        print(str(u["id"]) + ". " + u["nombres"] + " " + u["apellidos"])

    id_usuario = utilidades.pedir_entero("Id del usuario: ", 1)
    usuario = utilidades.buscar_por_id(usuarios, id_usuario)

    if usuario is None:
        print("No existe un usuario con ese id.")
        return

    historial = []
    for p in lista:
        if p["usuario_id"] == id_usuario:
            historial.append(p)

    print("\n--- HISTORIAL DE " + usuario["nombres"] + " " + usuario["apellidos"] + " ---")

    if len(historial) == 0:
        print("Este usuario no tiene prestamos.")
        return

    for p in historial:
        prestamos.mostrar_uno(p, herramientas)

    print("\nTotal de prestamos: " + str(len(historial)))



def mas_solicitadas():
    lista = almacenamiento.cargar(RUTA_PRESTAMOS)
    herramientas = almacenamiento.cargar(RUTA_HERRAMIENTAS)

    if len(lista) == 0:
        print("\nNo hay prestamos registrados.")
        return

    conteo = {}
    for p in lista:
        id_h = p["herramienta_id"]
        if id_h in conteo:
            conteo[id_h] = conteo[id_h] + p["cantidad"]
        else:
            conteo[id_h] = p["cantidad"]

    ranking = []
    for id_h in conteo:
        herramienta = utilidades.buscar_por_id(herramientas, id_h)
        if herramienta is None:
            nombre = "(eliminada, id " + str(id_h) + ")"
        else:
            nombre = herramienta["nombre"]
        ranking.append({"nombre": nombre, "total": conteo[id_h]})

    ranking.sort(key=lambda x: x["total"], reverse=True)

    print("\n--- HERRAMIENTAS MAS SOLICITADAS ---")
    puesto = 1
    for r in ranking:
        print(str(puesto) + ". " + r["nombre"] + " | " + str(r["total"]) + " unidades prestadas")
        puesto = puesto + 1


def usuarios_mas_activos():
    lista = almacenamiento.cargar(RUTA_PRESTAMOS)
    usuarios = almacenamiento.cargar(RUTA_USUARIOS)

    if len(lista) == 0:
        print("\nNo hay prestamos registrados.")
        return

    conteo = {}
    for p in lista:
        id_h = p["usuario_id"]
        if id_h in conteo:
            conteo[id_h] = conteo[id_h] + p["cantidad"]
        else:
            conteo[id_h] = p["cantidad"]

    ranking = []
    for id_h in conteo:
        usuario = utilidades.buscar_por_id(usuarios, id_h)
        if usuario is None:
            nombre = "(eliminado, id " + str(id_h) + ")"
        else:
            nombre = usuario["nombres"] + " " + usuario["apellidos"]
        ranking.append({"nombre": nombre, "total": conteo[id_h]})

    ranking.sort(key=lambda x: x["total"], reverse=True)

    print("\n--- USUARIOS MAS ACTIVOS ---")
    puesto = 1
    for r in ranking:
        print(str(puesto) + ". " + r["nombre"] + " | " + str(r["total"]) + " herramientas solicitadas")
        puesto = puesto + 1


