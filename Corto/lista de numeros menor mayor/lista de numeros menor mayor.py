import psycopg2
from psycopg2 import sql

# Conexión a la base de datos PostgreSQL (asegúrate de cambiar los valores)
conexion = psycopg2.connect(
    dbname="numeros",
    user="postgres",
    password="proyectos",
    host="localhost",
    port="5432"
)

def obtener_lista_numeros():
    # Solicitar al usuario que ingrese dos números
    entrada_usuario1 = int(input("Ingrese el primer número: "))
    entrada_usuario2 = int(input("Ingrese el segundo número: "))

    # Determinar cuál es el mayor de los dos números
    numero_mayor = max(entrada_usuario1, entrada_usuario2)
    numero_menor = min(entrada_usuario1, entrada_usuario2)

    # Crear la lista de números desde el mayor hasta el menor
    lista_numeros = list(range(int(numero_mayor), int(numero_menor) - 1, -1))

    # Mostrar la lista de números
    print(f"Lista de números desde {numero_mayor} hasta {numero_menor}: {lista_numeros}")

    # Insertar en el historial
    insertar_en_historial(conexion, numero_mayor, numero_menor)

def insertar_en_historial(conexion, numero_mayor, numero_menor):
    # Función para insertar un registro en la base de datos
    with conexion.cursor() as cursor:
        cursor.execute(sql.SQL("""
            INSERT INTO historial_numeros (numero_mayor, numero_menor)
            VALUES (%s, %s)
        """), (numero_mayor, numero_menor))
    conexion.commit()

def mostrar_historial():
    try:
        cursor = conexion.cursor()
        cursor.execute("SELECT * FROM historial_numeros")

        historial = cursor.fetchall()
        for row in historial:
            print(f"ID: {row[0]}, Número Mayor: {row[1]}, Número Menor: {row[2]}")

        # Guardar historial en un archivo
        with open('historial_numeros.txt', 'w') as archivo:
            for row in historial:
                archivo.write(f"ID: {row[0]}, Número Mayor: {row[1]}, Número Menor: {row[2]}\n")

    except Exception as e:
        print(f"Error al obtener el historial: {e}")

def main():
    while True:
        try:
            # Menú principal
            print("1. Obtener lista de números y guardar en historial")
            print("2. Mostrar historial de números")
            print("0. Salir")

            opcion = int(input("Ingrese su opción: "))

            if opcion == 1:
                # Obtener lista de números y guardar en historial
                obtener_lista_numeros()

            elif opcion == 2:
                # Mostrar historial de números
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
