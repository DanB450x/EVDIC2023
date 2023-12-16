import psycopg2
from datetime import date

def conectar():
    # Establecer la conexión con la base de datos
    conexion = psycopg2.connect(
        host="localhost",
        port="5432",
        database="monitoreo_ventas",
        user="postgres",
        password="proyectos"
    )
    return conexion

def agregar_venta(conexion, producto_nombre, cantidad, precio_unitario):
    # Agregar una nueva venta a la base de datos
    cursor = conexion.cursor()
    cursor.execute("""
        INSERT INTO ventas (producto_nombre, cantidad, precio_unitario)
        VALUES (%s, %s, %s)
    """, (producto_nombre, cantidad, precio_unitario))
    conexion.commit()
    cursor.close()

def generar_informe_ventas(conexion):
    # Generar un informe de ventas
    cursor = conexion.cursor()
    cursor.execute("SELECT * FROM ventas")
    ventas = cursor.fetchall()
    cursor.close()

    # Imprimir el informe
    if ventas:
        print("ID  | Producto            | Cantidad | Precio Unitario | Fecha Venta")
        print("----|----------------------|----------|------------------|-------------")
        for venta in ventas:
            print(f"{venta[0]:<4}| {venta[1]:<20}| {venta[2]:<9}| {venta[3]:<16}| {venta[4]}")
    else:
        print("No hay ventas registradas.")

def analizar_datos_ventas(conexion):
    # Analizar los datos de ventas (puedes personalizar esta función según tus necesidades)
    cursor = conexion.cursor()
    cursor.execute("SELECT producto_nombre, SUM(cantidad) AS total_cantidad FROM ventas GROUP BY producto_nombre")
    resultados = cursor.fetchall()
    cursor.close()

    # Imprimir los resultados del análisis
    if resultados:
        print("Producto            | Total Cantidad Vendida")
        print("---------------------|------------------------")
        for resultado in resultados:
            print(f"{resultado[0]:<20}| {resultado[1]}")
    else:
        print("No hay datos para analizar.")

def menu():
    while True:
        print("Menú de opciones")
        print("1. Agregar venta")
        print("2. Generar informe de ventas")
        print("3. Analizar datos de ventas")
        print("4. Salir")

        opcion = input("Ingrese una opción: ")

        if opcion == "1":
            producto_nombre = input("Ingrese el nombre del producto: ")
            cantidad = int(input("Ingrese la cantidad vendida: "))
            precio_unitario = float(input("Ingrese el precio unitario del producto: "))
            agregar_venta(conexion, producto_nombre, cantidad, precio_unitario)
        elif opcion == "2":
            generar_informe_ventas(conexion)
        elif opcion == "3":
            analizar_datos_ventas(conexion)
        elif opcion == "4":
            conexion.close()
            break
        else:
            print("Opción no válida")

if __name__ == "__main__":
    conexion = conectar()
    menu()
