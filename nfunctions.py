import re
import os
import json
import csv
import random

path = "insumos.csv"


def menu():
    """
    Muestra el menú de opciones y solicita al usuario que ingrese una opción.

    Returns:
        str: Opción ingresada por el usuario.
    """
    print("""
        1. Cargar datos desde archivo.
        2. Listar cantidad por marca.
        3. Listar insumos por marca.
        4. Buscar insumo por característica.
        5. Listar insumos ordenados.
        6. Realizar compras.
        7. Guardar en formato JSON.
        8. Leer desde formato JSON.
        9. Actualizar precios.
        10. Acceder al siguiente menu.
        11. Salir del programa.
        """)
    opcion = input("Ingrese una opción: ")
    return opcion


def menu_2():
    print("""
        1. Agregar nuevo producto.
        2. Mostrar datos.
        3. Actualizar datos.
        4. Volver al menu anterior.
        5. Siguiente menu.
        6. Salir del programa.
        """)
    opcion = input("Ingrese una opción: ")
    return opcion


def mostrar_datos_productos(datos: dict):
    for dato in datos:
        print(f"ID: {dato['id']}")
        print(f"Descripción: {dato['nombre']}")
        print(f"Marca: {dato['marca']}")
        print(f"Precio: ${dato['precio']}")
        print(f"Característica: {dato['caracteristicas']}")
        print("--------------------------------------------------------------------------")


# ----------------------------------------------------------------------------------------------------
# 1

def formatear_csv(path: str):
    """
    Lee un archivo CSV y retorna una lista de diccionarios con los datos formateados.

    Args:
        path (str): Ruta del archivo CSV.

    Returns:
        list: Lista de diccionarios con los datos formateados.
    """
    with open(path, encoding="utf8") as archivo:
        lista = []
        next(archivo)
        for linea in archivo:
            linea = linea.strip().split(',')
            diccionario_insumo = {
                'id': linea[0],
                'nombre': linea[1],
                'marca': linea[2],
                'precio': float(linea[3].replace('$', '')),
                'caracteristicas': linea[4]
            }
            lista.append(diccionario_insumo)
    return lista

lista_formateada = formatear_csv(path)

def cargar_insumos():
    def calcular_stock_disponible(insumo):
        insumo['STOCK'] = random.randint(0, 10)
        return insumo
    data = list(map(calcular_stock_disponible, lista_formateada))
    return data

insumos = cargar_insumos()
# print(insumos)

# ----------------------------------------------------------------------------------------------------
# 2

def contar_cantidad_por_marca(lista: list, key: str):
    """
    Cuenta la cantidad de insumos por marca.

    Args:
        lista (list): Lista de insumos.
        key (str): Marca a contar.

    Returns:
        list: Lista de tuplas con la marca y la cantidad de insumos.
    """
    cantidad_por_marca = []
    for insumo in lista:
        marca = insumo[key]
        for item in cantidad_por_marca:
            if item[0] == marca:
                item[1] += 1
                break
        else:
            cantidad_por_marca.append([marca, 1])
    return cantidad_por_marca


# ----------------------------------------------------------------------------------------------------
# 3

def listar_insumos_por_marca(lista: list, key: str, key2: str, key3: str):
    """
    Lista los insumos agrupados por marca.

    Args:
        lista (list): Lista de insumos.
        key (str): Key de marca del producto.
        key2 (str): Key de nombre del producto.
        key3 (str): Key de precio del producto.

    Returns:
        dict: Diccionario que agrupa los insumos por marca.
    """
    insumos_por_marca = {}
    for insumo in lista:
        marca = insumo[key]
        nombre = insumo[key2]
        precio = insumo[key3]
        if marca not in insumos_por_marca:
            insumos_por_marca[marca] = []
        insumos_por_marca[marca].append([nombre, precio])
    return insumos_por_marca


# ----------------------------------------------------------------------------------------------------
# 4

