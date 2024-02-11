#pylint: disable=invalid-name
"""Se desabilita Pylint por requerimiento para el nombre del programa"""
import time
import json
import math
from tabulate import tabulate

readfile1 = input()
readfile2 = input()
start = time.time()

def read_json(json_data):
    '''Se extrae archivo json ya sea si es string u objeto'''
    if isinstance(json_data, str) is True:
        return json.loads(json_data)
    if str(type(json_data)) == "<class '_io.TextIOWrapper'>":
        return json.load(json_data)
    return None

with open(readfile1, 'r', encoding="utf-8") as f1:
    productos = read_json(f1)

with open(readfile2, 'r',  encoding="utf-8") as f2:
    ventas = read_json(f2)

CantidadProductos = len(productos)

def remover_strings(s):
    """Removes invalid data in list"""
    if not s:
        print("INVALID DATA REMOVED: ", s)
        return float("nan")
    try:
        f = float(s)
        i = int(f)
        return i if f == i else f
    except ValueError:
        print("INVALID DATA REMOVED: ", s)
        return float("nan")

columnas = 2
filas = CantidadProductos
ListaProductos = [[0] * columnas for _ in range(filas)]
skip = 0

for n in range(CantidadProductos):
    precioEvaluar = productos[n]['price']
    precioIntFloat = remover_strings(precioEvaluar)
    #if precioIntFloat is not float("nan"):
    if math.isnan(precioIntFloat) is not True:
        ListaProductos[n-skip][0] = productos[n]['title']
        ListaProductos[n-skip][1] = precioIntFloat
        continue
    skip = skip + 1

ListaProductos.sort()

print("ORIGINAL TOTAL PRODUCTS: ", len(productos))
print("TOTAL REMOVED PRODUCTS: ", len(productos) - len(ListaProductos))

CantidadProductos = len(ListaProductos)

CantidadVentas = len(ventas)
ListaVentas = [[0] * columnas for _ in range(CantidadVentas)]
skip = 0

for m in range(CantidadVentas):
    cantidadEvaluar = ventas[m]['Quantity']
    cantidadIntFloat = remover_strings(cantidadEvaluar)
    #if cantidadIntFloat is not float("nan"):
    if math.isnan(cantidadIntFloat) is not True:
        ListaVentas[m-skip][0] = ventas[m]['Product']
        ListaVentas[m-skip][1] = cantidadIntFloat
        continue
    skip = skip + 1

ListaVentas.sort()
CantidadVentas = len(ListaVentas)

contador = ListaVentas[0][1]
for k in range(CantidadVentas):
    if ListaVentas[k][0] == ListaVentas[0][0]:
        contador = contador + ListaVentas[k][1]

VentasUnicas = [[ListaVentas[0][0],contador]]

for a in range(CantidadVentas):
    venta_evaluar = ListaVentas[a][0]
    CantidadVentasUnicas = len(VentasUnicas)
    for b in range(CantidadVentasUnicas):
        if venta_evaluar == VentasUnicas[-1][0]:
            continue
        ventas_realizadas = ListaVentas[a][1]
        contador_frecuencia = 1
        c = a
        for c in range(CantidadVentas):
            if venta_evaluar == ListaVentas[-1][0]:
                VentasUnicas.append([venta_evaluar,ventas_realizadas])
                break
            if venta_evaluar == ListaVentas[a+contador_frecuencia][0]:
                ventas_realizadas = ventas_realizadas + ListaVentas[a+contador_frecuencia][1]
                contador_frecuencia = contador_frecuencia + 1
            else:
                VentasUnicas.append([venta_evaluar,ventas_realizadas])
                break

VentasReales = []
CantidadVentasUnicas = len(VentasUnicas)
totalVendido = 0
salto = 0

for d in range(CantidadVentasUnicas):
    producto_evaluar = VentasUnicas[d][0]
    for e in range(CantidadProductos):
        if producto_evaluar == ListaProductos[e][0]:
            precioUnitario = ListaProductos[e][1]
            cantidad = VentasUnicas[d][1]
            subtotal = precioUnitario * cantidad
            VentasReales.append([producto_evaluar, precioUnitario, cantidad, subtotal])
            totalVendido = totalVendido + subtotal
            break
        if ListaProductos[e][0] == ListaProductos[-1][0]:
            print(producto_evaluar, " IS NOT IN OUR SYSTEM, ITEM REMOVED.")

TablaDatos = tabulate(VentasReales,headers=['PRODUCTOS','PRECIO UNITARIO','CANTIDAD','SUBTOTAL'])
print(TablaDatos)
print("=========================================================================")
print("TOTAL: ", totalVendido)
print("=========================================================================")
print('TOTAL PRODUCTOS: ', len(ListaProductos))
print('UNIQUE SALES: ', len(VentasUnicas))
print('REMOVED PRODUCTS: ', len(VentasUnicas)-len(VentasReales))

with open("SalesResults.txt", "w", encoding="utf-8") as writefile:
    L1 = ["FILE NAME: ", readfile2, "\n"]
    writefile.writelines(L1)

    datos = str(TablaDatos)
    L2 = [datos, '\n']
    writefile.writelines(L2)

    L3 = ["=========================================================================", "\n"]
    writefile.writelines(L3)

    grandTotal = str(totalVendido)
    L4 = ["TOTAL: ", grandTotal, "\n"]
    writefile.writelines(L4)

    writefile.writelines(L3)

    end = time.time()
    timee = end - start
    tiempo = str(timee)
    L5 = ["TIME: ", tiempo, " SEG\n"]
    writefile.writelines(L5)

    writefile.close()

print("TIME: ", tiempo, " SEG")
