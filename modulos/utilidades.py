def pedir_texto(mensaje):
    while True:
        texto = input(mensaje).strip()
        if texto != "":
            return texto
        print("\U000026A0 No se puede dejar vacio. Intente de nuevo.")


def pedir_entero(mensaje, minimo=0):
    while True:
        try:
            numero = int(input(mensaje))
            if numero >= minimo:
                return numero
            print(f"\U000026A0 El numero debe ser mayor o igual a {minimo}. Intente de nuevo.")
        except ValueError:
            print("\U000026A0 Debe ingresar un numero entero. Intente de nuevo.")


def pedir_opcion(mensaje, opciones):
    print(mensaje)
    for i in range(len(opciones)):
        print(" ", str(i + 1) + ")", opciones[i])

    numero = pedir_entero("Escoja una opcion: ", 1)
    while numero > len(opciones):
        print("\U000026A0 Esa opcion no existe.")
        numero = pedir_entero("Escoja una opcion: ", 1)

    return opciones[numero - 1]

def generar_id(lista):

    if len(lista) == 0:
        return 1

    mayor = 0
    for elemento in lista:
        if elemento["id"] > mayor:
            mayor = elemento["id"]

    return mayor + 1


def buscar_por_id(lista, id_buscado):
    for elemento in lista:
        if elemento["id"] == id_buscado:
            return elemento
    return None


def confirmar(mensaje):
    respuesta = input(mensaje + " (s/n): ").strip().lower()
    return respuesta == "s"


def pausar():
    input("\nPresione Enter para continuar....")