def buscar_insumo_por_caracteristica(lista: list, key: str):
    """
    Busca un insumo por una característica ingresada por el usuario.

    Args:
        lista (list): Lista de insumos.
        key (str): Key de característica.

    Returns:
        list: Lista de diccionarios con los insumos que coinciden con la característica buscada.
    """
    lista_caracteristicas = []
    caracteristica = input("Ingrese la caracteristica a buscar: ").capitalize()
    if not caracteristica:
        print("La característica no puede ser un string vacío")
        return lista_caracteristicas
    for insumo in lista:
        if key in insumo and re.search(caracteristica, insumo[key]):
            lista_caracteristicas.append(insumo)
    if not lista_caracteristicas:
        print("No se encontraron insumos con las características buscadas")
    return lista_caracteristicas


# ----------------------------------------------------------------------------------------------------
# 5

def ordenar_insumos(lista: list, key: str, key2: int, key3: str):
    """
    Ordena la lista de insumos por marca de forma ascendente y por precio de forma descendente.

    Args:
        lista (list): Lista de insumos.
        key (str): Key de marca del producto.
        key2 (int): Key de precio del producto.
        key3 (str): Key de caracteristicas del producto.

    Returns:
        list: Lista de insumos ordenados.
    """
    for i in range(len(lista)):
        for j in range(len(lista) - 1 - i):
            if lista[j][key] > lista[j + 1][key]:
                lista[j], lista[j + 1] = lista[j + 1], lista[j]
            elif lista[j][key] == lista[j + 1][key] and lista[j][key2] < lista[j + 1][key2]:
                lista[j], lista[j + 1] = lista[j + 1], lista[j]

    for insumo in lista:
        caracteristicas = insumo[key3].split("~")
        insumo[key3] = caracteristicas[0]

    return lista


# ----------------------------------------------------------------------------------------------------
# 6

def buscar_por_marca(lista: list, marca: str):
    """
    Busca insumos por marca.

    Args:
        lista (list): Lista de insumos.
        marca (str): Marca a buscar.

    Returns:
        list: Lista de insumos que coinciden con la marca buscada.
    """
    productos_encontrados = []
    for producto in lista:
        if producto['marca'] == marca:
            productos_encontrados.append(producto)
    return productos_encontrados


def mostrar_datos_tienda(producto: dict):
    """
    Muestra los datos de un insumo en el formato de tienda.

    Args:
        producto (dict): Datos del insumo.
    """
    print(f"ID: {producto['id']}")
    print(f"Descripción: {producto['nombre']}")
    print(f"Precio: ${producto['marca']}")
    print(f"Marca: {producto['precio']}")
    print(f"Característica: {producto['caracteristicas']}")
    print("--------------------------------------------------------------------------")


def generar_factura(lista_productos: list, total_compra: float):
    """
    Genera una factura de compra con los productos seleccionados.

    Args:
        lista_productos (list): Lista de productos seleccionados.
        total_compra (float): Total de la compra.
    """
    factura = "FACTURA DE COMPRA\n"
    factura += "--------------------------------------------------------------------------\n"

    for producto in lista_productos:
        factura += f"Producto: {producto['producto']}\n"
        factura += f"Cantidad: {producto['cantidad']}\n"
        factura += f"Subtotal: ${producto['subtotal']}\n"
        factura += "--------------------------------------------------------------------------\n"

    nombre_archivo = input("Ingrese el nombre para guardar la factura: ")
    if nombre_archivo.strip() == "":
        print("Debe ingresar al menos un caracter para el nombre de la factura. La factura no será generada.")
        return

    nombre_archivo += ".txt"

    with open(nombre_archivo, 'w') as archivo:
        archivo.write(factura)

    print(
        f"La factura se ha guardado correctamente en el archivo: {nombre_archivo}")


