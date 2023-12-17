import psycopg2

# Conexión a la base de datos PostgreSQL (asegúrate de cambiar los valores)
conexion = psycopg2.connect(
    dbname="comparacion_numeros_db",
    user="postgres",
    password="proyectos",
    host="localhost",
    port="5432"
)

def comparar_numeros(num1, num2, num3):
    if num1 == num2 and num2 == num3:
        resultado = f"Los números son: {num1}, {num2}, {num3}. Todos son iguales."
    elif num1 == num2:
        resultado = f"El número diferente es: {num3}"
    elif num1 == num3:
        resultado = f"El número diferente es: {num2}"
    elif num2 == num3:
        resultado = f"El número diferente es: {num1}"
    else:
        mayor = max(num1, num2, num3)
        if mayor == num1:
            resultado = f"El resultado de la suma es: {num1 + num2 + num3}"
        elif mayor == num2:
            resultado = f"El resultado de la multiplicación es: {num1 * num2 * num3}"
        else:
            resultado = f"La concatenación de los números es: {str(num1) + str(num2) + str(num3)}"
    
    return resultado

def ver_historial():
    try:
        with conexion.cursor() as cursor:
            cursor.execute("SELECT * FROM resultados")
            historial = cursor.fetchall()
        return historial
    except Exception as e:
        print(f"Error al obtener el historial: {e}")
        return []

def guardar_en_txt(resultado):
    try:
        with open('comparacion_numeros.txt', 'w') as archivo:
            archivo.write(resultado)
        print("Resultados guardados en 'comparacion_numeros.txt'.")
    except Exception as e:
        print(f"Error al guardar en el archivo: {e}")

def main():
    while True:
        print("\nMenú:")
        print("1. Comparar números")
        print("2. Ver historial")
        print("3. Salir")

        opcion = input("Ingrese su opción: ")

        if opcion == "1":
            numero1 = int(input("Ingrese el primer número: "))
            numero2 = int(input("Ingrese el segundo número: "))
            numero3 = int(input("Ingrese el tercer número:"))

            resultado = comparar_numeros(numero1, numero2, numero3)

            try:
                with conexion.cursor() as cursor:
                    cursor.execute("INSERT INTO resultados (resultado_texto) VALUES (%s)", (resultado,))
                conexion.commit()
                print("Resultados insertados en la base de datos.")
            except Exception as e:
                print(f"Error al insertar en la base de datos: {e}")

            print(resultado)

            # Guardar resultados en un archivo de texto
            guardar_en_txt(resultado)

        elif opcion == "2":
            historial = ver_historial()
            if historial:
                print("\nHistorial:")
                for registro in historial:
                    print(registro[1])
            else:
                print("El historial está vacío.")

        elif opcion == "3":
            print("Saliendo...")
            break

        else:
            print("Opción no válida. Intente de nuevo.")

if __name__ == "__main__":
    try:
        main()
    finally:
        # Cerrar la conexión a la base de datos al salir
        conexion.close()
