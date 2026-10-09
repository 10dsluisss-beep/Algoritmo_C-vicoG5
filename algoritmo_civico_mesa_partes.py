"""
ALGORITMO CÍVICO - Sistema de Mesa de Partes
Entrega 1: Estructuras fundamentales, funciones y modularidad inicial
Lenguaje: Python 3.x
Equipo: Algoritmo Cívico - UPN

El programa es un prototipo educativo. Guarda expedientes en expedientes.csv
en la misma carpeta del programa.
"""

import csv
import os
from datetime import datetime

ARCHIVO_CSV = "expedientes.csv"
PREFIJO_CODIGO = "EXP"
ANIO = datetime.now().year
contador_sesiones = 0  # Variable global de demostración


def cargar_expedientes():
    """Retorna los expedientes guardados; si no existe el archivo, retorna lista vacía."""
    expedientes = []
    if not os.path.exists(ARCHIVO_CSV):
        return expedientes
    try:
        with open(ARCHIVO_CSV, "r", newline="", encoding="utf-8") as archivo:
            lector = csv.DictReader(archivo)
            expedientes = list(lector)
    except (OSError, csv.Error) as error:
        print(f"Advertencia: no se pudo leer el archivo: {error}")
    return expedientes


def guardar_expedientes(expedientes):
    """Guarda la lista completa en CSV. Función sin retorno explícito."""
    campos = ["codigo", "dni", "ciudadano", "telefono", "correo",
              "asunto", "area", "folios", "fecha"]
    try:
        with open(ARCHIVO_CSV, "w", newline="", encoding="utf-8") as archivo:
            escritor = csv.DictWriter(archivo, fieldnames=campos)
            escritor.writeheader()
            escritor.writerows(expedientes)
    except OSError as error:
        print(f"Error al guardar los expedientes: {error}")


def validar_dni(dni):
    """Retorna True si el DNI contiene exactamente ocho dígitos."""
    return dni.isdigit() and len(dni) == 8


def validar_correo(correo):
    """Validación básica de correo para el prototipo."""
    return "@" in correo and "." in correo.split("@")[-1]


def siguiente_codigo(expedientes):
    """Genera un código correlativo a partir de los códigos existentes."""
    mayor = 0
    for expediente in expedientes:
        codigo = expediente.get("codigo", "")
        try:
            numero = int(codigo.split("-")[1])
            mayor = max(mayor, numero)
        except (IndexError, ValueError):
            continue
    return f"{PREFIJO_CODIGO}-{mayor + 1:05d}-{ANIO}"


def leer_texto(mensaje):
    """Solicita un texto no vacío; usa while para permitir reintentos."""
    while True:
        dato = input(mensaje).strip()
        if dato:
            return dato
        print("El campo no puede quedar vacío. Intente nuevamente.")


def leer_folios():
    """Solicita un número entero de folios mayor que cero."""
    while True:
        entrada = input("Cantidad de folios (entero mayor que 0): ").strip()
        if entrada.isdigit() and int(entrada) > 0:
            return int(entrada)
        print("Entrada inválida. Ingrese un entero mayor que cero.")


def registrar_expediente(expedientes):
    """Función operativa: valida, agrega al arreglo/lista y persiste el registro."""
    print("\n--- REGISTRO DE EXPEDIENTE ---")
    while True:
        dni = leer_texto("DNI (8 dígitos): ")
        if validar_dni(dni):
            break
        print("DNI inválido: debe contener exactamente 8 números.")

    ciudadano = leer_texto("Nombres y apellidos: ")
    telefono = leer_texto("Teléfono: ")
    while True:
        correo = leer_texto("Correo electrónico: ")
        if validar_correo(correo):
            break
        print("Correo inválido. Ejemplo: usuario@correo.com")

    asunto = leer_texto("Asunto del trámite: ")
    area = leer_texto("Área destinataria: ")
    folios = leer_folios()

    expediente = {
        "codigo": siguiente_codigo(expedientes),
        "dni": dni,
        "ciudadano": ciudadano,
        "telefono": telefono,
        "correo": correo,
        "asunto": asunto,
        "area": area,
        "folios": str(folios),
        "fecha": datetime.now().strftime("%Y-%m-%d %H:%M")
    }
    expedientes.append(expediente)  # Mutación de la lista recibida como parámetro
    guardar_expedientes(expedientes)
    print(f"\nExpediente registrado correctamente. Código: {expediente['codigo']}")