def tienda(lista_insumos: list):
    """
    Simula una tienda donde se pueden realizar compras de insumos.

    Args:
        lista_insumos (list): Lista de insumos.
    """
    lista_productos = []
    lista_precios = []

    os.system('cls')

    while True:
        marca_buscada = input(
            "Ingrese la marca que busca (o 'x' para finalizar): ").capitalize()
        if marca_buscada == 'X':
            break

        productos_encontrados = buscar_por_marca(
            lista_insumos, marca_buscada)

        if productos_encontrados:
            print("Productos encontrados:")
            for producto in productos_encontrados:
                mostrar_datos_tienda(producto)

            id_seleccion = input(
                "Ingrese el ID del producto que desea (o 'x' para finalizar): ").capitalize()
            if id_seleccion == 'X':
                break

            producto_seleccionado = None
            for producto in productos_encontrados:
                if producto['id'] == id_seleccion:
                    producto_seleccionado = producto
                    break

            if producto_seleccionado is None:
                print("ID de producto inválido. Inténtelo nuevamente.")
                continue

            try:
                os.system('cls')
                cantidad_buscada = int(
                    input("Ingrese la cantidad que desea comprar: "))
                if cantidad_buscada < 0:
                    print("Cantidad inválida. Inténtelo nuevamente.")
                    continue

                subtotal = int(
                    producto_seleccionado['precio']) * cantidad_buscada

                lista_productos.append({
                    'producto': producto_seleccionado['nombre'],
                    'cantidad': cantidad_buscada,
                    'subtotal': subtotal
                })
                lista_precios.append(subtotal)

                print("Producto agregado al carrito.")

            except ValueError:
                print("Entrada inválida. Inténtelo nuevamente.")
                continue

    if len(lista_productos) > 0:
        print("Carrito de compras:")
        total_compra = sum(lista_precios)
        print(f"Total: ${total_compra}")

        generar_factura(lista_productos, total_compra)
    else:
        print("No se agregaron productos al carrito. La compra ha sido cancelada.")


# ----------------------------------------------------------------------------------------------------
# 7

def guardar_en_formato_json(lista_insumos: list):
    """
    Guarda los productos de alimento de la lista en un archivo JSON.

    Args:
        lista_insumos (list): Lista de insumos.
    """
    productos_alimento = []
    for insumo in lista_insumos:
        if "Alimento" in insumo["nombre"]:
            productos_alimento.append(insumo)

    if len(productos_alimento) > 0:
        nombre_archivo = "productos_alimento.json"
        with open(nombre_archivo, "w") as archivo:
            json.dump(productos_alimento, archivo, indent=4)
        print(
            f"Se ha generado el archivo JSON con los productos de alimento: {nombre_archivo}")
    else:
        print("No se encontraron productos de alimento.")


# ----------------------------------------------------------------------------------------------------
# 8

def leer_desde_formato_json():
    """
    Lee los productos de alimento desde un archivo JSON y los muestra en la consola.
    """
    nombre_archivo = "productos_alimento.json"

    try:
        with open(nombre_archivo, "r") as archivo:
            productos_alimento = json.load(archivo)

        print("Productos de alimento:")
        for producto in productos_alimento:
            print(f"ID: {producto['id']}")
            print(f"Nombre: {producto['nombre']}")
            print(f"Marca: {producto['marca']}")
            print(f"Precio: {producto['precio']}")
            print(f"Características: {producto['caracteristicas']}")
            print(
                "--------------------------------------------------------------------------")

    except FileNotFoundError:
        print("No se encontró el archivo JSON. Primero debe generar el archivo utilizando la opción 7.")


# ----------------------------------------------------------------------------------------------------
# 9

