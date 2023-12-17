import psycopg2

# Conexión a la base de datos PostgreSQL (asegúrate de cambiar los valores)
conexion = psycopg2.connect(
    dbname="pares_db",
    user="postgres",
    password="proyectos",
    host="localhost",
    port="5432"
)

def guardar_en_txt(resultado):
    try:
        with open('numeros_pares.txt', 'w') as archivo:
            archivo.write(resultado)
        print("Resultados guardados en 'numeros_pares.txt'.")
    except Exception as e:
        print(f"Error al guardar en el archivo: {e}")

def mostrar_en_consola(resultado):
    print("Números pares:", resultado)

# Pedir al usuario que ingrese el número de inicio y el número de fin
Primero = int(input("Ingrese el primer número: "))
Último = int(input("Ingrese el último número: "))

# Imprimir los números de 2 en 2 desde el inicio hasta el fin
resultado = ""
for valor in range(Primero, Último + 1, 2):
    print(valor, end=', ')
    resultado += str(valor) + ', '

# Cerrar la conexión a la base de datos al salir
conexion.close()

# Opciones adicionales
opcion = input("\n¿Desea guardar los resultados en un archivo? (S/N): ").upper()
if opcion == 'S':
    guardar_en_txt(resultado)

opcion = input("¿Desea mostrar los resultados en la consola? (S/N): ").upper()
if opcion == 'S':
    mostrar_en_consola(resultado)
