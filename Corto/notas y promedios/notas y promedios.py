import psycopg2
from tabulate import tabulate

# Conexión a la base de datos PostgreSQL (asegúrate de cambiar los valores)
conexion = psycopg2.connect(
    dbname="notas_db",
    user="postgres",
    password="proyectos",
    host="localhost",
    port="5432"
)

def Historial():
    try:
        cursor = conexion.cursor()
        cursor.execute("SELECT * from registro_notas;")

        rows = cursor.fetchall()
        print(tabulate(rows, headers=["numero1", "numero2", "numero3", "final"], tablefmt="psql", numalign="center"))

        # Guardar historial en un archivo
        with open('historial_notas.txt', 'w') as archivo:
            archivo.write(tabulate(rows, headers=["numero1", "numero2", "numero3", "final"], tablefmt="psql", numalign="center"))
        
    except Exception as e:
        print(f"Error en la conexión o al obtener el historial: {e}\n")

def Post(nota1, nota2, nota3, final):
    try:
        with conexion.cursor() as cursor:
            instruccion = "INSERT INTO registro_notas(numero1, numero2, numero3, final) VALUES (%s, %s, %s, %s);"
            valores = (nota1, nota2, nota3, final)
            cursor.execute(instruccion, valores)
            conexion.commit()
        print("Se ha escrito en la base de datos.")
    except Exception as e:
        print(f"Error en el ingreso de datos o de conexión: {e}\n")

def nota():
    promedio = (nota1 + nota2 + nota3) / 3

    if promedio >= 60:
        final = 'Aprobado'
        print(f"¡Aprobado! El promedio es {promedio:.2f}")
    else:
        final = 'Reprobado'
        print(f"Reprobado. El promedio es {promedio:.2f}")

    return final

opcion = " "

print(" Cuadro de notas")

while opcion != 'X':
    print("Seleccione una opción del siguiente menú:\n'1' Ingresar notas\n'0' Ver historial\n'X' Salir")
    opcion = input("Su elección: ").upper()

    if opcion == '1':
        nota1 = int(input("Ingrese la primera nota: "))
        nota2 = int(input("Ingrese la segunda nota: "))
        nota3 = int(input("Ingrese la tercera nota: "))

        resultado = nota()
        Post(nota1, nota2, nota3, resultado)

    elif opcion == '0':
        Historial()

    elif opcion == 'X':
        break

    else:
        print("Opción no válida, ingrese una de las opciones del menú")

# Cerrar la conexión a la base de datos al salir
conexion.close()
