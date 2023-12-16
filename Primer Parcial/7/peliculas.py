import psycopg2

# Conexión a la base de datos
conn = psycopg2.connect(
    host="localhost",
    database="peliculas",
    user="postgres",
    password="proyectos"
)
cursor = conn.cursor()

# Menú principal
def menu_principal():
    print("1. Obtener recomendaciones")
    print("2. Ingresar valoración")
    print("3. Agregar información")
    print("4. Mostrar información")
    print("5. Salir")

# Obtener recomendaciones para un usuario específico
def obtener_recomendaciones(id_usuario):
    query = """
        SELECT p.titulo
        FROM peliculas p
        JOIN valoraciones v ON p.id_pelicula = v.id_pelicula
        WHERE v.id_usuario = %s
        ORDER BY v.puntuacion DESC
        LIMIT 5;
    """
    cursor.execute(query, (id_usuario,))
    recomendaciones = cursor.fetchall()
    return recomendaciones

# Insertar una nueva valoración
def insertar_valoracion():
    usuario_id = int(input("Ingrese el ID del usuario: "))
    pelicula_id = int(input("Ingrese el ID de la película: "))
    puntuacion = int(input("Ingrese la puntuación (1-5): "))
    
    query = "INSERT INTO valoraciones (id_usuario, id_pelicula, puntuacion) VALUES (%s, %s, %s);"
    cursor.execute(query, (usuario_id, pelicula_id, puntuacion))
    conn.commit()
    print("Valoración insertada correctamente.")

# Agregar información a las tablas
def agregar_informacion():
    print("1. Agregar usuario")
    print("2. Agregar película")
    print("3. Agregar valoración")
    opcion = input("Seleccione una opción (1-3): ")

    if opcion == "1":
        nombre_usuario = input("Ingrese el nombre del usuario: ")
        edad_usuario = int(input("Ingrese la edad del usuario: "))
        query = "INSERT INTO usuarios (nombre, edad) VALUES (%s, %s) RETURNING id_usuario;"
        cursor.execute(query, (nombre_usuario, edad_usuario))
        nuevo_id_usuario = cursor.fetchone()[0]
        conn.commit()
        print(f"Usuario agregado con ID: {nuevo_id_usuario}")

    elif opcion == "2":
        titulo_pelicula = input("Ingrese el título de la película: ")
        genero_pelicula = input("Ingrese el género de la película: ")
        director_pelicula = input("Ingrese el director de la película: ")
        query = "INSERT INTO peliculas (titulo, genero, director) VALUES (%s, %s, %s) RETURNING id_pelicula;"
        cursor.execute(query, (titulo_pelicula, genero_pelicula, director_pelicula))
        nuevo_id_pelicula = cursor.fetchone()[0]
        conn.commit()
        print(f"Película agregada con ID: {nuevo_id_pelicula}")

    elif opcion == "3":
        insertar_valoracion()

# Mostrar información de las tablas
def mostrar_informacion():
    print("1. Mostrar usuarios")
    print("2. Mostrar películas")
    print("3. Mostrar valoraciones")
    opcion = input("Seleccione una opción (1-3): ")

    if opcion == "1":
        cursor.execute("SELECT * FROM usuarios;")
        usuarios = cursor.fetchall()
        for usuario in usuarios:
            print(usuario)
    elif opcion == "2":
        cursor.execute("SELECT * FROM peliculas;")
        peliculas = cursor.fetchall()
        for pelicula in peliculas:
            print(pelicula)
    elif opcion == "3":
        cursor.execute("SELECT * FROM valoraciones;")
        valoraciones = cursor.fetchall()
        for valoracion in valoraciones:
            print(valoracion)

# Menú principal
while True:
    menu_principal()
    opcion = input("Seleccione una opción (1-5): ")

    if opcion == "1":
        usuario_id = int(input("Ingrese el ID del usuario: "))
        recomendaciones = obtener_recomendaciones(usuario_id)
        print("Recomendaciones para el usuario {}: {}".format(usuario_id, recomendaciones))
    elif opcion == "2":
        insertar_valoracion()
    elif opcion == "3":
        agregar_informacion()
    elif opcion == "4":
        mostrar_informacion()
    elif opcion == "5":
        print("¡Hasta luego!")
        break
    else:
        print("Opción no válida. Inténtelo de nuevo.")

# Cierre de la conexión
cursor.close()
conn.close()
