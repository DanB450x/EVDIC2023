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
        entrada_usuario = entrada_usuario.lower()
        vocales = ["a", "e", "i", "o", "u", "á", "é", "í", "ó", "ú"]

        frecuencias = {}
        
        for vocal in vocales:
            veces = 0
            for caracter in entrada_usuario:
                if vocal == caracter:
                    veces += 1
            frecuencias[vocal] = veces

        # Conectar a la base de datos y guardar los resultados
        try:
            with psycopg2.connect(**parametros_conexion) as conexion:
                with conexion.cursor() as cursor:
                    for vocal, frecuencia in frecuencias.items():
                        instruccion = "INSERT INTO frecuencia_vocales(vocal, frecuencia, entrada_usuario) VALUES (%s, %s, %s);"
                        valores = (vocal, frecuencia, entrada_usuario)
                        cursor.execute(instruccion, valores)
                    conexion.commit()
            print("Resultados almacenados en la base de datos.")

            # Mostrar los resultados en el código
            print("Resultados del conteo de vocales:")
            for vocal, frecuencia in frecuencias.items():
                print(f"{vocal}: {frecuencia} veces")

        except Exception as e:
            print(f"Error en la conexión o al guardar los resultados en la base de datos: {e}\n")

        # Salida en un archivo de texto
        with open('vocales.txt', 'w') as f:
            f.write("Resultados del conteo de vocales:\n")
            for vocal, frecuencia in frecuencias.items():
                f.write(f"{vocal}: {frecuencia} veces\n")

    elif opcion_menu == 2:
        print("Fin del programa")