def mostrar_expediente(expediente):
    """Imprime un expediente. Función sin retorno explícito."""
    print("-" * 48)
    for campo, valor in expediente.items():
        print(f"{campo.capitalize():12}: {valor}")
    print("-" * 48)


def listar_expedientes(expedientes):
    """Muestra todos los expedientes; usa for para recorrer la lista."""
    if not expedientes:
        print("\nNo hay expedientes registrados.")
        return
    print(f"\n--- EXPEDIENTES REGISTRADOS: {len(expedientes)} ---")
    for expediente in expedientes:
        mostrar_expediente(expediente)


def buscar_expediente(expedientes):
    """Busca por código o DNI y muestra coincidencias."""
    criterio = leer_texto("Ingrese código de expediente o DNI: ").lower()
    encontrados = [
        expediente for expediente in expedientes
        if expediente.get("codigo", "").lower() == criterio
        or expediente.get("dni", "") == criterio
    ]
    if encontrados:
        for expediente in encontrados:
            mostrar_expediente(expediente)
    else:
        print("No se encontraron expedientes con ese código o DNI.")


def ordenar_expedientes(expedientes):
    """Ordena por código y muestra los resultados."""
    ordenados = sorted(expedientes, key=lambda expediente: expediente.get("codigo", ""))
    if not ordenados:
        print("No hay expedientes para ordenar.")
        return
    print("\n--- LISTADO ORDENADO POR CÓDIGO ---")
    for expediente in ordenados:
        print(f"{expediente['codigo']} | {expediente['ciudadano']} | {expediente['asunto']}")


def resumen_total(expedientes):
    """Retorna un resumen calculado a partir de la lista."""
    return f"Total de expedientes registrados: {len(expedientes)}"


def demostrar_alcances():
    """Demuestra variable local, global y no local."""
    mensaje_local = "Esta variable existe solo dentro de demostrar_alcances()."

    def funcion_interna():
        mensaje_no_local = "Variable no local modificada por la función interna."

        def modificar_no_local():
            nonlocal mensaje_no_local
            mensaje_no_local = "La variable no local fue modificada correctamente."

        modificar_no_local()
        print(mensaje_no_local)

    global contador_sesiones
    contador_sesiones += 1
    print(mensaje_local)
    funcion_interna()
    print(f"Variable global contador_sesiones: {contador_sesiones}")


def demostrar_parametros():
    """Demuestra que el nombre local se reasigna y que una lista mutable puede modificarse."""
    numero = 10
    lista_demo = ["inicio"]

    def intentar_cambiar_numero(valor):
        valor = 99  # Reasignación local; no cambia la variable externa
        print(f"Dentro de la función, valor = {valor}")

    def agregar_elemento(lista):
        lista.append("agregado")  # Modifica el mismo objeto lista

    intentar_cambiar_numero(numero)
    agregar_elemento(lista_demo)
    print(f"Fuera de la función, numero = {numero} (sigue siendo 10)")
    print(f"Fuera de la función, lista_demo = {lista_demo} (se modificó la lista)")


def mostrar_menu():
    """Muestra el menú principal."""
    print("\n" + "=" * 48)
    print("      ALGORITMO CÍVICO - MESA DE PARTES")
    print("=" * 48)
    print("1. Registrar expediente")
    print("2. Listar expedientes")
    print("3. Buscar por código o DNI")
    print("4. Ordenar expedientes por código")
    print("5. Ver resumen total")
    print("6. Demostrar alcance de variables")
    print("7. Demostrar parámetros")
    print("0. Guardar y salir")


def main():
    """Controla la navegación del menú con while e if/elif/else."""
    expedientes = cargar_expedientes()
    print("Sistema educativo de registro de expedientes municipales.")
    while True:
        mostrar_menu()
        opcion = input("Seleccione una opción: ").strip()

        if opcion == "1":
            registrar_expediente(expedientes)
        elif opcion == "2":
            listar_expedientes(expedientes)
        elif opcion == "3":
            buscar_expediente(expedientes)
        elif opcion == "4":
            ordenar_expedientes(expedientes)
        elif opcion == "5":
            print(resumen_total(expedientes))
        elif opcion == "6":
            demostrar_alcances()
        elif opcion == "7":
            demostrar_parametros()
        elif opcion == "0":
            guardar_expedientes(expedientes)
            print("Datos guardados. Gracias por usar Algoritmo Cívico.")
            break
        else:
            print("Opción no válida. Seleccione una opción del menú.")


if __name__ == "__main__":
    main()
