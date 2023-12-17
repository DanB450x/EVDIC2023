import psycopg2
from tabulate import tabulate

def conectar_bd():
    try:
        conexion = psycopg2.connect(
            user="postgres",
            password="proyectos",
            host="localhost",
            port="5432",
            database="historial_triangulos_db"
        )
        return conexion
    except Exception as e:
        print("Error al conectar a la base de datos:", e)
        return None

def insertar_triangulo(conexion, lado1, lado2, lado3, tipo):
    try:
        cursor = conexion.cursor()
        cursor.execute("""
            INSERT INTO historial_triangulos (lado1, lado2, lado3, tipo)
            VALUES (%s, %s, %s, %s)
        """, (lado1, lado2, lado3, tipo))
        conexion.commit()
        print("Triángulo insertado correctamente.")
    except Exception as e:
        print("Error al insertar en la base de datos:", e)

def determinar_tipo(lado1, lado2, lado3):
    if lado1 == lado2 == lado3:
        return "Equilátero"
    elif lado1 == lado2 or lado1 == lado3 or lado2 == lado3:
        return "Isósceles"
    else:
        return "Escaleno"

def mostrar_historial(conexion):
    try:
        cursor = conexion.cursor()
        cursor.execute("SELECT * FROM historial_triangulos")

        print(tabulate(cursor, headers=["lado1", "lado2", "lado3", "tipo"], tablefmt="psql", numalign="center"))
    except Exception as e:
        print("Error al obtener el historial:", e)

def guardar_historial_txt(conexion):
    try:
        cursor = conexion.cursor()
        cursor.execute("SELECT * FROM historial_triangulos")

        with open('historial_triangulos.txt', 'w') as f:
            f.write("Historial de Triángulos:\n")
            for row in cursor:
                f.write(str(row) + '\n')
        print("Historial guardado en historial_triangulos.txt")
    except Exception as e:
        print("Error al guardar el historial en el archivo:", e)

def main():
    conexion = conectar_bd()

    if conexion:
        while True:
            print("\nMenú:")
            print("1. Ingresar 3 números enteros positivos")
            print("2. Ver historial")
            print("3. Guardar historial en archivo")
            print("4. Salir")

            opcion = input("Ingrese su opción: ")

            if opcion == "1":
                lado1 = int(input("Ingrese el primer lado: "))
                lado2 = int(input("Ingrese el segundo lado: "))
                lado3 = int(input("Ingrese el tercer lado: "))

                tipo = determinar_tipo(lado1, lado2, lado3)
                insertar_triangulo(conexion, lado1, lado2, lado3, tipo)

                print(f"El triángulo es {tipo}")

            elif opcion == "2":
                mostrar_historial(conexion)

            elif opcion == "3":
                guardar_historial_txt(conexion)

            elif opcion == "4":
                print("Saliendo...")
                break

            else:
                print("Opción no válida. Intente de nuevo.")

        conexion.close()

if __name__ == "__main__":
    main()
