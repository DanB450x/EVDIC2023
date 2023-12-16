import psycopg2
from decimal import Decimal
from datetime import datetime

# Conéctate a la base de datos (reemplaza los valores con los tuyos)
conn = psycopg2.connect(
    dbname="inventario",
    user="postgres",
    password="proyectos",
    host="localhost",
    port="5432"
)

# Crea un cursor para ejecutar comandos SQL
cur = conn.cursor()

# Crea las tablas (asegúrate de ejecutar estos comandos una sola vez)
cur.execute('''
    CREATE TABLE IF NOT EXISTS categorias (
        id SERIAL PRIMARY KEY,
        nombre VARCHAR(100) NOT NULL
    )
''')

cur.execute('''
    CREATE TABLE IF NOT EXISTS proveedores (
        id SERIAL PRIMARY KEY,
        nombre VARCHAR(100) NOT NULL,
        direccion VARCHAR(255),
        telefono VARCHAR(20)
    )
''')

cur.execute('''
    CREATE TABLE IF NOT EXISTS productos (
        id SERIAL PRIMARY KEY,
        nombre VARCHAR(100) NOT NULL,
        descripcion TEXT,
        precio DECIMAL(10, 2) NOT NULL,
        cantidad INTEGER NOT NULL,
        categoria_id INTEGER REFERENCES categorias(id),
        proveedor_id INTEGER REFERENCES proveedores(id),
        fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
''')

# Guarda los cambios
conn.commit()

# Función para agregar una categoría si no existe
def agregar_categoria(nombre_categoria):
    cur.execute("INSERT INTO categorias (nombre) VALUES (%s) ON CONFLICT DO NOTHING", (nombre_categoria,))
    conn.commit()

# Función para agregar un proveedor si no existe
def agregar_proveedor(nombre_proveedor, direccion_proveedor, telefono_proveedor):
    cur.execute("INSERT INTO proveedores (nombre, direccion, telefono) VALUES (%s, %s, %s) ON CONFLICT DO NOTHING",
                (nombre_proveedor, direccion_proveedor, telefono_proveedor))
    conn.commit()

# Función para agregar un producto
def agregar_producto():
    nombre = input("Ingrese el nombre del producto: ")
    descripcion = input("Ingrese la descripción del producto: ")
    precio = Decimal(input("Ingrese el precio del producto: "))
    cantidad = int(input("Ingrese la cantidad del producto: "))
    nombre_categoria = input("Ingrese el nombre de la categoría: ")
    nombre_proveedor = input("Ingrese el nombre del proveedor: ")

    # Asegúrate de que la categoría y el proveedor existan
    agregar_categoria(nombre_categoria)
    agregar_proveedor(nombre_proveedor, "Dirección de ejemplo", "Teléfono de ejemplo")

    # Obtiene el ID de la categoría
    cur.execute('SELECT id FROM categorias WHERE nombre = %s', (nombre_categoria,))
    categoria_id = cur.fetchone()[0]

    # Obtiene el ID del proveedor
    cur.execute('SELECT id FROM proveedores WHERE nombre = %s', (nombre_proveedor,))
    proveedor_id = cur.fetchone()[0]

    # Inserta el producto
    cur.execute('''
        INSERT INTO productos (nombre, descripcion, precio, cantidad, categoria_id, proveedor_id)
        VALUES (%s, %s, %s, %s, %s, %s)
    ''', (nombre, descripcion, precio, cantidad, categoria_id, proveedor_id))

    conn.commit()
    print("Producto agregado con éxito!")

# Función para obtener la lista de productos
def obtener_productos():
    cur.execute('SELECT * FROM productos')
    productos = cur.fetchall()
    for producto in productos:
        print(producto)

# Menú de selección
while True:
    print("\nMenu:")
    print("1. Agregar Producto")
    print("2. Mostrar Productos")
    print("3. Salir")

    opcion = input("Ingrese la opción: ")

    if opcion == "1":
        agregar_producto()
    elif opcion == "2":
        obtener_productos()
    elif opcion == "3":
        break
    else:
        print("Opción no válida. Intente de nuevo.")

# Cierra la conexión
cur.close()
conn.close()

