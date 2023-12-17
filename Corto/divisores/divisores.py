import psycopg2

# Parámetros de conexión a la base de datos PostgreSQL
parametros_conexion = {
    'host': 'localhost',
    'port': '5432',
    'user': 'postgres',
    'password': 'proyectos',
    'dbname': 'divisores_numero'
}

# Solicitar al usuario que ingrese un número
entrada_usuario = int(input("Ingrese un número: "))

# Inicializar una lista para almacenar los divisores
lista_divisores = []

# Encontrar los divisores del número
for divisor_candidato in range(1, entrada_usuario + 1):
    if entrada_usuario % divisor_candidato == 0:
        lista_divisores.append(divisor_candidato)

# Mostrar los divisores
print(f"Los divisores de {entrada_usuario} son: {lista_divisores}")

# Conectar a la base de datos y guardar los resultados
try:
    with psycopg2.connect(**parametros_conexion) as conexion:
        with conexion.cursor() as cursor:
            # Crear la tabla si no existe
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS divisores_numero (
                    id SERIAL PRIMARY KEY,
                    numero_ingresado INT NOT NULL,
                    divisor INT NOT NULL
                );
            """)
            # Insertar los divisores en la base de datos
            for divisor in lista_divisores:
                instruccion = "INSERT INTO divisores_numero(numero_ingresado, divisor) VALUES (%s, %s);"
                valores = (entrada_usuario, divisor)
                cursor.execute(instruccion, valores)
            conexion.commit()
    print("Resultados almacenados en la base de datos.")
except Exception as e:
    print(f"Error en la conexión o al guardar los resultados en la base de datos: {e}\n")

# Salida en un archivo de texto
with open('divisores.txt', 'w') as f:
    f.write(f"Los divisores de {entrada_usuario} son: {lista_divisores}\n")
