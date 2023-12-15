import psycopg2
from datetime import date

# Conexión a la base de datos
def conectar_db():
    try:
        conexion = psycopg2.connect(
            database="presupuesto_personal",
            user="postgres",
            password="proyectos",
            host="localhost",
            port="5432"
        )
        print("Conexión exitosa a la base de datos.")
        return conexion
    except Exception as e:
        print("Error de conexión:", e)
        return None

# Crear tabla tipos_gastos si no existe
def crear_tabla_tipos_gastos(conexion):
    with conexion.cursor() as cursor:
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS tipos_gastos (
                id SERIAL PRIMARY KEY,
                nombre VARCHAR(255) NOT NULL
            );
        """)
        conexion.commit()

# Crear tabla gastos si no existe
def crear_tabla_gastos(conexion):
    with conexion.cursor() as cursor:
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS gastos (
                id SERIAL PRIMARY KEY,
                tipo_id INTEGER REFERENCES tipos_gastos(id),
                descripcion VARCHAR(255) NOT NULL,
                monto NUMERIC NOT NULL,
                fecha DATE NOT NULL
            );
        """)
        conexion.commit()

# Crear tabla presupuesto si no existe
def crear_tabla_presupuesto(conexion):
    with conexion.cursor() as cursor:
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS presupuesto (
                id SERIAL PRIMARY KEY,
                tipo_id INTEGER REFERENCES tipos_gastos(id),
                monto_presupuestado NUMERIC NOT NULL
            );
        """)
        conexion.commit()

# Función para ingresar un nuevo gasto
def ingresar_gasto(conexion):
    tipo_gasto = input("Ingrese el tipo de gasto: ")
    descripcion = input("Ingrese la descripción del gasto: ")
    monto = float(input("Ingrese el monto del gasto: "))
    fecha = date.today()

    with conexion.cursor() as cursor:
        # Obtener el ID del tipo de gasto o insertar uno nuevo si no existe
        cursor.execute("INSERT INTO tipos_gastos (nombre) VALUES (%s) ON CONFLICT (nombre) DO NOTHING RETURNING id;", (tipo_gasto,))
        tipo_id = cursor.fetchone()[0]

        # Insertar el gasto en la tabla gastos
        cursor.execute("INSERT INTO gastos (tipo_id, descripcion, monto, fecha) VALUES (%s, %s, %s, %s);", (tipo_id, descripcion, monto, fecha))
        conexion.commit()

    print("Gasto ingresado correctamente.")

# Función para ver un resumen de los gastos acumulados
def ver_resumen_gastos(conexion):
    with conexion.cursor() as cursor:
        cursor.execute("""
            SELECT tipos_gastos.nombre, SUM(gastos.monto) AS total_gastado
            FROM gastos
            JOIN tipos_gastos ON gastos.tipo_id = tipos_gastos.id
            GROUP BY tipos_gastos.nombre
            ORDER BY total_gastado DESC;
        """)
        resultados = cursor.fetchall()

        if resultados:
            print("\nResumen de Gastos Acumulados:")
            for resultado in resultados:
                print(f"{resultado[0]}: Q{resultado[1]:,.2f}")
        else:
            print("No hay gastos registrados.")

# Función para ajustar el presupuesto
def ajustar_presupuesto(conexion):
    tipo_gasto = input("Ingrese el tipo de gasto para ajustar el presupuesto: ")
    monto_presupuestado = float(input("Ingrese el nuevo monto presupuestado: "))

    with conexion.cursor() as cursor:
        # Obtener el ID del tipo de gasto o insertar uno nuevo si no existe
        cursor.execute("INSERT INTO tipos_gastos (nombre) VALUES (%s) ON CONFLICT (nombre) DO NOTHING RETURNING id;", (tipo_gasto,))
        tipo_id = cursor.fetchone()[0]

        # Actualizar o insertar el presupuesto en la tabla presupuesto
        cursor.execute("""
            INSERT INTO presupuesto (tipo_id, monto_presupuestado)
            VALUES (%s, %s)
            ON CONFLICT (tipo_id) DO UPDATE SET monto_presupuestado = EXCLUDED.monto_presupuestado;
        """, (tipo_id, monto_presupuestado))

        conexion.commit()

    print("Presupuesto ajustado correctamente.")

# Función principal
def main():
    conexion = conectar_db()
    if conexion:
        crear_tabla_tipos_gastos(conexion)
        crear_tabla_gastos(conexion)
        crear_tabla_presupuesto(conexion)

        while True:
            print("\n1. Ingresar nuevo gasto")
            print("2. Ver resumen de gastos acumulados")
            print("3. Ajustar presupuesto")
            print("4. Salir")

            opcion = input("Seleccione una opción: ")

            if opcion.isdigit():
                opcion = int(opcion)
                if opcion == 1:
                    ingresar_gasto(conexion)
                elif opcion == 2:
                    ver_resumen_gastos(conexion)
                elif opcion == 3:
                    ajustar_presupuesto(conexion)
                elif opcion == 4:
                    print("Saliendo del programa...")
                    break
                else:
                    print("Opción no válida.")
            else:
                print("Por favor, ingrese un número.")

        conexion.close()
        print("Conexión cerrada.")

if __name__ == "__main__":
    main()
