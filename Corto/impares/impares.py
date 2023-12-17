import psycopg2
from psycopg2 import sql
from tabulate import tabulate

# Conexión a la base de datos PostgreSQL (asegúrate de cambiar los valores)
conexion = psycopg2.connect(
    dbname="impares",
    user="postgres",
    password="proyectos",
    host="localhost",
    port="5432"
)

def obtener_impares():
    # Función para obtener los números impares del 1 al 100
    impares = [i for i in range(1, 101) if i % 2 != 0]
    return impares

def contar_impares():
    # Función para contar la cantidad de números impares
    return len(obtener_impares())

def insertar_en_historial(conexion, cantidad_impares):
    # Función para insertar un registro en la base de datos
    with conexion.cursor() as cursor:
        cursor.execute(sql.SQL("""
            INSERT INTO historial_impares (cantidad)
            VALUES (%s)
        """), (cantidad_impares,))
    conexion.commit()

def mostrar_historial():
    try:
        cursor = conexion.cursor()
        cursor.execute("SELECT * FROM historial_impares")

        historial = cursor.fetchall()
        print(tabulate(historial, headers=["ID", "Cantidad Impares"], tablefmt="psql", numalign="center"))

        # Guardar historial en un archivo
        with open('historial_impares.txt', 'w') as archivo:
            archivo.write(tabulate(historial, headers=["ID", "Cantidad Impares"], tablefmt="psql", numalign="center"))

    except Exception as e:
        print(f"Error al obtener el historial: {e}")

def main():
    while True:
        try:
            # Menú principal
            print("1. Mostrar números impares del 1 al 100")
            print("2. Contar la cantidad de números impares")
            print("3. Mostrar historial de impares")
            print("0. Salir")

            opcion = int(input("Ingrese su opción: "))

            if opcion == 1:
                # Mostrar números impares
                impares = obtener_impares()
                print("Números impares del 1 al 100:", impares)

            elif opcion == 2:
                # Contar la cantidad de números impares
                cantidad_impares = contar_impares()
                print(f"Hay {cantidad_impares} números impares del 1 al 100.")
                insertar_en_historial(conexion, cantidad_impares)

            elif opcion == 3:
                # Mostrar historial de impares
                mostrar_historial()

            elif opcion == 0:
                # Salir del programa
                break

            else:
                print("Opción no válida. Intente nuevamente.")

        except ValueError:
            print("Por favor, ingrese un número válido.")

if __name__ == "__main__":
    try:
        main()
    finally:
        # Cerrar la conexión a la base de datos al salir
        conexion.close()
