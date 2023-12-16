import psycopg2

def conectar():
    # Establecer la conexión con la base de datos
    conexion = psycopg2.connect(
        host="localhost",
        port="5432",
        database="registro_estudiantes",
        user="postgres",
        password="proyectos"
    )
    return conexion

def agregar_estudiante(conexion, nombre, edad, genero, direccion):
    # Crear un nuevo estudiante en la base de datos
    cursor = conexion.cursor()
    cursor.execute("""
        INSERT INTO estudiantes (nombre, edad, genero, direccion)
        VALUES (%s, %s, %s, %s)
    """, (nombre, edad, genero, direccion))
    conexion.commit()
    cursor.close()

def editar_estudiante(conexion, id_estudiante, nombre, edad, genero, direccion):
    # Editar la información de un estudiante en la base de datos
    cursor = conexion.cursor()
    cursor.execute("""
        UPDATE estudiantes
        SET nombre = %s, edad = %s, genero = %s, direccion = %s
        WHERE id = %s
    """, (nombre, edad, genero, direccion, id_estudiante))
    conexion.commit()
    cursor.close()

def eliminar_estudiante(conexion, id_estudiante):
    # Eliminar un estudiante de la base de datos
    cursor = conexion.cursor()
    cursor.execute("DELETE FROM estudiantes WHERE id = %s", (id_estudiante,))
    conexion.commit()
    cursor.close()

def mostrar_estudiantes(conexion):
    # Consultar los estudiantes de la base de datos
    cursor = conexion.cursor()
    cursor.execute("SELECT * FROM estudiantes")
    estudiantes = cursor.fetchall()
    cursor.close()

    # Imprimir los estudiantes
    for estudiante in estudiantes:
        print("ID:", estudiante[0])
        print("Nombre:", estudiante[1])
        print("Edad:", estudiante[2])
        print("Género:", estudiante[3])
        print("Dirección:", estudiante[4])
        print("-----------------------------")

def menu():
    while True:
        # Imprimir el menú
        print("Menú de opciones")
        print("1. Agregar estudiante")
        print("2. Mostrar estudiantes")
        print("3. Editar estudiante")
        print("4. Eliminar estudiante")
        print("5. Salir")

        # Obtener la opción del usuario
        opcion = input("Ingrese una opción: ")

        # Procesar la opción
        if opcion == "1":
            # Agregar estudiante
            nombre = input("Ingrese el nombre del estudiante: ")
            edad = input("Ingrese la edad del estudiante: ")
            genero = input("Ingrese el género del estudiante: ")
            direccion = input("Ingrese la dirección del estudiante: ")
            agregar_estudiante(conexion, nombre, edad, genero, direccion)
        elif opcion == "2":
            # Mostrar estudiantes
            mostrar_estudiantes(conexion)
        elif opcion == "3":
            # Editar estudiante
            id_estudiante = input("Ingrese el ID del estudiante a editar: ")
            nombre = input("Ingrese el nuevo nombre del estudiante: ")
            edad = input("Ingrese la nueva edad del estudiante: ")
            genero = input("Ingrese el nuevo género del estudiante: ")
            direccion = input("Ingrese la nueva dirección del estudiante: ")
            editar_estudiante(conexion, id_estudiante, nombre, edad, genero, direccion)
        elif opcion == "4":
            # Eliminar estudiante
            id_estudiante = input("Ingrese el ID del estudiante a eliminar: ")
            eliminar_estudiante(conexion, id_estudiante)
        elif opcion == "5":
            # Salir
            conexion.close()
            break
        else:
            # Opción no válida
            print("Opción no válida")

if __name__ == "__main__":
    conexion = conectar()
    menu()