def actualizar_precios(lista_insumos: list):
    """
    Actualiza los precios de los productos de acuerdo a un porcentaje (8.4%) y guarda los productos actualizados en un archivo CSV.

    Args:
        lista_insumos (list): Lista de insumos.

    """
    porcentaje = 8.4

    def actualizar_precio(insumo: dict):
        """
        Actualiza el precio de un insumo según el porcentaje proporcionado.

        Args:
            insumo (dict): Diccionario que contiene los datos del insumo.

        Returns:
            dict: Diccionario con el insumo actualizado.

        """
        insumo['precio'] = round(
            insumo['precio'] + (insumo['precio'] * porcentaje / 100), 2)
        return insumo

    lista_insumos_actualizados = list(map(actualizar_precio, lista_insumos))

    try:
        with open('insumos_actualizados.csv', 'w', newline='') as archivo_csv:
            writer = csv.DictWriter(
                archivo_csv, fieldnames=lista_insumos_actualizados[0].keys())
            writer.writeheader()
            writer.writerows(lista_insumos_actualizados)
    except Exception as e:
        print("Ha ocurrido un error al guardar los insumos actualizados:", e)
        return

    print("Los precios se han actualizado correctamente y se han guardado en el archivo 'insumos_actualizados.csv'.")


# ----------------------------------------------------------------------------------------------------
# Requerimientos extra
# 1


def cargar_marcas():
    """
    Carga las marcas disponibles desde el archivo marcas.txt.

    Returns:
        list: Lista de marcas disponibles.
    """
    marcas = []
    with open('marcas.txt', 'r') as archivo:
        for linea in archivo:
            marcas.append(linea.strip())
    return marcas


def validar_numero(entrada):
    """
    Valida que la entrada sea un número entero positivo.

    Args:
        entrada: Valor ingresado por el usuario.

    Returns:
        int or None: El valor convertido a entero si es válido, None si no es válido.
    """
    try:
        numero = int(entrada)
        if numero > 0:
            return numero
    except ValueError:
        pass
    return None


def agregar_nuevo_producto(lista: list, key: str, key2: str, key3: str, key4: str, key5: str):
    """
    Agrega un nuevo producto a la lista de insumos.

    Args:
        lista (list): Lista de insumos.
        key (str): Key de id del producto.
        key2 (str): Key de nombre del producto.
        key3 (str): Key de marca del producto.
        key4 (str): Key de precio del producto.
        key5 (str): Key de características del producto.

    Returns:
        list: Lista de insumos actualizada.
    """
    nuevo_producto = {}

    marcas = cargar_marcas()
    print("Marcas disponibles:")
    for marca in marcas:
        print(marca)

    while True:
        marca = input(
            "Ingrese la marca del producto ('x' para cancelar): ").capitalize()
        if marca == 'X':
            print("Cancelando. No se agregó ningún producto.")
            return lista
        elif marca not in marcas or marca.isdigit():
            print("Marca inválida. Por favor, ingrese una marca válida.")
            continue
        else:
            nuevo_producto[key3] = marca
            break

    id_producto = str(len(lista) + 1)
    nuevo_producto[key] = id_producto

    while True:
        nombre = input(
            "Ingrese el nombre del producto ('x' para cancelar): ").capitalize()
        if nombre == 'X':
            print("Cancelando. No se agregó ningún producto.")
            return lista
        elif nombre.isdigit():
            print("Nombre inválido. Por favor, ingrese un nombre válido.")
        else:
            nuevo_producto[key2] = nombre.capitalize()
            break

    while True:
        precio = input("Ingrese el precio del producto ('x' para cancelar): ")
        if precio == 'x':
            print("Cancelando. No se agregó ningún producto.")
            return lista
        elif not precio.replace('.', '', 1).isdigit():
            print("Precio inválido. Por favor, ingrese un número válido.")
            continue
        else:
            nuevo_producto[key4] = float(precio)
            break

    caracteristicas_agregadas = 0
    while caracteristicas_agregadas < 3:
        opcion = input(
            f"Ingrese la característica {caracteristicas_agregadas + 1} ('x' para cancelar, 'xx' para finalizar): ").capitalize()

        if opcion == 'X':
            print("Cancelando. No se agregó ningún producto.")
            return lista
        elif opcion == 'Xx':
            break

        if opcion.isdigit():
            print(
                "Característica inválida. Por favor, ingrese una característica válida.")
            continue
        else:
            key5 = f'caracteristica_{caracteristicas_agregadas + 1}'
            caracteristicas = nuevo_producto.get(key5, "")
            if caracteristicas:
                caracteristicas += "~" + opcion
            else:
                caracteristicas = opcion
            nuevo_producto[key5] = caracteristicas
            caracteristicas_agregadas += 1

    if opcion == 'xx':
        for i in range(caracteristicas_agregadas + 1, 4):
            caracteristica_key = f'caracteristica_{i}'
            nuevo_producto[caracteristica_key] = ""

    lista.append(nuevo_producto)
    return lista


