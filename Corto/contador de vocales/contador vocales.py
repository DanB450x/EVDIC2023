import psycopg2

# Parámetros de conexión a la base de datos PostgreSQL
parametros_conexion = {
    'host': 'localhost',
    'port': '5432',
    'user': 'postgres',
    'password': 'proyectos',
    'dbname': 'contador_vocales'
}

opcion_menu = 0  # Inicializamos la variable opcion_menu

def mostrar_menu():
    opcion = int(input("Menú principal \n" +
        "1. Iniciar \n" + 
        "2. Salir \n"))
    return opcion

while opcion_menu != 2:
    opcion_menu = mostrar_menu()
    
    if opcion_menu == 1:
        entrada_usuario = input("Ingrese una palabra o frase: ")
        contador_vocales = 0

        for caracter in entrada_usuario:
            if caracter in "aeiouáéíóú":
                contador_vocales += 1

        print("La cantidad de vocales es: ", contador_vocales)

        # Conectar a la base de datos y guardar los resultados
        try:
            with psycopg2.connect(**parametros_conexion) as conexion:
                with conexion.cursor() as cursor:
                    instruccion = "INSERT INTO cantidad_vocales(cantidad, entrada_usuario) VALUES (%s, %s);"
                    valores = (contador_vocales, entrada_usuario)
                    cursor.execute(instruccion, valores)
                    conexion.commit()
            print("Resultados almacenados en la base de datos.")
        except Exception as e:
            print(f"Error en la conexión o al guardar los resultados en la base de datos: {e}\n")

        # Salida en un archivo de texto
        with open('cantidad_vocales.txt', 'w') as f:
            f.write(f"La cantidad de vocales es: {contador_vocales}\n")

    elif opcion_menu == 2:
        print("Fin del programa")
