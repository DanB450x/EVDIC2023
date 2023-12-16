import psycopg2

# Conexión a la base de datos (sustituye 'nombre_de_tu_base' por el nombre de tu base de datos)
conn = psycopg2.connect(
    host="localhost",
    database="canciones",
    user="postgres",
    password="proyectos"
)
cursor = conn.cursor()

# Menú principal
def menu_principal():
    print("1. Desplegar el listado de canciones")
    print("2. Buscar por artista")
    print("3. Buscar por canción")
    print("4. Ingresar nueva canción")
    print("5. Salir")

# Desplegar el listado de canciones
def desplegar_canciones():
    cursor.execute("SELECT * FROM canciones;")
    canciones = cursor.fetchall()
    for cancion in canciones:
        print(f"Artista: {cancion[1]}, Canción: {cancion[2]}, Letra: {cancion[3]}")

# Buscar por artista
def buscar_por_artista():
    artista = input("Ingrese el nombre del artista: ")
    query = "SELECT * FROM canciones WHERE artista ILIKE %s;"
    cursor.execute(query, (f"%{artista}%",))
    canciones = cursor.fetchall()
    for cancion in canciones:
        print(f"Artista: {cancion[1]}, Canción: {cancion[2]}, Letra: {cancion[3]}")

# Buscar por canción
def buscar_por_cancion():
    cancion = input("Ingrese el nombre de la canción: ")
    query = "SELECT * FROM canciones WHERE cancion ILIKE %s;"
    cursor.execute(query, (f"%{cancion}%",))
    canciones = cursor.fetchall()
    for cancion in canciones:
        print(f"Artista: {cancion[1]}, Canción: {cancion[2]}, Letra: {cancion[3]}")

# Ingresar nueva canción
def ingresar_nueva_cancion():
    artista = input("Ingrese el nombre del artista: ")
    cancion = input("Ingrese el nombre de la canción: ")
    letra = input("Ingrese la letra de la canción: ")

    query = "INSERT INTO canciones (artista, cancion, letra) VALUES (%s, %s, %s) RETURNING id_cancion;"
    cursor.execute(query, (artista, cancion, letra))
    nueva_id_cancion = cursor.fetchone()[0]
    conn.commit()
    print(f"Canción agregada con ID: {nueva_id_cancion}")

# Menú principal
while True:
    menu_principal()
    opcion = input("Seleccione una opción (1-5): ")

    if opcion == "1":
        desplegar_canciones()
    elif opcion == "2":
        buscar_por_artista()
    elif opcion == "3":
        buscar_por_cancion()
    elif opcion == "4":
        ingresar_nueva_cancion()
    elif opcion == "5":
        print("¡Hasta luego!")
        break
    else:
        print("Opción no válida. Inténtelo de nuevo.")

# Cierre de la conexión
cursor.close()
conn.close()
