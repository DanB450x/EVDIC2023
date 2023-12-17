import psycopg2
from psycopg2 import sql
from tabulate import tabulate

# Conexión a la base de datos PostgreSQL (asegúrate de cambiar los valores)
conexion = psycopg2.connect(
    dbname="historial_taxi_db",
    user="postgres",
    password="proyectos",
    host="localhost",
    port="5432"
)

def es_bisiesto(anio):
    # Función para verificar si un año es bisiesto
    return (anio % 4 == 0 and anio % 100 != 0) or (anio % 400 == 0)

def insertar_en_historial(anio, bisiesto):
    # Función para insertar un registro en la base de datos
    with conexion.cursor() as cursor:
        cursor.execute(sql.SQL("""
            INSERT INTO historial_anios_taxi (anio, bisiesto)
            VALUES (%s, %s)
        """), (anio, bisiesto))
    conexion.commit()

def mostrar_historial():
    try:
        with conexion.cursor() as cursor:
            cursor.execute("SELECT * FROM historial_anios_taxi")
            historial = cursor.fetchall()

        print("\nHistorial de resultados:")
        print(tabulate(historial, headers=["Año", "Bisiesto"], tablefmt="psql", numalign="center"))
        return historial
    except Exception as e:
        print(f"Error al obtener el historial: {e}")
        return []

def guardar_en_txt(historial):
    try:
        with open('historial_anios_taxi.txt', 'w') as archivo:
            archivo.write("Historial de resultados:\n")
            for row in historial:
                archivo.write(f"Año: {row[0]}, Bisiesto: {row[1]}\n")
        print("Resultados guardados en 'historial_anios_taxi.txt'.")
    except Exception as e:
        print(f"Error al guardar en el archivo: {e}")

def main():
    while True:
        try:
            # Menú principal
            print("1. Verificar si un año es bisiesto")
            print("2. Mostrar historial")
            print("0. Salir")

            opcion = int(input("Ingrese su opción: "))

            if opcion == 1:
                # Verificar si un año es bisiesto
                anio = int(input("Ingrese el año: "))
                bisiesto = es_bisiesto(anio)
                print(f"El año {anio} {'es' if bisiesto else 'no es'} bisiesto.")
                insertar_en_historial(anio, bisiesto)

            elif opcion == 2:
                # Mostrar historial
                historial = mostrar_historial()

                # Guardar historial en un archivo de texto
                guardar_en_txt(historial)

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
    except KeyboardInterrupt:
        print("Interrupción del usuario. Saliendo...")
    finally:
        # Cerrar la conexión a la base de datos al salir
        conexion.close()
