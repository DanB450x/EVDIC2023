import psycopg2
import matplotlib.pyplot as plt
import pandas as pd

def conectar():
    # Establecer la conexión con la base de datos
    conexion = psycopg2.connect(
        host="localhost",
        port="5432",
        database="analisis_sensores",
        user="postgres",
        password="proyectos"
    )
    return conexion

def agregar_columnas_si_no_existen(conexion):
    try:
        cursor = conexion.cursor()
        # Intentar agregar columnas valor1 y valor2
        cursor.execute("""
            ALTER TABLE datos_sensores
            ADD COLUMN valor1 FLOAT,
            ADD COLUMN valor2 FLOAT;
        """)
        conexion.commit()
        cursor.close()
    except psycopg2.errors.DuplicateColumn:
        # Ignorar error si las columnas ya existen
        pass

def agregar_muestra_sensor(conexion, sensor_nombre, valor1, valor2):
    try:
        # Agregar una nueva muestra de sensor a la base de datos
        with conexion.cursor() as cursor:
            cursor.execute("""
                INSERT INTO datos_sensores (sensor_nombre, valor1, valor2)
                VALUES (%s, %s, %s)
            """, (sensor_nombre, valor1, valor2))
        conexion.commit()
    except Exception as e:
        # Imprimir el error
        print(f"Error al agregar muestra de sensor: {e}")
        # Revertir la transacción
        conexion.rollback()

def obtener_datos_sensor(conexion, sensor_nombre):
    # Obtener los datos del sensor desde la base de datos
    with conexion.cursor() as cursor:
        cursor.execute("""
            SELECT fecha_muestra, valor1, valor2
            FROM datos_sensores
            WHERE sensor_nombre = %s
        """, (sensor_nombre,))
        datos = cursor.fetchall()
    return datos

def mostrar_grafico(datos, sensor_nombre):
    # Mostrar un gráfico con los datos del sensor
    df = pd.DataFrame(data=datos, columns=['Fecha Muestra', 'Valor1', 'Valor2'])
    plt.plot(df['Fecha Muestra'], df['Valor1'], label='Valor1')
    plt.plot(df['Fecha Muestra'], df['Valor2'], label='Valor2')
    plt.title(f'Datos del Sensor: {sensor_nombre}')
    plt.xlabel('Fecha Muestra')
    plt.ylabel('Valor')
    plt.legend()
    plt.show()

def menu():
    while True:
        print("Menú de opciones")
        print("1. Agregar muestra de sensor")
        print("2. Mostrar gráfico de datos de sensor")
        print("3. Salir")

        opcion = input("Ingrese una opción: ")

        if opcion == "1":
            sensor_nombre = input("Ingrese el nombre del sensor: ")
            valor1 = float(input("Ingrese el primer valor del sensor: "))
            valor2 = float(input("Ingrese el segundo valor del sensor: "))
            agregar_muestra_sensor(conexion, sensor_nombre, valor1, valor2)
        elif opcion == "2":
            sensor_nombre = input("Ingrese el nombre del sensor para mostrar el gráfico: ")
            datos_sensor = obtener_datos_sensor(conexion, sensor_nombre)
            if datos_sensor:
                mostrar_grafico(datos_sensor, sensor_nombre)
            else:
                print(f"No hay datos disponibles para el sensor {sensor_nombre}.")
        elif opcion == "3":
            conexion.close()
            break
        else:
            print("Opción no válida")

if __name__ == "__main__":
    conexion = conectar()
    agregar_columnas_si_no_existen(conexion)
    menu()
