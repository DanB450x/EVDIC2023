import psycopg2
from tabulate import tabulate
import math

# Parámetros de conexión a la base de datos PostgreSQL
parametros_conexion = {
    'host': 'localhost',
    'port': '5432',
    'user': 'postgres',
    'password': 'proyectos',
    'dbname': 'areas'
}

# Función para obtener el historial desde la base de datos
def Historial():
    try:
        with psycopg2.connect(**parametros_conexion) as conexion:
            with conexion.cursor() as cursor:
                cursor.execute("SELECT * FROM ej9;")
                rows = cursor.fetchall()
                print(tabulate(rows, headers=["numero", "figura", "area"], tablefmt="psql", numalign="center"))
    except Exception as e:
        print(f"Error en la conexión o la consulta: {e}\n")

# Función para insertar datos en la base de datos
def Post(figura, area):
    try:
        with psycopg2.connect(**parametros_conexion) as conexion:
            with conexion.cursor() as cursor:
                instruccion = "INSERT INTO ej9(figura, area) VALUES (%s, %s);"
                valores = (figura, area)
                cursor.execute(instruccion, valores)
                conexion.commit()
        print("Se ha añadido a la base de datos.")
    except Exception as e:
        print(f"Error en el ingreso de datos o conexión: {e}\n")

# Función para calcular el área de un círculo
def Circulo():
    radio = float(input("Ingrese el radio del Círculo: "))
    area = math.pi * radio**2
    return area

# Función para calcular el área de un triángulo
def Triangulo():
    base = float(input("Ingrese la base del Triángulo: "))
    altura = float(input("Ingrese la altura del Triángulo: "))
    area = 0.5 * base * altura
    return area

# Función para calcular el área de un cuadrado
def Cuadrado():
    lado = float(input("Ingrese el lado del Cuadrado: "))
    area = lado**2
    return area

# Función para calcular el área de un rectángulo
def Rectangulo():
    largo = float(input("Ingrese el largo del Rectángulo: "))
    ancho = float(input("Ingrese el ancho del Rectángulo: "))
    area = largo * ancho
    return area

# Menú principal
opcion = " "

print("Calculador de ÁREA")

while opcion != 'X':
    print("Seleccione una opción del siguiente menú:\n'1' Círculo\n'2' Triángulo\n'3' Cuadrado\n'4' Rectángulo\n'0' Ver historial\n'X' Salir")
    opcion = input("Su elección: ").upper()

    if opcion == '1':
        figura = 'círculo'
        numero = Circulo()
        Post(figura, numero)
    elif opcion == '2':
        figura = 'triángulo'
        numero = Triangulo()
        Post(figura, numero)
    elif opcion == '3':
        figura = 'cuadrado'
        numero = Cuadrado()
        Post(figura, numero)
    elif opcion == '4':
        figura = 'rectángulo'
        numero = Rectangulo()
        Post(figura, numero)
    elif opcion == '0':
        Historial()
    elif opcion == 'X':
        break
    else:
        print("Opción no válida, ingrese una de las opciones del menú")

# Salida en un archivo de texto
with open('areas.txt', 'w') as f:
    f.write("Resultados del historial:\n")
    try:
        with psycopg2.connect(**parametros_conexion) as conexion:
            with conexion.cursor() as cursor:
                cursor.execute("SELECT * FROM ej9;")
                rows = cursor.fetchall()
                for row in rows:
                    f.write(str(row) + '\n')
    except Exception as e:
        f.write(f"Error en la conexión o la consulta: {e}\n")

print("Programa finalizado.")
