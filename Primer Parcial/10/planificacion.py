import psycopg2

# Conexión a la base de datos
conn = psycopg2.connect(
    host="localhost",
    database="planificacion_produccion",
    user="postgres",
    password="proyectos"
)
cursor = conn.cursor()

# Menú principal
def menu_principal():
    print("1. Ingresar nuevo producto")
    print("2. Ingresar nueva orden de producción")
    print("3. Mostrar productos")
    print("4. Mostrar órdenes de producción")
    print("5. Salir")

# Ingresar un nuevo producto
def ingresar_producto():
    nombre = input("Ingrese el nombre del producto: ")
    descripcion = input("Ingrese la descripción del producto: ")
    tiempo_produccion = int(input("Ingrese el tiempo estimado de producción por unidad: "))

    query = "INSERT INTO productos (nombre, descripcion, tiempo_produccion) VALUES (%s, %s, %s) RETURNING id_producto;"
    cursor.execute(query, (nombre, descripcion, tiempo_produccion))
    nuevo_id_producto = cursor.fetchone()[0]
    conn.commit()
    print(f"Producto agregado con ID: {nuevo_id_producto}")

# Ingresar una nueva orden de producción
def ingresar_orden_produccion():
    id_producto = int(input("Ingrese el ID del producto: "))
    cantidad = int(input("Ingrese la cantidad de unidades a producir: "))
    fecha_entrega = input("Ingrese la fecha de entrega solicitada (YYYY-MM-DD): ")

    query = "INSERT INTO ordenes_produccion (id_producto, cantidad, fecha_entrega) VALUES (%s, %s, %s) RETURNING id_orden;"
    cursor.execute(query, (id_producto, cantidad, fecha_entrega))
    nuevo_id_orden = cursor.fetchone()[0]
    conn.commit()
    print(f"Orden de producción agregada con ID: {nuevo_id_orden}")

# Mostrar productos
def mostrar_productos():
    cursor.execute("SELECT * FROM productos;")
    productos = cursor.fetchall()
    for producto in productos:
        print(producto)

# Mostrar órdenes de producción
def mostrar_ordenes_produccion():
    cursor.execute("SELECT * FROM ordenes_produccion;")
    ordenes_produccion = cursor.fetchall()
    for orden_produccion in ordenes_produccion:
        print(orden_produccion)

# Menú principal
while True:
    menu_principal()
    opcion = input("Seleccione una opción (1-5): ")

    if opcion == "1":
        ingresar_producto()
    elif opcion == "2":
        ingresar_orden_produccion()
    elif opcion == "3":
        mostrar_productos()
    elif opcion == "4":
        mostrar_ordenes_produccion()
    elif opcion == "5":
        print("¡Hasta luego!")
        break
    else:
        print("Opción no válida. Inténtelo de nuevo.")

# Cierre de la conexión
cursor.close()
conn.close()
