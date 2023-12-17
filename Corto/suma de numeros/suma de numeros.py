import psycopg2

# Conexión a la base de datos PostgreSQL (asegúrate de cambiar los valores)
conexion = psycopg2.connect(
    dbname="suma_numeros_db",
    user="postgres",
    password="proyectos",
    host="localhost",
    port="5432"
)

def calcular_suma(numero):
    suma = sum(range(1, numero + 1))
    return suma

def ver_historial():
    try:
        with conexion.cursor() as cursor:
            cursor.execute("SELECT * FROM resultados_suma")
            historial = cursor.fetchall()
        return historial
    except Exception as e:
        print(f"Error al obtener el historial: {e}")
        return []

def imprimir_historial(historial):
    print("\nHistorial de resultados:")
    print("ID  |  Resultado")
    print("---------------")
    for row in historial:
        print(f"{row[0]:2}  |  {row[1]}")

def guardar_en_txt(resultado):
    try:
        with open('suma_numeros.txt', 'w') as archivo:
            archivo.write(resultado)
        print("Resultados guardados en 'suma_numeros.txt'.")
    except Exception as e:
        print(f"Error al guardar en el archivo: {e}")

def guardar_en_db(resultado):
    try:
        with conexion.cursor() as cursor:
            cursor.execute("INSERT INTO resultados_suma (resultado) VALUES (%s)", (resultado,))
        conexion.commit()
        print("Resultado insertado en la base de datos.")
    except Exception as e:
        print(f"Error al insertar en la base de datos: {e}")

def main():
    opcion_menu = 0

    while opcion_menu != 3:
        print("\nMenú:")
        print("1. Calcular suma de números")
        print("2. Mostrar historial")
        print("3. Salir")

        opcion_menu = int(input("Ingrese su opción: "))

        if opcion_menu == 1:
            numero_ingresado = int(input("Ingrese un número: "))
            resultado = calcular_suma(numero_ingresado)
            print(f"La suma de los números del 1 a {numero_ingresado} es: {resultado}")

            # Guardar resultados en un archivo de texto
            guardar_en_txt(str(resultado))

            # Guardar resultados en la base de datos
            guardar_en_db(resultado)

        elif opcion_menu == 2:
            historial = ver_historial()
            imprimir_historial(historial)

        elif opcion_menu == 3:
            print("Fin del programa")

        else:
            print("Opción no válida. Intente de nuevo.")

    # Cerrar la conexión a la base de datos al salir
    conexion.close()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("Interrupción del usuario. Saliendo...")
    finally:
        # Cerrar la conexión a la base de datos al salir
        conexion.close()