# 2


def actualizar_datos(lista: list, key: str, key2: str, key3: str, key4: str, key5: str):
    """
    Actualiza y guarda los datos de la lista en un archivo en el formato especificado.

    Args:
        lista (list): Lista de productos.
        key (str): Key de id del producto.
        key2 (str): Key de nombre del producto.
        key3 (str): Key de marca del producto.
        key4 (str): Key de precio del producto.
        key5 (str): Key de características del producto.

    Returns:
        None
    """
    formato = input("Ingrese el formato de exportación (csv/json): ")

    if formato.lower() == "csv":
        with open("nuevos_insumos.csv", "w", encoding="utf-8", newline="") as archivo:
            escritor = csv.writer(archivo)
            escritor.writerow(
                ["ID", "NOMBRE", "MARCA", "PRECIO", "CARACTERISTICAS"])
            for producto in lista:
                caracteristicas = producto[key5]
                escritor.writerow([
                    producto[key],
                    producto[key2],
                    producto[key3],
                    producto[key4],
                    caracteristicas
                ])

        print("Datos actualizados guardados en el archivo nuevos_insumos.csv.")

    elif formato.lower() == "json":
        with open("nuevos_insumos.json", "w", encoding="utf-8") as archivo:
            json.dump(lista, archivo)

        print("Datos actualizados guardados en el archivo nuevos_insumos.json.")
    else:
        print("Formato de exportación inválido. No se guardaron los datos actualizados.")

# ----------------------------------------------------------------------------------------------------
# 1.B

def realizar_venta():
    """
    Realiza la venta de un producto.

    Muestra los productos disponibles y solicita al usuario el ID del producto y la cantidad deseada.
    Verifica que el ID sea un número válido en el rango de 1 a 50 y realiza la venta si hay suficiente stock.
    """
    print("Productos disponibles:")
    for insumo in insumos:
        print(f"ID: {insumo['ID']}")
        print(f"Descripción: {insumo['NOMBRE']}")
        print(f"Marca: {insumo['MARCA']}")
        print(f"Precio: ${insumo['PRECIO']}")
        print(f"Stock disponible: {insumo['STOCK']}")
        print("-----------------------------------")

    try:
        id_producto = input("Ingrese el ID del producto que desea vender: ")
        cantidad = int(input("Ingrese la cantidad que desea vender: "))

        if not (id_producto.isdigit() and 1 <= int(id_producto) <= 50):
            raise ValueError("ID de producto inválido. Por favor, ingrese un ID válido.")

        for insumo in insumos:
            if insumo['ID'] == id_producto:
                if insumo['STOCK'] >= cantidad:
                    insumo['STOCK'] -= cantidad
                    print("Venta realizada correctamente.")
                else:
                    print("No hay stock suficiente para realizar la venta. Por favor, compre menos cantidad.")
                break
        else:
            print("ID de producto no encontrado. Por favor, ingrese un ID válido.")

    except ValueError as e:
        print(f"Error: {str(e)} Ingrese valores válidos para el ID del producto y la cantidad.")

def menu_3():
    print("1. Realizar venta")
    print("2. Salir")
    opcion = input("Ingrese una opción: ")
    return opcion