import psycopg2
from datetime import date

def conectar():
    # Establecer la conexión con la base de datos
    conexion = psycopg2.connect(
        host="localhost",
        port="5432",
        database="seguimiento_pedidos",
        user="postgres",
        password="proyectos"
    )
    return conexion

def agregar_pedido(conexion, cliente_nombre, producto_nombre, cantidad):
    # Agregar un nuevo pedido a la base de datos
    cursor = conexion.cursor()
    cursor.execute("""
        INSERT INTO pedidos (cliente_nombre, producto_nombre, cantidad)
        VALUES (%s, %s, %s)
    """, (cliente_nombre, producto_nombre, cantidad))
    conexion.commit()
    cursor.close()

def actualizar_pedido(conexion, id_pedido, estado, fecha_entrega):
    # Actualizar la información de un pedido en la base de datos
    cursor = conexion.cursor()
    cursor.execute("""
        UPDATE pedidos
        SET estado = %s, fecha_entrega = %s
        WHERE id = %s
    """, (estado, fecha_entrega, id_pedido))
    conexion.commit()
    cursor.close()

def eliminar_pedido(conexion, id_pedido):
    # Eliminar un pedido de la base de datos
    cursor = conexion.cursor()
    cursor.execute("DELETE FROM pedidos WHERE id = %s", (id_pedido,))
    conexion.commit()
    cursor.close()

def mostrar_pedidos(conexion):
    # Mostrar todos los pedidos de la base de datos
    cursor = conexion.cursor()
    cursor.execute("SELECT * FROM pedidos")
    pedidos = cursor.fetchall()
    cursor.close()

    # Imprimir los pedidos
    if pedidos:
        print("ID  | Cliente            | Producto           | Cantidad | Estado    | Fecha Pedido | Fecha Entrega")
        print("----|--------------------|--------------------|----------|-----------|--------------|--------------")
        for pedido in pedidos:
            print(f"{pedido[0]:<4}| {pedido[1]:<18}| {pedido[2]:<18}| {pedido[3]:<9}| {pedido[4]:<10}| {pedido[5]:<13}| {pedido[6]}")
    else:
        print("No hay pedidos registrados.")

def menu():
    while True:
        print("Menú de opciones")
        print("1. Agregar pedido")
        print("2. Actualizar estado y fecha de entrega del pedido")
        print("3. Eliminar pedido")
        print("4. Mostrar todos los pedidos")
        print("5. Salir")

        opcion = input("Ingrese una opción: ")

        if opcion == "1":
            cliente_nombre = input("Ingrese el nombre del cliente: ")
            producto_nombre = input("Ingrese el nombre del producto: ")
            cantidad = int(input("Ingrese la cantidad del producto: "))
            agregar_pedido(conexion, cliente_nombre, producto_nombre, cantidad)
        elif opcion == "2":
            id_pedido = int(input("Ingrese el ID del pedido a actualizar: "))
            estado = input("Ingrese el nuevo estado del pedido: ")
            fecha_entrega = input("Ingrese la nueva fecha de entrega (YYYY-MM-DD): ")
            actualizar_pedido(conexion, id_pedido, estado, fecha_entrega)
        elif opcion == "3":
            id_pedido = int(input("Ingrese el ID del pedido a eliminar: "))
            eliminar_pedido(conexion, id_pedido)
        elif opcion == "4":
            mostrar_pedidos(conexion)
        elif opcion == "5":
            conexion.close()
            break
        else:
            print("Opción no válida")

if __name__ == "__main__":
    conexion = conectar()
    menu()
