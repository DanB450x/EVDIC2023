import psycopg2
import math
from tabulate import tabulate

def conectar_bd():
    try:
        conexion = psycopg2.connect(
            user="postgres",
            password="proyectos",
            host="localhost",
            port="5432",
            database="factorial"
        )
        return conexion
    except Exception as e:
        print("Error al conectar a la base de datos:", e)
        return None

def insertar_resultado(conexion, numero, factorial):
    try:
        cursor = conexion.cursor()
        cursor.execute("""
            INSERT INTO calculofac(numero, factorial)
            VALUES (%s, %s)
        """, (numero, factorial))
        conexion.commit()
        print("Resultado insertado correctamente.")
    except Exception as e:
        print("Error al insertar en la base de datos:", e)

def calcular_factorial(numero):
    if numero % 7 == 0:
        return math.factorial(numero)
    else:
        raise ValueError("El número no es divisible por 7. Error.")

def mostrar_historial(conexion):
    try:
        cursor = conexion.cursor()
        cursor.execute("SELECT * FROM calculofac")
        print(tabulate(cursor, headers=["numero", "factorial"], tablefmt="psql", numalign="center"))
    except Exception as e:
        print("Error al obtener el historial:", e)

def guardar_en_archivo(numero, factorial):
    with open('factorial.txt', 'a') as archivo:
        archivo.write(f"El factorial de {numero} es: {factorial}\n")

def main():
    conexion = conectar_bd()

    if conexion:
        while True:
            print("\nMenú:")
            print("1. Calcular factorial de un número divisible por 7")
            print("2. Ver historial")
            print("3. Salir")

            opcion = input("Ingrese su opción: ")

            if opcion == "1":
                try:
                    numero = int(input("Ingrese un número: "))
                    resultado = calcular_factorial(numero)
                    print(f"El factorial de {numero} es: {resultado}")
                    insertar_resultado(conexion, numero, resultado)
                    guardar_en_archivo(numero, resultado)

                except ValueError as ve:
                    print(ve)
                except Exception as e:
                    print("Error inesperado:", e)

            elif opcion == "2":
                mostrar_historial(conexion)

            elif opcion == "3":
                print("Saliendo...")
                break

            else:
                print("Opción no válida. Intente de nuevo.")

        conexion.close()

if __name__ == "__main__":
    main()
